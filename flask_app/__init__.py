from flask import Flask, flash, session
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "95591817-8b5c-4a04-96bc-820304c53360"
bcrypt = Bcrypt(app)

DATABASE = 'recipes_schema'
