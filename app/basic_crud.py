from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
print("base_crud_app")


@app.route('/login/', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        name = 'Dork'
        password = '1234'

        user_name = request.form.get('name')
        user_password = request.form.get('password')

        print(user_name, user_password)

        if name == str(user_name) and password == str(user_password): 
            return render_template('index.html', name=user_name)
        else:
            return jsonify({'message': 'Wrong username and password'})

    else: 
        return render_template('login.html')
