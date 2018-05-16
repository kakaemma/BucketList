from flask import jsonify
from validate_email import validate_email
from models.users import UserModal


class Authenticate(object):

    """ 
    This takes care of all user operations 
    from registration to login
    """

    @staticmethod
    def register(name, email, password):
        if not name or not email or not password:
            response = jsonify({'Error': 'Missing value(s)'})
            response.status_code = 406
            return response

        if not len(name) >= 3:
            response = jsonify({'Error': 'name too short'})
            response.status_code = 422
            return response

        if not len(password) > 6:
            response = jsonify({'Error': 'Password too short'})
            response.status_code = 422
            return response

        if not validate_email(email):
            response = jsonify({'Error': 'Invalid Email address'})
            response.status_code = 422
            return response

        check_user = UserModal.check_user_email(email)
        if email == check_user:
            response = jsonify({'Conflict': 'Email already exists'})
            response.status_code = 409
            return response

        if email != check_user:
            new_user = UserModal(name, email, password)
            new_user.add_user()
            response = jsonify({'message': 'Successfully registered'})
            response.status_code = 201
            return response



    @staticmethod
    def login(email, password):
        if not email or not password:
            response = jsonify({'Error': 'Missing login credentialss'})
            response.status_code = 422
            return response

        if not validate_email(email):
            response = jsonify({'Error': 'Invalid Email address'})
            response.status_code = 422
            return response

        if not len(password) >6:
            response = jsonify({'Error': 'Password is too short.'})
            response.status_code = 422
            return response

        login_user = UserModal.check_user(email, password)

        if not login_user:
            response = jsonify({'Error': 'Invalid credentials'})
            response.status_code = 401
            return response

        response = jsonify({
                'Status': 'Successfully logged in',
                'id': login_user
            })
        response.status_code = 200
        return response

    @staticmethod
    def reset_password(email, old_pass, new_pass):
        if not email or not new_pass or not old_pass:
            response = jsonify({
                'Error': 'Missing email or password'
            })
            response.status_code = 422
            return response

        check_for_user_by_email = UserModal.check_user_return_pass(email)

        if not check_for_user_by_email or not \
                        old_pass == check_for_user_by_email:
            response = jsonify({
                'Error': 'Email and password do not exist'
            })
            response.status_code = 403
            return response

        check_for_password = UserModal.check_user(email, old_pass)
        if not check_for_password:
            response = jsonify({'Error': 'Old password is wrong'})
            response.status_code = 401
            return response

        if old_pass == new_pass:
            response = jsonify({
                'Error': 'Old password and new password are the same'
            })
            response.status_code = 401
            return response

        reset_password = UserModal.reset_user_pass(email, new_pass)
        if not reset_password:
            response = jsonify({'Error': 'Password change failed'})
            response.status_code = 401
            return  response

        response = jsonify({'Success': 'Password reset successfully'})
        response.status_code = 200
        return response
