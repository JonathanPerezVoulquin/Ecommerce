from flask import redirect, render_template, url_for, request, flash, current_app, session, make_response
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos, search, bcrypt, login_manager
from .forms import CustomerLoginForm, CustomerRegisterForm
from .models import Register, CustomerOrder
import secrets
import pdfkit


@app.route('/customer/register', methods=['GET', 'POST'])
def customerRegister():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,
        password=hash_password, country=form.country.data, province=form.province.data, city= form.city.data,
        postal_code=form.postal_code.data, address=form.address.data, contact=form.contact.data, profile = form.profile.data)
        db.session.add(register) # this register is the variable
        flash(f'Welcome {form.name.data}. Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('customer/register.html', form= form)


@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Incorrect email or password', 'danger')
        return redirect(url_for('customerLogin'))

    return render_template('customer/login.html', form=form)

@app.route('/customer/logout')
def customerLogout():
    logout_user()
    return redirect(url_for('customerLogin'))


@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id 
        invoice = secrets.token_hex(5)
        try:
            order_1 = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order_1)            
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully', 'success')            
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('getCart'))


@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        total = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price'] * int(product['quantity']))
            subTotal -= discount
            iva = ('%.2f' % (.21 * float(subTotal)))
            total = (float("%.2f" % (1.21 * subTotal)))
    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, iva=iva, subTotal=subTotal, total=total, customer=customer, orders=orders )



@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        total = 0
        subTotal = 0
        customer_id = current_user.id
        if request.method == "POST":            
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
            
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subTotal += float(product['price'] * int(product['quantity']))
                subTotal -= discount
                iva = ('%.2f' % (.21 * float(subTotal)))
                total = (float("%.2f" % (1.21 * subTotal)))

            rendered = render_template('customer/pdf.html', customer=customer,invoice=invoice,orders=orders, iva=iva, total=total)
            config = pdfkit.configuration(wkhtmltopdf=b'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe')
            pdf= pdfkit.from_string(rendered,configuration=config)
            response = make_response(pdf)
            response.headers['content-Type']= 'application/pdf'
            response.headers['content-Disposition'] = 'inline: file=' + invoice + '.pdf' 
            return response
    return redirect(url_for('orders'))