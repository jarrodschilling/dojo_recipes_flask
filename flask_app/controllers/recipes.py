from flask import Flask, redirect, request, flash, session, render_template
from flask_app import app
from flask_app.models.recipe import Recipe


@app.route('/recipes')
def recipes_home():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    recipes = Recipe.get_all(data)
    return render_template('recipes.html', recipes=recipes)


@app.route('/recipes/create')
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_recipe.html')


@app.route('/recipes/new', methods=['POST'])
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/create')

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


@app.route('/recipes/<int:recipe_id>')
def get_one_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_one(data)
    return render_template("recipe.html", recipe=recipe)

@app.route("/recipes/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': recipe_id
    }
    one_recipe = Recipe.delete_one(data)
    return redirect('/recipes')

@app.route("/recipes/edit/<int:recipe_id>")
def update_recipe_page(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_one(data)
    return render_template('edit.html', recipe=recipe)


@app.route("/recipes/update", methods=['POST'])
def update_recipe():
    print(request.form)
    if 'user_id' not in session:
        return redirect('/')
    check_id = request.form['id']
    if 'under' not in request.form:
        flash("Can this be made in under 30 mins?")
        return redirect(f'/recipes/edit/{check_id}')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{check_id}')
    data = {
        'id': request.form['id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'under': request.form['under'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made']
    }

    recipe_update = Recipe.update_recipe(data)
    return redirect('/recipes')