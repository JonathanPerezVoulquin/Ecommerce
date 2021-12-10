from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app
from shop.products.models import Addproduct

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
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()
        if product_id and quantity and colors and request.method == 'POST':
            dictItems = {product_id:{'name': product.name, 'price': product.price, 'discount': product.discount,
            'color':colors, 'quantity': quantity, 'image': product.image_1}}
            #add another item to the list
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
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