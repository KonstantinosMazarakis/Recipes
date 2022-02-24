from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.recipe import Recipe



@app.route("/recipes/<int:id>/edit")
def recipes_edit(id):

    recipe = Recipe.get_recipe({'id':id})
    recipe.date_made_on = str(recipe.date_made_on)[0:10]
    return render_template("recipes_edit.html", recipe = recipe)




@app.route("/recipes/edit_post", methods=['POST'])
def recipes_edit_post():
    data = request.form
    Recipe.edit_recipe(data)
    return redirect ("/dashboard")