from flask import request, make_response, jsonify, session
from . import bs
from .. models import User
import re

@bs.route('/api/v1/auth/register', methods=['POST'])
def create_user_account():
    """Endpoint to create a user"""
    # import pdb; pdb.set_trace()

    username = str(request.data.get('username').strip(' '))
    email = str(request.data.get('email').strip(' '))
    password = str(request.data.get('password').strip(' '))
    confirm_password = str(request.data.get('confirm_password').strip(' '))

    

    if username and email and password and confirm_password:
        """Checks is all fields have been filled in"""
        
        if password != confirm_password:
            response = make_response(jsonify({
                'message': "Unmatched passwords"
                }
            ), 400)
            return response
        
        elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            """Email Validation"""
            response = make_response(jsonify({
                'message': "Invalid email address"
                }
            ), 400)
            return response

        else:
            for user in User.user:
                if user.username == username:
                    response =make_response(
                    jsonify({
                        'message':'The username already exists'
                        
                        }), 409)
                    return response

                if user.email == email:
                    response =make_response(
                    jsonify({
                        'message':'The email address already exists'
                        
                        }), 409)
                    return response

                    
        user= User(username=username, email=email, password=password)
        user.save(user)
        response =make_response(
            jsonify({
                'message':'User Created successfully'
                
                }), 201)
        return response
    
    response = make_response(jsonify({
            'message': "Input empty fields"
            }
    ), 400)
    return response

@bs.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    """Api to log in a user using username and password provided """ 
    username = str(request.data.get('username'))
    password = str(request.data.get('password'))
    responce = ''
    if username and password:
        for myuser in User.user:
            if username==myuser.username and password==myuser.password:
                """Add Logged in user into login session"""

                session["username"]=username
                responce = make_response(
                    jsonify({
                        'message':'User Logged in successfully'
                    }),200)
                return responce
                

            responce1 = make_response(
                jsonify({
                    'message':'Wrong username or password entered'
                }),404)

            return responce1

        responce = make_response(
                jsonify({
                    'message':'User not found, kindly register first'
                }),404)

        return responce
    
    responce = make_response(
        jsonify({
            'message':'Empty username or password field'
        }),400)

    return responce

@bs.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():
    """this endpoint will logout the user by removing the username from the session"""

    if session.get("username") is not None:
        session.pop("username", None)
        return jsonify({"message": "User Logged out successfully"})
    

    responce = make_response(
    jsonify({
        'message':'You are not logged in'
    }),400)

    return responce


@bs.route('/api/v1/auth/reset_password', methods=['PUT'])
def reset_password():
    """This endpoint enables a registered user to edit password"""
    username = str(request.data.get('username'))
    current_password = str(request.data.get('current_password')) 
    new_password = str(request.data.get('new_password').strip(' ')) 
    confirm_password = str(request.data.get('confirm_password').strip(' ')) 

    if username and current_password and new_password and confirm_password: 

        for myuser in User.user:
            if myuser.username == username and myuser.password == current_password:
              
                if new_password != confirm_password:
                    res = make_response(jsonify({
                            'message':'Passords not matching'
                        }), 400)
                    return res

                myuser.password=new_password

                resp= make_response(jsonify({
                            'message':'Password reset successfully'
                        }), 200)
                return resp

            respon = make_response(jsonify({
                            'message':'Username or password error'
                        }), 404)
            return respon

        respons = make_response(jsonify({
                            'message':'No available user'
                        }), 404)
        return respons

    response = make_response(jsonify({
                            'message':'Input Empty Fields'
                        }), 400)
    return response

         
