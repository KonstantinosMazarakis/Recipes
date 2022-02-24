from flask_app.controllers import login_and_registration
from flask_app.controllers import recipes_new
from flask_app.controllers import recipes_view
from flask_app.controllers import recipes_edit

from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)
