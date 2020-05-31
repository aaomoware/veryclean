from flask import render_template, request, session, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user, login_user
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Addproduct, Brand, Category
import os

@app.route('/admin')
@login_required
def admin():
    if current_user.is_authenticated:
        if os.environ['ADMIN'] != current_user.email:
            return redirect(url_for('shop'))
        else:
            products = Addproduct.query.all()
            return render_template('admin/index.html', title='Admin Page', products=products)



@app.route('/brands')
@login_required
def brands():
    if current_user.is_authenticated:
        if os.environ['ADMIN'] != current_user.email:
            return redirect(url_for('shop'))
        else: 
            brands = Brand.query.order_by(Brand.id.desc()).all()
            return render_template('admin/brands.html', title='Brand Page', brands=brands)



@app.route('/categories')
@login_required
def categories():
    if current_user.is_authenticated:
        if os.environ['ADMIN'] != current_user.email:
            return redirect(url_for('shop'))
        else:
            categories = Category.query.order_by(Category.id.desc()).all()
            return render_template('admin/brands.html', title='Category Page', categories=categories)

