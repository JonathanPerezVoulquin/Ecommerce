from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app
from shop.products.models import Addproduct
from shop.products.routes import brands, categories

def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/addcart', methods=['POST'])
def addCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        colors = request.form.get('colors')       
        product = Addproduct.query.filter_by(id=product_id).first()
        
        if product_id and quantity and colors and request.method == 'POST':
            # Check if requested quantity exceeds stock
            if quantity > product.stock: 
                flash('No stock')  # Show flash message if no stock
                return redirect(request.referrer)  # Redirect back to the previous page
            
            dictItems = {product_id: {
                'name': product.name, 
                'price': product.price,
                'discount': product.discount,
                'color': colors, 
                'quantity': quantity, 
                'image': product.image_1, 
                'colors': product.colors,
                'stock': product.stock
            }}

            # Add another item to the list
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    # For increased quantity items
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            new_quantity = item['quantity'] + quantity

                            # Check if new quantity exceeds stock
                            if new_quantity > item['stock']:
                                flash(f'No hay suficiente stock para "{product.name}".', 'warning')
                                return redirect(request.referrer)

                            item['quantity'] = new_quantity
                            print('Producto ya en el carrito, cantidad actualizada')
                else:
                    # Add the product to the cart if it is not there
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], dictItems)
                    print('Producto agregado al carrito')
                    return redirect(request.referrer)
            else:
                # Create a new cart if it does not exist
                session['Shoppingcart'] = dictItems
                print('Nuevo carrito creado')
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carts/')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    
    subtotal = 0
    total = 0
    
    for k, product in session['Shoppingcart'].items():
        discount = (product['discount'] / 100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        iva = ('%.2f' % (.21 * float(subtotal)))  # Tax in Argentina (21%)
        total = float('%.2f' % (1.21 * subtotal))
        
    return render_template('products/carts.html', iva=iva, total=total, subtotal=subtotal, brands=brands(), categories=categories())

@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/deleteitem/<int:id>')
def deleteItem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
        return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
