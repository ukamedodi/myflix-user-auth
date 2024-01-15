from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from pymongo import MongoClient
import certifi
import ssl

app = Flask(__name__)

# mongo_client = MongoClient('mongodb+srv://ukamedodi:superman18@myflix.wasdykw.mongodb.net/?retryWrites=true&w=majority')
# database = mongo_client['userData']
# users_collection = database['users']



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle the form data for login
        data = {
            'email': request.form['email'],
            'password': request.form['password']
        }

        # response = users_collection.find_one({'email': data['email']})
        response  = 1
      
        if response != None:
            # Successful login, redirect to the home page
            # You may want to handle the session ID here
            return redirect("http://34.130.249.80/:5010/")
        else:
            # Failed login, you might want to handle error messages here
            return render_template('login.html', error_message="Invalid credentials")

    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        confirmPassword = request.form['confirmPassword']
        # Handle the form data for signup
        data = {
            'firstName': request.form['firstName'],
            'lastName': request.form['lastName'],
            'email': request.form['email'],
            'password': request.form['password']
        }

        if data['password'] != confirmPassword:
            return render_template('signup.html', error_message="Passwords do not match")
        else:
            # users_collection.insert_one(data)
            return redirect(url_for('login'))

    else:
        return render_template('signup.html')
    
    
if __name__ == '__main__':
    app.run(host = "0.0.0.0",debug=True)
