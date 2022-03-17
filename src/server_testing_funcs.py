from flask import Blueprint
from data_store import data_store

view_users_blueprint = Blueprint('view_users', __name__,)


@view_users_blueprint.route('/test/view/users')
def handle_test_view_users():
    return data_store.get()['users']
