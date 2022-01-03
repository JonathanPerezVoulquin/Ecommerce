from flask import redirect, render_template, url_for, request, flash, session, current_app
from shop import db, app, photos, search
from .forms import CustomerRegisterForm


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm(request.form)
    return render_template('customer/register.html', form= form)