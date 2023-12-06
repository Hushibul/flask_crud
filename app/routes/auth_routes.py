from flask import Blueprint, request, render_template, url_for, redirect, jsonify
from passlib.hash import sha256_crypt

from app.utilities.mysql_connection_utility import get_connection, close_connection, connect_to_mysql

auth_routes = Blueprint('auth_routes', __name__)

table = 'registered_users'

connection_pool = connect_to_mysql()

def check_registered_user(email, connection):
   try:      
        cursor = connection.cursor(buffered=True)

        query = f"SELECT * FROM `{table}` WHERE `email` = '{email}'"
        cursor.execute(query)
        result = cursor.fetchone()
        return result
   except Exception as err:
        return err
   finally:
        close_connection(connection)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login(): 
    try:
        connection = get_connection(connection_pool)
        if request.method == 'POST':
            email: str = request.form.get('email')
            password: str = request.form.get('password')

            if not email: 
                return jsonify({'message': 'Email is required'})
            elif not password: 
                return jsonify({'message': 'Password is required'})

            existing_user = check_registered_user(email, connection)
            
            if existing_user:
               is_password_true = sha256_crypt.verify(password, existing_user[3])
               
               if is_password_true:
                   return redirect('/product/get-all-product')
               else:
                   return jsonify({'message': 'Invalid password'})
            else:
                return jsonify({'message': 'User not found'})
        else: 
            return render_template('login.html')
    except Exception as err:
        return str(err)
    finally:
        close_connection(connection)

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    try: 
        connection = get_connection(connection_pool)
        if request.method == 'POST':
            name: str = request.form.get('name')
            email: str = request.form.get('email')
            password: str = request.form.get('password')

            if not name:
                return jsonify({'message': 'Name is required'})
            elif not email:
                return jsonify({'message': 'Email is required'})
            elif not password:
                return jsonify({'message': 'Password is required'})
            
            existing_user = check_registered_user(email, connection)
            if existing_user:
                return jsonify({'message': 'User already exists. Try out a new email'})
            else: 
                hashedPassword = sha256_crypt.encrypt(password)

                cursor = connection.cursor(buffered=True)
                query = f"INSERT INTO `{table}` (`name`, `email`, `password`) VALUES ('{name}', '{email}', '{hashedPassword}')"
                cursor.execute(query)
                connection.commit()
                        
            return jsonify({'message': 'Registration successful'})
        
        else:
            message = request.args.get('message', '')
            return render_template('register.html', message=message)
    
    except Exception as err:
        return str(err) 
    finally:
        close_connection(connection)