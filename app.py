from flask import Flask, render_template, request, jsonify
import random
import string
import logging

# Disable Flask's default logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)

def generate_secure_password(length=64):
    # Define the character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"

    # Ensure the password contains at least one character from each set
    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(special_chars)
    ]
    
    # Combine all character sets for the rest of the password
    all_chars = uppercase + lowercase + digits + special_chars

    # Generate the rest of the password randomly
    password += random.choices(all_chars, k=length - len(password))

    # Shuffle to avoid predictable patterns
    random.shuffle(password)

    # Return as a string
    return ''.join(password)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    length = int(request.form.get('length', 64))
    if length < 4:  # Ensure minimum length to accommodate all character sets
        length = 4
    password = generate_secure_password(length)
    return jsonify({'password': password})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
