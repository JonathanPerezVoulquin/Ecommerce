from flask import redirect, render_template, url_for, request, flash
from shop import db, app, photos, search, bcrypt
from .forms import CustomerRegisterForm
from .models import Register


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm(request.form)
    if request.method == 'POST':
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,
        password=hash_password, country=form.country.data, province=form.province.data, city= form.city.data,
        postal_code=form.postal_code.data, address=form.address.data, contact=form.contact.data, profile = form.profile.data)
        db.session.add(register) # this register is the variable
        flash(f'Welcome {form.name.data}. Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('customer/register.html', form= form)

