from flask import flash, render_template, request, redirect, session
from flask_app import app, bcrypt # ...server.py
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' in session:
            return f(*args, **kwargs)
        else:
            flash("you need to login first")
            return redirect ("/user/login_registration")
    return wrap

#CREATE
# route to post register
# method = post 
@app.route('/home')         
def home():
    context ={
        'user' : User.get_one(id),
        'all_recipes': Recipe.get_all()
    }
    return render_template('home.html', **context)

    
@app.route('/user/login_registration')         
def login_registration():
    return render_template('login_registration.html')

@app.route('/user/register', methods=['POST'])
def register():
    #validate registration form
    if not User.validate(request.form):
        return redirect('/user/login_registration')
    #hash password
    hash_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
    **request.form,
    'password': hash_pw
    }
    #set user id to create instance
    id = User.create(data)
    #session user_id 
    session['user_id'] = id
    #redirect to dashboard 
    return redirect('/user/dashboard')

#READ
#route to login
#method = post
@app.route('/user/login', methods=['POST'])
def login():
    #validate login credentials
    if not User.validate_login(request.form):
        return redirect('/user/login_registration')
#redirect to dashboard if validated
    return redirect('/user/dashboard')

#route to dashboard
@app.route('/user/dashboard')
@login_required
def dashboard():
    data ={
        'id': session['user_id'] #retreiving id from session
    }
    context ={
        'user' : User.get_one(data),
        'all_recipes': Recipe.get_all()
    }
    return render_template('dashboard.html', **context)


#'delete
#logout out of session 
@app.route('/user/logout')
@login_required
def logout():
    
    # if 'user_id' not in session:
    #     flash("you need to login first")
    # else:
    #clears session when logged out
    session.clear()
    #redirect to homepage
    return redirect('/')




