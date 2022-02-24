from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.recipe import Recipe

@app.route("/recipes/<int:id>")
def recipes_view(id):
    recipe = Recipe.get_recipe({'id':id})
    return render_template("recipes_view.html", recipe = recipe)
