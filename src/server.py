import flask
from server_testing_funcs import view_users_blueprint
from server_auth import user_perm_change


app = flask.Flask(__name__)
app.register_blueprint(view_users_blueprint)
app.register_blueprint(user_perm_change)

app.run(port=5000, debug = True)