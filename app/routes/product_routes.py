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

            if not product_name:
                return jsonify({'message': 'product_name is required'})
            elif not product_type:
                return jsonify({'message': 'product_type is required'})
            elif not product_price: 
                return jsonify({'message': 'product_price is required'})

            cursor = connection.cursor(buffered=True)
            query = f"SELECT * FROM `{table}` WHERE `product_name` = '{product_name}'"
            cursor.execute(query)
            existing_product =  cursor.fetchone()
            connection.commit()

            if existing_product:
                return jsonify({'message': 'Product already exists'})
            else:
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
    connection = get_connection(connection_pool)
    cursor = connection.cursor(buffered=True)
    query = f"SELECT * FROM `{table}`"
    cursor.execute(query)
    result =  cursor.fetchall()
    connection.commit()

    print('result', result)

    return render_template('index.html', data = result)


@product_routes.route('/search', methods=['GET'])
def search_products():
    try:
        # Extract query parameters from the request
        product_name = request.args.get('product_name')
        product_type = request.args.get('product_type')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')

        # Create the base query
        query = f"SELECT * FROM `{table}` WHERE 1=1"

        # Add conditions based on the provided parameters
        if product_name:
            query += f" AND `product_name` = '{product_name}'"
        if product_type:
            query += f" AND `product_type` = '{product_type}'"
        if min_price:
            query += f" AND `product_price` >= {min_price}"
        if max_price:
            query += f" AND `product_price` <= {max_price}"

        # Execute the query
        connection = get_connection(connection_pool)
        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        
        # Fetch the results
        results = cursor.fetchall()

        return jsonify({'products': results})

    except Exception as err:
        return jsonify({'error': str(err)}), 500

    finally:
        close_connection(connection)

@product_routes.route('/update/<int:product_id>', methods=['POST'])
def update_product(product_id):
    try:
        # Extract data from the request form
        product_name = request.form.get('product_name')
        product_type = request.form.get('product_type')
        product_price = request.form.get('product_price')
        in_stock = request.form.get('in_stock')

        # Convert product_price to int (if necessary)
        product_price = int(product_price) if product_price is not None else None

        # Convert in_stock to bool (if necessary)
        in_stock = in_stock.lower() == 'true' if in_stock is not None else None

        connection = get_connection(connection_pool)
        cursor = connection.cursor(buffered=True)

        query = (
            f"UPDATE `{table}` SET "
            f"`product_name` = %s, `product_type` = %s, `product_price` = %s, `in_stock` = %s "
            f"WHERE `id` = %s"
        )

        cursor.execute(query, (product_name, product_type, product_price, in_stock, product_id))
        connection.commit()

        return jsonify({'message': 'Product Updated'})
    
    except Exception as err:
        # Return a JSON response with the error message
        return jsonify({'error': str(err)}), 500
    finally:
        close_connection(connection)


@product_routes.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    try:
        if product_id:
            connection = get_connection(connection_pool)
            cursor = connection.cursor(buffered=True)
            query = f"DELETE FROM `{table}` WHERE `id` = %s"
            cursor.execute(query, (product_id,))
            connection.commit()

            return jsonify({'message': 'Product Deleted'})
        else: 
            return jsonify({'message': 'Product does not exist'})
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        close_connection(connection)
