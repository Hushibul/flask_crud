from flask import Blueprint, request, render_template, url_for, redirect

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        name: str = 'Dork'
        password: str = '1234'

        user_name: str = request.form.get('name')
        user_password: str = request.form.get('password')

        if name == user_name and password == user_password: 
            return render_template('index.html', name=user_name)
        else:
            return redirect(url_for('auth_routes.register', message="User doesn't exist! Please register."))

    else: 
        return render_template('login.html')
    
@auth_routes.route('/register')
def register():
    message = request.args.get('message', '')
    return render_template('register.html', message=message)