from flask import request, make_response, jsonify
from . import auth
from .. models import User, BlacklistToken
import re
from flask_bcrypt import Bcrypt

@auth.route('/api/v1/auth/register', methods=['POST'])
def create_user_account():
    """Register a new user"""

    username1 = request.data.get('username')
    email1 = request.data.get('email')
    password1 = request.data.get('password')
    confirm_password1 = request.data.get('confirm_password')

    users = User.get_all()
    all_input = username1 and email1 and password1 and confirm_password1

    if isinstance(username1, int) or isinstance(email1, int) or isinstance(password1, int) or isinstance(confirm_password1, int):
        return jsonify({'message': "Invalid input, kindly use valid strings"}), 400

    if all_input:
        """ Remove whitespaces before and after input """

        username = str(username1.strip(' '))
        email = str(email1.strip(' '))
        password = str(password1.strip(' '))
        confirm_password = str(confirm_password1.strip(' '))

        existing_username = [
            u for u in users if u.username.lower() == username.lower()]
        existing_email = [e for e in users if e.email.lower() == email.lower()]
        all_stripped_input = username and email and password and confirm_password

    if not all_input:
        response = jsonify(
            {'message': "Invalid input, kindly fill in all required input"}), 400

    elif not all_stripped_input:
        response = jsonify({'message': "Input empty fields"}), 400

    elif not username.isalpha():
        response = jsonify(
            {'message': "kindly use only letters for a username"}), 400

    elif len(username) < 3:
        response = jsonify(
            {'message': "Kindly set a username of more than 3 letters"}), 400

    elif not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*.,#?&])[A-Za-z\d$@$!.,%*#?&]{6,}$", password):
        response = jsonify(
            {'message': "Kindly set a strong password. Ensure to use aminimum of 6 characters that contains at least 1 letter, one number and one special character"}), 400

    elif password != confirm_password:
        response = jsonify({'message': "Unmatched passwords"}), 400

    elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        response = jsonify({'message': "Invalid email address"}), 400
        
    elif existing_username:
        response = jsonify(
            {'message': "The username is already registered, kindly chose a different one"}), 409

    elif existing_email:
        response = jsonify(
            {'message': "The email is already registered, kindly chose a different one"}), 409

    else:

        user = User(username=username, email=email, password=password)
        user.save()
        response = jsonify({'message': "User Registered successfully"}), 201

    return response


@auth.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    """Log in a user using username and password provided, and generate access token """
    username1 = request.data.get('username')
    password1 = request.data.get('password')

    all_credentials = username1 and password1
    int_input = isinstance(username1, int) or isinstance(password1, int)

    if int_input or not all_credentials:
        return jsonify({'message': "Invalid input, fill in all required inputs, and kindly use strings"}), 400

    if all_credentials:
        username = str(username1.strip(' '))
        password = str(password1.strip(' '))
        user = User.query.filter_by(username=request.data['username']).first()

    if user:
        correct_pwd = user.password_is_valid(request.data['password'])
        access_token = user.generate_token(user.id)

    if not username and password:
        response = jsonify({'message': "Fill in the empty fields"}), 400

    elif not user:
        response = jsonify({'message': "Invalid username", 'status_code': 204})

    elif user and not correct_pwd:
        response = jsonify({'message': "Wrong password entered"}), 401

    else:
        response = make_response(jsonify({
            'Message': 'Successfully Logged in',
            'access_token': access_token.decode()}), 200)
    return response


@auth.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():
    """Logout the user by blacklisting access token"""

    token = User.validate_token()

    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        response = jsonify(
            {'message': 'Invalid token, Login to obtain a new token'}), 401

    else:
        token = BlacklistToken(token=token['access_token'])
        token.save()
        response = jsonify({'message': 'Successfully Logged Out'}), 200

    return response


@auth.route('/api/v1/auth/update_password', methods=['PUT'])
def update_password():
    """ change password by a logged in user """

    email1 = request.data.get('email')
    current_password1 = request.data.get('current_password')
    new_password1 = request.data.get('new_password')
    confirm_password1 = request.data.get('confirm_password')

    all_input = email1 and current_password1 and new_password1 and confirm_password1

    token = User.validate_token()

    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        return jsonify({'message': 'Invalid token, Login to obtain a new token'}), 401

    if isinstance(email1, int) or isinstance(current_password1, int) or isinstance(new_password1, int) or isinstance(confirm_password1, int):
        return jsonify({'message': "Invalid input, kindly use valid strings"}), 400

    if all_input:

        email = str(email1.strip(' '))
        current_password = str(current_password1.strip(' '))
        new_password = str(new_password1.strip(' '))
        confirm_password = str(confirm_password1.strip(' '))

        user = User.query.filter_by(email=request.data['email']).first()

        all_stripped_input = email and current_password and new_password and confirm_password
        valid_user = user and user.password_is_valid(
            request.data['current_password'])

    if not all_input:
        response = jsonify(
            {'message': "Invalid input, kindly fill in all required input"}), 400

    elif not all_stripped_input:
        response = jsonify({'error': 'Input Empty Fields'}), 400

    elif not user:
        response = jsonify({'error': "Invalid Email", 'status_code': 204})

    elif not valid_user:
        response = jsonify({'error': "Wrong password"}), 400

    elif new_password != confirm_password:
        response = jsonify({'message': "Passwords not matching"}), 400

    else:
        new_hashed_password = Bcrypt().generate_password_hash(new_password).decode('utf-8')
        user.password = new_hashed_password

        user.save()
        response = jsonify({'message': "Password updated successfully"}), 200

    return response


@auth.route('/api/v1/auth/reset_password', methods=['PUT'])
def reset_password():
    """ Reset password using email"""

    email1 = request.data.get('email')

    if isinstance(email1, int):
        return jsonify({'message': "Invalid input, kindly use valid strings"}), 400

    if email1:

        email = str(email1.strip(' '))

        reg_email = User.query.filter_by(email=email).first()

    if not email1:
        response = jsonify({'message': "Invalid input, kindly fill in all required input"}), 400

    elif not email:
        response = jsonify({'error': 'Input Empty Fields'}), 400

    elif not reg_email:
        response = jsonify({'error': "Email error, kindly ensure the indicated email is correct", 'status_code': 204})

    else:

        import smtplib
        import uuid

        gmail_user = "kezzyangiro@gmail.com"
        gmail_pwd = "k0717658539h"
        TO = email
        SUBJECT = "WeConnect Password Reset"

        new_pwd = uuid.uuid4()
        TEXT = f"Hello, you have successfully reset your Weconnect password. Your new password is:   {str(new_pwd)}   You can login using this new password, click on and use change password functionality to update to a new password of your choice."
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.ehlo()
        
        server.login(gmail_user, gmail_pwd)
        BODY = '\r\n'.join(['To: %s' % TO,
                'From: %s' % gmail_user,
                'Subject: %s' % SUBJECT,
                '', TEXT])

        server.sendmail(gmail_user, [TO], BODY)
        

        new_hashed_password = Bcrypt().generate_password_hash(str(new_pwd)).decode('utf-8')
        reg_email.password = new_hashed_password

        reg_email.save()
        response = jsonify({'message': "Password reset successfully, check your email for your new password"}), 200

    return response
