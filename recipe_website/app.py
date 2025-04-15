import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import datetime
from forms import RecipeForm

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')
from models import Recipe, Category, db

db.init_app(app)

@app.route('/')
def index():
    recepies = Recipe.query.all()
    categories = Category.query.all()
    return render_template('index.html', recepies=recepies, categories=categories, datetime=datetime)

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', recipe=recipe, datetime=datetime)

@app.route('/add', methods=['GET', 'POST'])
def new_recipe():
    form = RecipeForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        new_recipe = Recipe(title=form.title.data, ingredients=form.ingredients.data, 
                            instructions=form.instructions.data, created_at=datetime.now(), category_id=form.category_id.data)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('index'))
    
    # Render the add recipe form
    return render_template('new_recipe.html', form=form, datetime=datetime)

@app.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = RecipeForm(obj=recipe)  # Populate form with existing recipe data
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        recipe.category_id = form.category_id.data

        db.session.commit()
        return redirect(url_for('view_recipe', recipe_id=recipe.id))
    return render_template('edit_recipe.html', form=form, recipe=recipe, datetime=datetime)
    
@app.route('/delete/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
