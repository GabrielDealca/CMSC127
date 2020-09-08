from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from .models import Group, Category, AddProduct
from .forms import Addproducts

import secrets, os

@app.route('/')
def home():
	page = request.args.get('page', 1, type=int)
	products = AddProduct.query.filter(AddProduct.stock > 0).order_by(AddProduct.id.desc()).paginate(page=page, per_page=2)
	groups = Group.query.join(AddProduct, (Group.id == AddProduct.group_id)).all()
	categories = Category.query.join(AddProduct, (Category.id == AddProduct.category_id)).all()
	return render_template('products/index.html', products=products, groups=groups, categories=categories)

@app.route('/product/<int:id>')
def single_page(id):
	product = AddProduct.query.get_or_404(id)
	groups = Group.query.join(AddProduct, (Group.id == AddProduct.group_id)).all()
	categories = Category.query.join(AddProduct, (Category.id == AddProduct.category_id)).all()
	return render_template('products/single_page.html', product=product, groups=groups, categories=categories)

@app.route('/group/<int:id>', methods=['GET', 'POST'])
def get_group(id):
	page = request.args.get('page', 1, type=int)
	get_g = Group.query.filter_by(id=id).first_or_404()
	group = AddProduct.query.filter_by(group_id=id).paginate(page=page, per_page=2)
	groups = Group.query.join(AddProduct, (Group.id == AddProduct.group_id)).all()
	categories = Category.query.join(AddProduct, (Category.id == AddProduct.category_id)).all()
	return render_template('products/index.html', group=group, groups=groups, categories=categories, get_g=get_g)

@app.route('/categories/<int:id>', methods=['GET', 'POST'])
def get_category(id):
	page = request.args.get('page', 1, type=int)
	get_cat = Category.query.filter_by(id=id).first_or_404()
	get_catprod = AddProduct.query.filter_by(category=get_cat).paginate(page=page, per_page=2)
	categories = Category.query.join(AddProduct, (Category.id == AddProduct.category_id)).all()
	groups = Group.query.join(AddProduct, (Group.id == AddProduct.group_id)).all()
	return render_template('products/index.html', get_catprod=get_catprod, categories=categories, groups=groups, get_cat=get_cat)


@app.route('/addgroup', methods=['GET', 'POST'])
def addgroup():
	if 'email' not in session:
		flash(f'Please login first', 'danger')
		return redirect(url_for('login'))
	if request.method == "POST":
		getgroup = request.form.get('group')
		group = Group(name=getgroup)
		db.session.add(group)
		flash(f'The Group {getgroup} was added to your database', 'success')
		db.session.commit()
		return redirect(url_for('addgroup'))

	return render_template('products/addgroup.html', groups='groups')

@app.route('/updategroup/<int:id>', methods=['GET', 'POST'])
def updategroup(id):
	if 'email' not in session:
		flash(f'Please login first', 'danger')
		return redirect(url_for('login'))
	updategroup = Group.query.get_or_404(id)
	group = request.form.get('group')
	if request.method == "POST":
		updategroup.name = group
		flash(f'The group name has been updated', 'success')
		db.session.commit()
		return redirect(url_for('groups'))
	return render_template('products/updategroup.html', title='Update Groups', updategroup=updategroup)

@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
	if 'email' not in session:
		flash(f'Please login first', 'danger')
		return redirect(url_for('login'))
	updatecat = Category.query.get_or_404(id)
	group = request.form.get('category')
	if request.method == "POST":
		updatecat.name = category
		flash(f'The category has been updated', 'success')
		db.session.commit()
		return redirect(url_for('categories'))
	return render_template('products/updategroup.html', title='Update Categories', updatecat=updatecat)

@app.route('/deletegroup/<int:id>', methods=['GET', 'POST'])
def deletegroup(id):
	group = Group.query.get_or_404(id)
	if request.method == "POST":
		db.session.delete(group)
		db.session.commit()
		flash(f'The group {group.name} was deleted from your database', 'success')
		return redirect(url_for('admin'))
	flash(f"The group {group.name} can't be deleted from your database", 'warning')
	return redirect(url_for('admin'))

@app.route('/deletecat/<int:id>', methods=['GET', 'POST'])
def deletecat(id):
	category = Category.query.get_or_404(id)
	if request.method == "POST":
		db.session.delete(category)
		db.session.commit()
		flash(f'The group {category.name} was deleted from your database', 'success')
		return redirect(url_for('admin'))
	flash(f"The group {category.name} can't be deleted from your database", 'warning')
	return redirect(url_for('admin'))



@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
	if 'email' not in session:
		flash(f'Please login first', 'danger')
		return redirect(url_for('login'))
	if request.method == "POST":
		getcat = request.form.get('category')
		cat = Category(name=getcat)
		db.session.add(cat)
		flash(f'The Category {getcat} was added to your database', 'success')
		db.session.commit()
		return redirect(url_for('addcat'))

	return render_template('products/addgroup.html')

@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
	if 'email' not in session:
		flash(f'Please login first', 'danger')
		return redirect(url_for('login'))
	groups = Group.query.all()
	categories = Category.query.all()
	form = Addproducts(request.form)
	if request.method == "POST":
		name = form.name.data
		price = form.price.data
		# discount.form.discount.data
		stock = form.stock.data
		# colors = form.colors.data
		desc = form.description.data
		group = request.form.get('group')
		category = request.form.get('category')
		image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
		image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
		image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
		addpro = AddProduct(name=name, price=price, stock=stock, desc=desc, group_id=group, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)
		db.session.add(addpro)
		flash(f'The product {name} has been added to your database', 'success')
		db.session.commit()
		return redirect(url_for('admin'))

	return render_template('products/addproduct.html', form=form, title="Add Product", groups=groups, categories=categories)

@app.route('/updateproduct/<int:id>', methods=['POST', 'GET'])
def updateproduct(id):
	groups = Group.query.all()
	categories = Category.query.all()
	product = AddProduct.query.get_or_404(id)
	group = request.form.get('group')
	category = request.form.get('category')
	form = Addproducts(request.form)
	if request.method == "POST":
		product.name = form.name.data
		product.price = form.price.data
		product.group_id = group
		product.category_id = category
		product.desc = form.description.data
		product.stock = form.stock.data
		if request.files.get('image_1'):
			try:
				os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
				product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
			except:
				product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

		if request.files.get('image_2'):
			try:
				os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
				product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
			except:
				product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

		if request.files.get('image_3'):
			try:
				os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
				product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
			except:
				product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

		db.session.commit()
		flash(f'You product has been updated', 'success')
		return redirect(url_for('admin'))

	form.name.data = product.name
	form.price.data = product.price
	form.stock.data = product.stock
	form.description.data = product.desc
	return render_template('products/updateproduct.html', form=form, title="Update Products", groups=groups, categories=categories, product=product)

@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
	product = AddProduct.query.get_or_404(id)
	if request.method == "POST":			
		try:
			os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))						
			os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))			
			os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
		except Exception as e:
			print(e)
			
		db.session.delete(product)
		db.session.commit()
		flash(f'{product.name} has been deleted from products', 'success')
		return redirect(url_for('admin'))
	flash(f"{product.name} can't be deleted from products", 'success')
	return redirect(url_for('admin'))