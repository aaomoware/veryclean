from flask import redirect, render_template, flash, request, url_for, session
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets

@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        db.session.commit()
        flash(f'The Brand {getbrand} has been added to the database', 'success')
        return redirect(url_for('addbrand'))

    return render_template('products/brand_category.html', brands='brands')


@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        db.session.commit()
        flash(f'The Category {getcategory} has been added to the database', 'success')
        return redirect(url_for('addcategory'))

    return render_template('products/brand_category.html', brands=False)


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        colours = form.colours.data
        discount = form.discount.data
        description = form.description.data

        brand = request.form.get('brand')
        category = request.form.get('category')

        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        addproduct = Addproduct(
            name=name,
            price=price,
            stock=stock,
            colours=colours,
            discount=discount,
            description=description,
            brand_id=brand,
            category_id=category,
            image_1=image_1,
            image_2=image_2,
            image_3=image_3)
        db.session.add(addproduct)
        db.session.commit()
        flash(f'The product {name} has been added to the database', 'success')
        return redirect(url_for('addproduct'))
    return render_template('products/addproduct.html', title='Add Product Page',
                           form=form,
                           brands=brands,
                           categories=categories)
