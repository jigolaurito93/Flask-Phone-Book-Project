from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm, LoginForm, PhoneForm
from app.models import User, Contact
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/home')
@login_required
def home():
    posts = Contact.query.all()
    if current_user.is_authenticated:
        contacts=Contact.query.filter(Contact.user_id == current_user.id).all()
        return render_template('home.html', contacts=contacts)
    else:
        return render_template('home.html', contacts=[])
    


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Successfully Signed Up..')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        # CHeck to see if there is already a user with either username or email
        check_user = db.session.execute(db.select(User).filter((User.username == username) | (User.email == email))).scalars().all()
        if check_user:
            # Flash a message saying that user with email/username already exists
            flash('A user with that username and/or email already exists','warning')
            return redirect(url_for('signup'))
        # If check_user is empty, create a new record in the user table
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        flash(f"Thank you {new_user.username} for signing up!", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)  


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Successfull Logged In..')
        username = form.username.data
        password = form.password.data
        print(username, password)
        # TODO: Check if there is a user with username and that password
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f'You have succesfully logged in as {username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username and/or password. Please try again', 'danger')
            return redirect(url_for('login'))

        
    return render_template('login.html', form=form)




@app.route("/add-phone", methods=["GET", "POST"])
@login_required
def add_phone():
    form = PhoneForm()
    # Check if the form was submitted and is valid
    if form.validate_on_submit():
        first = form.first_name.data
        last = form.last_name.data
        address = form.address.data
        phone_number = form.phone_number.data
        user_id = current_user.id

        print(first, last, address, phone_number)
        new_contact = Contact(first_name=first, last_name=last, address=address, phone_number=phone_number, user_id= user_id) 
        flash(f"{new_contact.first_name} {new_contact.last_name} has been added to the phone book", "success")
        return redirect(url_for('home'))
    return render_template('add_phone.html', form=form)


@app.route('/contacts/<contact_id>')
def view_single_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id) # SELECT * FROM post WHERE id = post_id  --(post_id comes from the URL)
    return render_template('single_contact.html', contact=contact)



#edit_contact page is where logged in user can edit contact that belongs to them
@app.route('/edit-contacts/<contact_id>', methods=["GET", "POST"])
@login_required
def edit_contact(contact_id):
    form = PhoneForm()
    contact_to_edit = Contact.query.get_or_404(contact_id)
    if current_user != contact_to_edit.user:
        flash("You do not have permission to edit this contact", "danger")
        return redirect(url_for('home'))
    

    if form.validate_on_submit():
        # If form submitted, update Contact
        contact_to_edit.first_name = form.first_name.data
        contact_to_edit.last_name = form.last_name.data
        contact_to_edit.address = form.address.data
        contact_to_edit.phone_number = form.phone_number.data
        # Commit that to the database
        db.session.commit()
        flash(f'{contact_to_edit.email} has been updated', 'primary')
        return redirect(url_for('home'))
        # return redirect(url_for('view_single_contact', contact_id=contact_to_edit.id))
    
    # Pre-populate form with contact feed
    form.first_name.data = contact_to_edit.first_name
    form.last_name.data = contact_to_edit.last_name
    form.address.data = contact_to_edit.address
    form.phone_number.data = contact_to_edit.phone_number

    return render_template('edit_contact.html', contact=contact_to_edit, form=form)





@app.route('/delete-contacts/<contact_id>')
@login_required
def delete_contact(contact_id):
    contact_to_delete = Contact.query.get_or_404(contact_id)
    if current_user != contact_to_delete.user:
        flash("You do not have permission to delete this contact", "danger")
        return redirect(url_for('home'))
    contact_to_delete.delete()
    flash(f'Entry for {contact_to_delete.first_name} {contact_to_delete.last_name} has been deleted', 'info')
    return redirect(url_for('home'))




@app.route('/logout')
def logout():
    logout_user()
    flash("You have logged out", "info")
    return redirect(url_for('index'))


