#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""


from flask import request, abort, jsonify
from api.v1.views import app_views
from api.v1.views import storage
from models.state import State


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a state """
    json_st = request.get_json()
    if json_st is None:
        abort(400, 'Not a JSON')
    if "name" not in json_st:
        abort(400, 'Missing name')
    n_state = State(**json_st)
    storage.new(n_state)
    storage.save()
    return jsonify(n_state.to_dict()), 201


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def attain_all_states():
    """Attains the list of all State obj"""
    state_ls = []
    states = storage.all(State)
    for state in states.values():
        state_ls.append(state.to_dict())
    return jsonify(state_ls)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def attain_state_via_id(state_id):
    """Attains the list of States via ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_via_id(state_id):
    """Deletes the list of States via ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_via_id(state_id):
    """Updates a state via ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_st = request.get_json()
    if json_st is None:
        abort(400, 'Not a JSON')
    for key, val in json_st.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, val)
    storage.save()
    return jsonify(state.to_dict()), 200
