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

    all_input = username1 and email1 and password1 and confirm_password1
    int_input = isinstance(username1, int) or isinstance(email1, int) or isinstance(password1, int) or isinstance(confirm_password1, int)

    if int_input or not all_input:
        return jsonify({'Error': "Invalid input, fill in all required input and kindly use valid strings"}), 400
        
    username = str(username1.strip(' '))
    email = str(email1.strip(' '))
    password = str(password1.strip(' '))
    confirm_password = str(confirm_password1.strip(' '))
    
    all_stripped_input = username and email and password and confirm_password

    if not all_stripped_input:
        response = jsonify({'Error': "Input empty fields"}), 400

    elif not username.isalpha():
        response = jsonify(
            {'Error': "kindly use only letters for a username"}), 400

    elif len(username) < 3:
        response = jsonify(
            {'Error': "Kindly set a username of more than 3 letters"}), 400

    elif not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*.,#?&])[A-Za-z\d$@$!.,%*#?&]{6,}$", password):
        response = jsonify(
            {'Error': "Kindly set a strong password. Ensure to use aminimum of 6 characters that contains at least 1 letter, one number and one special character"}), 400

    elif password != confirm_password:
        response = jsonify({'Error': "Unmatched passwords"}), 400

    elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        response = jsonify({'Error': "Invalid email address, kindly use the right email format i.e abc@def.com"}), 400
        
    elif [u for u in User.get_all() if u.username.lower() == username.lower()]:
        response = jsonify({'Error': "The username is already registered, kindly chose a different one"}), 409

    elif [e for e in User.get_all() if e.email.lower() == email.lower()]:
        response = jsonify({'Error': "The email is already registered, kindly chose a different one"}), 409

    else:

        user = User(username=username, email=email, password=password)
        user.save()
        response = jsonify({'Success': "User Registered successfully"}), 201

    return response


@auth.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    """Log in a user using username and password provided, and generate access token """
    username1 = request.data.get('username')
    password1 = request.data.get('password')

    all_credentials = username1 and password1
    int_input = isinstance(username1, int) or isinstance(password1, int)

    if int_input or not all_credentials:
        return jsonify({'Error': "Invalid input, fill in all required inputs, and kindly use strings"}), 400

    username = str(username1.strip(' '))
    password = str(password1.strip(' '))
    

    if not username or not password:
        return jsonify({'Error': "Fill in the empty fields"}), 400

    user = User.query.filter_by(username=request.data['username']).first()

    if not user:
        return jsonify({'Error': "User not found, kindly use correct username", 'status_code': 204})

    correct_pwd = user.password_is_valid(request.data['password'])
    access_token = user.generate_token(user.id)

    if not correct_pwd:
        response = jsonify({'Error': "Wrong password entered"}), 401

    else:
        response = make_response(jsonify({
            'Success': 'Successfully Logged in',
            'access_token': access_token.decode()}), 200)
    return response


@auth.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():
    """Logout the user by blacklisting access token"""

    token = User.validate_token()

    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        response = jsonify({'Error': 'Invalid token, Login to obtain a new token'}), 401

    else:
        token = BlacklistToken(token=token['access_token'])
        token.save()
        response = jsonify({'Success': 'Successfully Logged Out'}), 200

    return response


