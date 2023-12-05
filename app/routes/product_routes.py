from flask import Blueprint, request, render_template, url_for, redirect, jsonify

from app.utilities.mysql_connection_utility import get_connection, close_connection, connect_to_mysql

product_routes = Blueprint('product_routes', __name__)

table = 'products'

connection_pool = connect_to_mysql()

@product_routes.route('/create', methods=['GET', 'POST'])
def create_product(): 
    connection = get_connection(connection_pool)
    try:
        if request.method == 'POST':
            product_name: str = request.form.get('product_name')
            product_type: str = request.form.get('product_type')
            product_price: int = request.form.get('product_price')
            in_stock: bool = request.form.get('in_stock')

            cursor = connection.cursor()
            query = f"INSERT INTO `{table}` (`product_name`, `product_type`, `product_price`, `in_stock`) VALUES ('{product_name}', '{product_type}', '{product_price}', '{in_stock}')"
            cursor.execute(query)
            connection.commit()

            return jsonify({'message': 'Product Added Successfully'})
        else: 
            return render_template('index.html')
    except Exception as err:
        return str(err)
    finally:
        close_connection(connection)
    
@product_routes.route('/get-all-product', methods=['GET'])
def get_all_product():
    print('get')
    return jsonify({'message': 'get requested hit'})


@product_routes.route('/get-product', methods=['GET'])
def get_product_by_id():
    print('get id')
    return jsonify({'message': 'get requested hit'})

@product_routes.route('/update', methods=['POST'])
def update_product():
    print('update')

@product_routes.route('/delete', methods=['POST'])
def delete_product():
    print('delete')