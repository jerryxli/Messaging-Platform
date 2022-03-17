from auth import change_global_permission, auth_register_v1
import flask
import json

user_perm_change = flask.Blueprint('user_perm_change', __name__)


@user_perm_change.route("/admin/userpermission/change/v1")
def handle_perm_change():
    auth_register_v1("tetian@gmail.com", "wopooo", "Tetian", "Madfouni")
    auth_register_v1("madfouni@gmail.com", "wopooooo", "Tetian", "Madfouni2")
    data = json.loads(flask.request.data)
    change_global_permission(int(data['u_id']), int(data['permission_id']))
    return {}


