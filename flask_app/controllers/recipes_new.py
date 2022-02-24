from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.recipe import Recipe


@app.route("/recipes/new")
def recipes_new():
    return render_template("recipes_new.html")



@app.route("/recipes/new_post", methods=['POST'])
def recipes_new_post():
    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made_on': request.form['date_made_on'],
        'under_30_minutes': request.form['under_30_minutes'],
                'users_id': session['id']
        }

    Recipe.add_recipe(data)
    return redirect("/dashboard")
