from flask import redirect, render_template, flash, request, url_for
from shop import db, app
from .models import Brand, Category
from .forms import Addproducts

@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
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
    brands = Brands.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    return render_template('products/addproduct.html', title='Add Product Page',
                           form=form,
                           brands=brands,
                           categories=category)
