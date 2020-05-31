from flask import redirect, render_template, flash, request, url_for, session, current_app
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets, os


@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=8)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()

    colours = []
    for product in products.items:
        colours.append(product.colours)
    return render_template('products/index.html', products=products, brands=brands, categories=categories, colours=set(colours), home=1)



@app.route('/about')
def about():
    return render_template('products/about.html', about=1)

@app.route('/contact')
def contactus():
    return render_template('products/contact.html', contact=1)

@app.route('/shop')
def shop():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=8)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()

    colours = []
    for product in products.items:
        colours.append(product.colours)
    return render_template('products/shop.html', products=products, shop=1)


@app.route('/product/<int:id>')
def product_details(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/product_details.html', product=product, product_details=1)



@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    brand_id = Brand.query.filter_by(id=id).first_or_404()
    products = Addproduct.query.filter_by(brand=brand_id).paginate(page=page, per_page=6)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()

    colours = []
    for product in products.items:
        colours.append(product.colours)
    return render_template('products/index.html', brand=products, brands=brands, categories=categories, colours=set(colours), brand_id=brand_id)


@app.route('/category/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    category_id = Category.query.filter_by(id=id).first_or_404()
    products = Addproduct.query.filter_by(category=category_id).paginate(page=page, per_page=8)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()

    colours = []
    for product in products.items:
        colours.append(product.colours)
    return render_template('products/index.html', category=products, brands=brands, categories=categories, colours=set(colours), category_id=category_id)



@app.route('/addbrand', methods=['GET', 'POST'])
@login_required
def addbrand():
    if os.environ['ADMIN'] not in session:
        return redirect(url_for('shop'))
    else:
        if request.method == 'POST':
            getbrand = request.form.get('brand')
            brand = Brand(name=getbrand)
            db.session.add(brand)
            db.session.commit()
            flash(f'The Brand {getbrand} has been added to the database', 'success')
            return redirect(url_for('brands'))
        return render_template('products/brand_category.html', brands='brands')



@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
@login_required
def updatebrand(id):
    if os.environ['ADMIN'] not in session:
        return redirect(url_for('shop'))
    else:
        updatebrand = Brand.query.get_or_404(id)
        brand = request.form.get('brand')

        if request.method == 'POST':
            updatebrand.name = brand
            flash(f'Yuor brand has been updated', 'success')
            db.session.commit()
            return redirect(url_for('brands'))
        return render_template('products/updatebrand.html', title='Update Brand Page', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['POST'])
@login_required
def deletebrand(id):
    if os.environ['ADMIN'] not in session:
        return redirect(url_for('shop'))
    else:
        brand = Brand.query.get_or_404(id)
    
        if request.method == 'POST':
            db.session.delete(brand)
            db.session.commit()
            flash(f'The brand {brand.name} was deleted from the database', 'success')
            return redirect(url_for('brands'))
        return redirect(url_for('brands'))


@app.route('/addcategory', methods=['GET', 'POST'])
@login_required
def addcategory():
    if os.environ['ADMIN'] not in session:
        return redirect(url_for('shop'))
    else:
        if request.method == 'POST':
            getcategory = request.form.get('category')
            category = Category(name=getcategory)
            db.session.add(category)
            db.session.commit()
            flash(f'The Category {getcategory} has been added to the database', 'success')
            return redirect(url_for('categories'))
        return render_template('products/brand_category.html', brands=False)



@app.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
@login_required
def updatecategory(id):
    if os.environ['ADMIN'] not in session:
        return redirect(url_for('shop'))
    else:
        updatecategory = Category.query.get_or_404(id)
        category = request.form.get('category')

        if request.method == 'POST':
            updatecategory.name = category
            flash(f'Yuor Category has been updated', 'success')
            db.session.commit()
            return redirect(url_for('categories'))
        return render_template('products/updatebrand.html', title='Update category Page', updatecategory=updatecategory)



@app.route('/deletecategory/<int:id>', methods=['POST'])
@login_required
def deletecategory(id):
    if os.environ['ADMIN'] not in session:
        return redirect(url_for('shop'))
    else:
        category = Category.query.get_or_404(id)
        
        if request.method == 'POST':
            db.session.delete(category)
            db.session.commit()
            flash(f'The category {category.name} was deleted from the database', 'success')
            return redirect(url_for('categories'))
        return redirect(url_for('categories'))



@app.route('/addproduct', methods=['GET', 'POST'])
@login_required
def addproduct():
    if os.environ['ADMIN'] not in session:
        return redirect(url_for('shop'))
    else:
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
            return redirect(url_for('admin'))
        return render_template('products/addproduct.html', title='Add Product Page', form=form, brands=brands, categories=categories)


@app.route('/updateproduct/<int:id>', methods=["GET", 'POST'])
@login_required
def updateproduct(id):
    if os.environ['ADMIN'] not in session:
        return redirect(url_for('shop'))
    else:
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


@app.route('/deleteproduct/<int:id>', methods=['POST'])
@login_required
def deleteproduct(id):
    if os.environ['ADMIN'] not in session:
        return redirect(url_for('shop'))
    else:
        product = Addproduct.query.get_or_404(id)

        if request.method == 'POST':
            if request.files.get('image_1'):
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + products.image_1))
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + products.image_2))
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + products.image_3))
                except Exception as e:
                    print(e)
            db.session.delete(product)
            db.session.commit()
            flash(f'The product {product.name} has been deleted', 'success')
            return redirect(url_for('admin'))
        return redirect(url_for('admin'))
