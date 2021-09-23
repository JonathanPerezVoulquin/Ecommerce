from flask import redirect, render_template, url_for, request, flash, session, current_app
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets
import os


@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=8)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', products=products, brands=brands, categories=categories)

@app.route('/brand/<int:id>')
def get_brand(id):
    brand = Addproduct.query.filter_by(brand_id=id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', brand=brand, brands=brands, categories=categories)


@app.route('/categories/<int:id>')
def get_category(id):
    get_cat_prod = Addproduct.query.filter_by(category_id=id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', get_cat_prod=get_cat_prod, categories=categories, brands=brands)


# BRAND
@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')


@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name = brand
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update brand Page', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f"The brand {brand.name} was deleted from your database", "success")
        return redirect(url_for('admin'))
    flash(f"The brand {brand.name} can't be  deleted from your database", "warning")
    return redirect(url_for('admin'))


# CATEGORY
@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getbrand = request.form.get('category')
        cat = Category(name=getbrand)
        db.session.add(cat)
        flash(f'The Category {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html')


@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecat.name = category
        flash(f'Your category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/addbrand.html', title='Update Category Page', updatecat=updatecat)


@app.route('/deletecat/<int:id>', methods=['POST'])
def deletecat(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        db.session.commit()
        flash(f"The brand {category.name} was deleted from your database", "success")
        return redirect(url_for('admin'))
    flash(f"The brand {category.name} can't be  deleted from your database", "warning")
    return redirect(url_for('admin'))


# PRODUCTS
@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock,
                            colors=colors, desc=desc,
                            brand_id=brand, category_id=category,
                            image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        db.session.commit()
        flash(f'The product {name} has breen added to your database', 'success')
        return redirect(url_for('admin'))

    return render_template('products/addproduct.html', title='Add Product Page', form=form, brands=brands,
                           categories=categories)


@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.color = form.colors.data
        product.desc = form.discription.data
        if request.files.get(
                'image_1'):  # To update and delete photos, using library os ,do it with the 'try' and 'except'
            try:
                os.unlink(os.path.join(current_app.root_path,
                                       'static/images/' + product.image_1))  # if we do not put "/" at the end it does not delete the photo to edit'static/images/'
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')

        db.session.commit()
        flash('You product has been updated', 'success')
        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discription.data = product.discount
    form.stock.data = product.stock
    form.discription.data = product.desc
    return render_template('products/updateproduct.html', form=form, product=product, categories=categories,
                           brands=brands)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    product = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was deleted form your record', 'success')
        return redirect(url_for('admin'))
    flash(f'Cant delete the product', 'danger')
    return redirect(url_for('admin'))