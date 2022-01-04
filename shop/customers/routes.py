from flask import redirect, render_template, url_for, request, flash, current_app
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos, search, bcrypt, login_manager
from .forms import CustomerLoginForm, CustomerRegisterForm
from .models import Register


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