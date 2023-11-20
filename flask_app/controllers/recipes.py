from flask import Flask, redirect, request, flash, session, render_template
from flask_app import app
from flask_app.models.recipe import Recipe


@app.route('/recipes')
def recipes_home():
    data = {
        'user_id': session['user_id']
    }
    recipes = Recipe.get_all(data)
    return render_template('recipes.html', recipes=recipes)

@app.route('/recipes/new')
def new_recipe_get():
    return render_template('new_recipe.html')

@app.route('/recipes/new', methods=['POST'])
def new_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under': request.form['under'],
        'user_id': session['user_id']
    }

    new_recipe = Recipe.save(data)

    return redirect('/recipes')