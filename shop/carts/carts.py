from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app
from shop.products.models import Addproduct
from shop.products.routes import brands, categories
def MagerDicts(dict1, dict2):
    if isinstance(dict1,list) and isinstance(dict2,list):
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
            dictItems = {product_id:{'name': product.name, 'price': product.price, 'discount': product.discount,
            'color':colors, 'quantity': quantity, 'image': product.image_1, 'colors': product.colors, 'stock':product.stock}}
            #add another item to the list
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    #for aumented quantity items
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                            if item['stock'] <= 0:
                                flash('No stock product')            
                    print('This product in already in your cart')
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], dictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = dictItems
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
    
    for k, product in session ['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        iva = ('%.2f' % (.21*float(subtotal)))
        # tax = iva in Argentina, with a value of 21%
        total = float('%.2f' % (1.21 * subtotal))
        
    return render_template('products/carts.html', iva = iva, total = total, subtotal=subtotal, brands=brands(), categories=categories())

"""
query to access each product

@app.route('/carts/<int:id>')
def queryStock(id):
    stock = Addproduct.query.get_or_404(id)
    return render_template('products/carts.html', stock=stock)
"""


@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session ['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated ')
                    return redirect(url_for('getCart')) 
        except Exception as e:
            print(e)
            return redirect(url_for('getCard'))


@app.route('/deleteitem/<int:id>')
def deleteItem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True 
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key,None)
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