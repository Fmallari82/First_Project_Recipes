from flask import Flask, render_template, request, redirect, session, flash
from flask_app.controllers import controllers_users, controllers_routes, controllers_recipes
from flask_app import app


if __name__=="__main__":   
    app.run(debug=True)    