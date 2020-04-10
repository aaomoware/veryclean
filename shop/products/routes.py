from flask import redirect, render_template, flash, request, url_for, session, current_app
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets, os



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



@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')

    if request.method == 'POST':
        updatebrand.name = brand
        flash(f'Yuor brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))

    return render_template('products/updatebrand.html', title='Update Brand Page', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    brand = Brand.query.get_or_404(id)
    
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from the database', 'success')
        return redirect(url_for('brands'))

    flash(f'The brand {brand.name} cant not be deleted', 'warning')
    return redirect(url_for('brands'))


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



@app.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')

    if request.method == 'POST':
        updatecategory.name = category
        flash(f'Yuor Category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('categories'))

    return render_template('products/updatebrand.html', title='Update category Page', updatecategory=updatecategory)



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


@app.route('/updateproduct/<int:id>', methods=["GET", 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    form = Addproducts(request.form)
    products = Addproduct.query.get_or_404(id)
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')

    if request.method == 'POST':
        products.name = form.name.data
        products.price = form.price.data
        products.discount = form.discount.data
        products.stock = form.stock.data
        products.colours = form.colours.data
        products.description = form.description.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + products.image_1))
                products.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                products.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + products.image_2))
                products.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                products.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + products.image_3))
                products.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                products.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash(f'The product as been updated', 'success')
        return redirect(url_for('admin'))

    form.name.data = products.name
    form.price.data = products.price
    form.discount.data = products.discount
    form.stock.data = products.stock
    form.colours.data = products.colours
    form.description.data = products.description
    return render_template('products/updateproduct.html', form=form, brands=brands, products=products, categories=categories)