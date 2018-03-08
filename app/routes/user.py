from flask import request, make_response, jsonify
from . import bs
from .. models import User

@bs.route('/')
@bs.route('/api/v1/auth/register', methods=['POST'])
def create_user_account():
    # import pdb; pdb.set_trace()

    username = str(request.data.get('username'))
    email = str(request.data.get('email'))
    password = str(request.data.get('password'))
    confirm_password = str(request.data.get('confirm_password'))

    if username and email and password and confirm_password:
        
        if password != confirm_password:
            response = make_response(jsonify({
                'message': "Unmatched passwords"
                }
            ), 403)
            return response

        elif email:
            response = make_response(jsonify({
                'message': "Invalid email address"
                }
            ), 403)
            return response

        elif [email==users.email for users in User.user]:
            response = make_response(jsonify({
                'message': "The email address already exist use a different ones"
                }
            ), 403)
            return response

        elif [username==users.username for users in User.user]:
            response = make_response(jsonify({
                'message': "The username already exist use a different ones"
                }
            ), 40)
            return response

        else:
            user= User(username=username, email=email, password=password)
            user.save(user)
            response =make_response(
                jsonify({
                    'message':'User Created successfully'
                    
                    }), 201)
            return response
    else:
        response = make_response(jsonify({
                'message': "Input empty fields"
                }
        ), 403)
        return response
