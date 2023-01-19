
from flask import Flask, render_template, request, redirect, session
from flask_app import app
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe

@app.route('/')         
def index():
    return render_template('index.html')
