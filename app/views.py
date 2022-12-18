from flask import render_template, url_for,flash, redirect,request
from flask_login import login_user, current_user, logout_user, login_required
from .models import Perfumes, User
from .forms import RegistrationForm, LoginForm, CpasswordForm
from werkzeug.security import generate_password_hash,check_password_hash

from app import app, db, admin
from flask_admin.contrib.sqla import ModelView

#admin.add_view(ModelView(User, db.session))                     #As per Section 8 Relations and flask admin example
#admin.add_view(ModelView(Perfumes, db.session))                 #Which allows the admin to create new records for the database non-exhaustively

#Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()                                                           #Retrieves data from the form from forms.py
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)        #retrieve a record
        db.session.add(user)                                                                                #and commit this record to the database
        db.session.commit()
        flash('Thanks for registering! Now you can login!')                                                 #provide flash message
        return redirect(url_for('login'))                                                                   #once the account has been created redirect it to the login page so that the user can login and start using
    return render_template('register.html', form=form)


#Log-in
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():                                                       #validating the forms to check as per field validations from models.py
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:                #check the password and check nothing is missing
            login_user(user)
            flash('Log-in successful!')                                                 #flashed login success!
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('index')
            return redirect(next)
    return render_template('login.html', form=form)

#Log-out
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))                   #upon logout return to about page

#Default page
@app.route('/')
def index():
    return render_template('about.html')                #routes to Company's blog page

#Company's aboout page
@app.route('/about')
def about():
    return render_template('about.html')                #routes to Company's blog page

#Error_404 handler
@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404             #returns the error code and renders the corresponding web-page

#Error_403 handler
@app.errorhandler(403)
def error_403(error):
    return render_template('403.html'), 403             #returns the error code and renders the corresponding web-page

#Changepassword
@app.route('/changepwd', methods=['GET','POST'])
@login_required                                         #provided that the user has logged in
def changepassword():
    form = CpasswordForm()                              #retrieves data from CpasswordForm()
    user = User.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():                                                   #if the form passes all the validation tests
        if user is None or not user.check_password(form.password.data):             #if the login details has been provided for the user that hasn't been
            flash('Wrong Current Password')                                         
            return redirect('/changepwd')                                           #the user wil be asked to change the password redirecting to the sane page!
        newpassword = form.npassword.data                                           #setting aliases for conciseness
        user.password = form.npassword.data
        db.session.commit()                                                         #commits to the database
        login_user(user)
        return redirect('/')                                                        #redirects to the company's blog page
    return render_template('change_password.html', title='Change Password',form = form)         


#app route to allow users to add item to cart
@app.route('/add_perfume/<id>', methods=['POST'])               #the route shows perfume by id
@login_required                                                 #provided that the user has logged in
def add_to_cart(id):
    Perfume = Perfumes.query.filter_by(id = id).first()
    user = current_user

    if request.method == 'POST':
        user.perfumes.append(Perfume)                           #add this record
        db.session.commit()                                     #commits to the dataabse
    return redirect('/allp')

#When a perfume is being removed it redirects to the page where the company sells all the perfumes
@app.route('/remove_perfume/<id>', methods=['GET','POST'])
@login_required                                                 #provided that the authenticated user has logged in
def rem_from_cart(id):
    Perfume = Perfumes.query.filter_by(id = id).first()         #retrieve perfume by id
    user = current_user                                         #define aliases
    user.perfumes.remove(Perfume)                               #remove perfumes by the Pointer
    db.session.commit()                                         #commit changes to the database
    return redirect('/allp')

#Shows all of the items that are saved or added to the cart
@app.route('/mc')
@login_required                                                                         #provided that the authenticated user has logged in
def Mystuff():
    user_items= User.query.filter_by(id = current_user.id).first()                      #retrieve user_items by id
    data = user_items.perfumes                                                          #define aliases
    username = user_items.username
    return render_template('savedperfumes.html', data = data, username = username)

#All perfumes that the company is selling!
@app.route('/allp')
@login_required                                                     #If and only if the authenticated user has logged in
def allperfumes():
    result = Perfumes.query.all()                                   #Retrieve all the records in the database
    return render_template('myperfumes.html', data = result)