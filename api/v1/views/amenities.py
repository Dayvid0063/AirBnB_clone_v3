#!/usr/bin/python3
"""Amenity objects that handles all default RESTFul API actions"""


from flask import request, abort, jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities():
    """attain the list of all Amenity obj"""
    amenities_ls = []
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        amenities_ls.append(amenity.to_dict())
    return jsonify(amenities_ls)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """attains the list of Amenities via ID"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates Amenity"""
    amenity_js = request.get_json()
    if amenity_js is None:
        abort(400, 'Not a JSON')
    if "name" not in amenity_js:
        abort(400, 'Missing name')
    if len(amenity_js) != 1:
        abort(400)
    new_amenity = Amenity(**amenity_js)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates amenity obj"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    amenity_js = request.get_json()
    if amenity_js is None:
        abort(400, 'Not a JSON')
    for k, val in amenity_js.items():
        if k not in ('id', 'created_at', 'updated_at'):
            setattr(amenities, k, val)
    storage.save()
    return jsonify(amenities.to_dict()), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes Amenities ID"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    storage.delete(amenities)
    storage.save()
    return jsonify({}), 200
