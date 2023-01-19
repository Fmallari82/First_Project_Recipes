import base64
from flask import flash, render_template, request, redirect, session, url_for
from flask_app import app

from flask_app.controllers.controllers_users import dashboard, login_required  # ...server.py
from flask_app.models.model_recipe import Recipe
from flask_app.models.model_user import User
from flask_app.models.model_image import Image
import urllib.request
import os
from werkzeug.utils import secure_filename
import requests

UPLOAD_FOLDER = 'flask_app/static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

location = input(UPLOAD_FOLDER)

@app.route("/upload", methods = ['POST', 'GET'])
def upload():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image successfully uploaded and displayed below')
            return render_template('recipe_new.html', filename=filename)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif, pdf')
            return redirect('/recipe/add')
    data = {
        **request.form
    }
    Image.create(data)
    return redirect('/recipe/add')

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('flask_app/static', filename='uploads/' + filename), code=301 )


#Create
@app.route('/recipe/add')
@login_required
def recipe_add():
    if not User.get_one({'id': session['user_id']}):
        return redirect('/user/login_registraion')
    context ={
        'recipe': Recipe.get_one({'id':id}),
        'user': User.get_one({'id': session['user_id']}),
        'image': Image.get_one({'id': id}),
        'images': Image.get_all()
    }
    return render_template('recipe_new.html', **context)


@app.route('/recipe/create', methods=['Post'])
def recipe_create():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/add')
    data = {
        **request.form
    }
    data['user_id'] = session['user_id']
    Recipe.create(data)
    return redirect('/user/dashboard')

#------------------------READ-----------------------------------------------------------
@app.route('/recipe/show_all')         
def show_all_recipes():
    data ={
        'id': session['user_id'],
        **request.form

    }
    context ={
        'user' : User.get_one(data),
        'all_recipes': Recipe.get_all(),
        'recipe' : Recipe.get_one(data)
    }
    return render_template('all_recipes.html',**context)


@app.route('/recipe/<int:id>/show')
def user_show(id):
    context ={
        'recipe': Recipe.get_one({'id':id}),
        'user': User.get_one({'id': session['user_id']})
    }
    return render_template('users_recipes.html', **context)

@app.route('/recipe/<int:id>/edit')
def recipe_edit(id):
    return render_template('recipe_edit.html',recipe= Recipe.get_one({'id': id}))

#UPDATE
@app.route('/recipe/<int:id>/update', methods=['Post'])
def recipe_update(id):
    if not Recipe.validate_recipe_edit(request.form):
        return redirect(f'/recipe/{id}/edit')
    data = {
        **request.form,
        'id':id
    }
    if 'is_under' in data:
        data['is_under'] = 1
    else:
        data['is_under'] = 0
    Recipe.update_one(data)
    return redirect('/user/dashboard')

#DELETE
@app.route('/recipe/<int:id>/delete')
def user_delete(id):
    
    Recipe.delete_one({'id':id})
    return redirect('/user/dashboard')


# @app.route('/recipe/add', methods=['POST'])
# @login_required
# def upload_image():
#     if 'image' not in request.files:
#         flash('No file part')
#         return redirect ('/recipe/add')
#     file = request.files ['image']
#     if file.filename == '':
#         flash ('No image selected for uploading')
#         return redirect('/recipe/add')
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return render_template('recip_new.html', filename=filename)
#     else:
#         flash('Allowed image types are - png, jpg, jpeg, gif')
#         return redirect ('/recipe/add')