@auth.route('/api/v1/auth/update_password', methods=['PUT'])
def update_password():
    """ change password by a logged in user """

    email1 = request.data.get('email')
    current_password1 = request.data.get('current_password')
    new_password1 = request.data.get('new_password')
    confirm_password1 = request.data.get('confirm_password')

    all_input = email1 and current_password1 and new_password1 and confirm_password1
    int_input = isinstance(email1, int) or isinstance(current_password1, int) or isinstance(new_password1, int) or isinstance(confirm_password1, int)

    token = User.validate_token()

    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        return jsonify({'Error': 'Invalid token, Login to obtain a new token'}), 401

    if int_input or not all_input:
        return jsonify(
            {'Error': "Invalid input, fill in all required input and kindly use valid strings"}), 400

    email = str(email1.strip(' '))
    current_password = str(current_password1.strip(' '))
    new_password = str(new_password1.strip(' '))
    confirm_password = str(confirm_password1.strip(' '))

    all_stripped_input = email and current_password and new_password and confirm_password

    if not all_stripped_input:
        return jsonify({'Error': 'Input Empty Fields'}), 400

    user = User.query.filter_by(email=request.data['email']).first()

    if not user:
        response = jsonify({'Error': "Unrecognised email, kindly ensure to use the email you registered with", 'status_code': 204})

    elif not user.password_is_valid(request.data['current_password']):
        response = jsonify({'Error': "Wrong current password"}), 400

    elif not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*.,#?&])[A-Za-z\d$@$!.,%*#?&]{6,}$", new_password):
        response = jsonify({'Error': "Kindly set a strong password. Ensure to use aminimum of 6 characters that contains at least 1 letter, one number and one special character"}), 400

    elif new_password != confirm_password:
        response = jsonify({'Error': "New password not matching with confirm password"}), 400

    else:
        new_hashed_password = Bcrypt().generate_password_hash(new_password).decode('utf-8')
        user.password = new_hashed_password

        user.save()
        response = jsonify({'Success': "Password updated successfully"}), 200

    return response


@auth.route('/api/v1/auth/reset_password', methods=['PUT', 'POST'])
def reset_password():

    if request.method == "POST":
        """ With a valid email, send a token to be used for password reset"""

        email1 = request.data.get('email')

        if not email1 or isinstance(email1, int):
            return jsonify({'Error': "Kindly fill in an email in a string format"}), 400

        email = str(email1.strip(' '))

        if not email or not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return jsonify({'Error': 'Fill in a valid email address and kindly use the right email format i.e abc@def.com'}), 400

        reg_email = User.query.filter_by(email=email).first()

        if not reg_email:
            response = jsonify({'Error': "Unrecognised email, kindly ensure to use the email you registered with", 'status_code': 204})

        else:

            import smtplib

            gmail_user = "kezzyangiro@gmail.com"
            gmail_pwd = "k0717658539h"
            TO = email
            SUBJECT = "WeConnect Password Reset"

            reset_token = reg_email.generate_token(reg_email.id)

            TEXT = f"Hello, kindly use the below token to reset your password {reset_token.decode()}   Copy it and paste it on your authorization header and fill in your new password. Kindly note that the token will expire in the next 15 minutes from the moment you receive this mail. If it does expire, resend a reset request and use the new token"
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.ehlo()
            
            server.login(gmail_user, gmail_pwd)
            BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_user,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])

            server.sendmail(gmail_user, [TO], BODY)
            response = jsonify({'Success': "Kindly check your email for a token to reset your password"}), 200

        return response

    else:
        """ Reset password using token received on email """
        
        token = User.validate_token()

        if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
            return jsonify({'Error': 'Invalid token, kindly use the right token sent to your email for password reset'}), 401
          
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not new_password or not confirm_password or isinstance(new_password, int) or isinstance(confirm_password, int):
            return jsonify({'Error': "Kindly fill in all required information (new_password and confirm_password)"}), 400

        new_pwd = new_password
        confirm_pwd = confirm_password

        if not new_pwd or not confirm_pwd:
            response = jsonify({'Error':"Kindly fill in a valid input, avoid using empty spaces as input"})

        elif not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*.,#?&])[A-Za-z\d$@$!.,%*#?&]{6,}$", new_pwd):
            response = jsonify({'Error': "Kindly set a strong password. Ensure to use aminimum of 6 characters that contains at least 1 letter, one number and one special character"}), 400

        elif new_pwd != confirm_pwd:
            response = jsonify({'Error': "Unmatched passwords"}), 400

        else:
            user = User.query.filter_by(id=token['user_id']).first()
            new_hashed_password = Bcrypt().generate_password_hash(str(new_pwd)).decode('utf-8')
            user.password = new_hashed_password

            user.save()
            response = jsonify({'Success': "Password reset successfully"}), 200
        
        return response

            