from flask import Flask
from flask import render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from  wtforms import StringField,SubmitField
from wtforms.validators import DataRequired, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Item(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	item = db.Column(db.String(30),unique=True)
	done = db.Column(db.Boolean(), default=False)
	def __repr__(self):
		return f"Item('{self.item}')"
class TodoForm(FlaskForm):
	item = StringField('item',validators=[DataRequired()])
	editedItem = StringField('editedItem')
	submit = SubmitField('Add')
	remove = SubmitField('Remove')
	edit = SubmitField('Edit')
	save = SubmitField('Save')
	done = SubmitField('Done')
	notDone = SubmitField('Not Done')

	def validate_item(self,item):
		ITEM = Item.query.filter_by(item=item.data).first()
		if ITEM:
			raise ValidationError('Already added')

@app.route('/', methods=['GET', 'POST'])
def Home():
	form = TodoForm()
	items = Item.query.all()
	if form.validate_on_submit():
		newItem = request.form['item']
		new = Item(item=newItem)
		db.session.add(new)
		db.session.commit()
		items = Item.query.all()
		return render_template('home.html',form = form,items=items)
	else:
		print(form.errors)
	return render_template('home.html',form = form,items=items)

@app.route("/remove/<int:item_id>",methods=['GET','POST'])
def delete(item_id):
	form = TodoForm()
	Item.query.filter_by(id=int(item_id)).delete()
	db.session.commit()
	items = Item.query.all()
	return redirect(url_for('Home'))

@app.route("/edit/<int:item_id>",methods=['GET','POST'])
def edit(item_id):
	form = TodoForm()
	items = Item.query.all()
	return render_template('home.html',form = form,items=items,item_id=item_id)

@app.route("/save/<int:item_id>",methods=['GET','POST'])
def save(item_id):
	form = TodoForm()
	#if form.validate_on_submit():
	newItem = request.form['editedItem']
	item = Item.query.filter_by(id=item_id).first()
	item.item = newItem
	db.session.commit()
	return redirect(url_for('Home'))

@app.route("/done/<int:item_id>",methods=['GET','POST'])
def done(item_id):
	form = TodoForm()
	item = Item.query.filter_by(id=item_id).first()
	item.done = True
	db.session.commit()
	return redirect(url_for('Home'))

@app.route("/notDone/<int:item_id>",methods=['GET','POST'])
def notDone(item_id):
	form = TodoForm()
	item = Item.query.filter_by(id=item_id).first()
	item.done = False
	db.session.commit()
	return redirect(url_for('Home'))

if __name__ == '__main__':
	app.debug = True
	app.run()