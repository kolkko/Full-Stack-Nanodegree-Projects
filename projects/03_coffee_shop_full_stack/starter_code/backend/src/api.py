import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
'''
@app.route('/drinks', methods=['GET'], endpoint='get_drinks')
def get_drinks():
    """
    Public Endpoint
    Fetch all drinks with a short description
    Return either drinks array or error 
    """
    try:
        return json.dumps({
            'success': True,
            'drinks': [drink.short() for drink in Drink.query.all()]
        }), 200
    except:
        return json.dumps({
            'success': False,
            'error': "An error occured"
        }), 500
'''
@TODO implement endpoint
    GET /drinks-detail
'''
@app.route('/drinks-detail', methods=['GET'], endpoint='drinks_detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(f):
    """
    Requires Manager status
    Fetch all drinks with a long description
    Return either drinks array or error 
    """
    try:
        return json.dumps({
            'success': True,
            'drinks': [drink.long() for drink in Drink.query.all()]
        }), 200
    except:
        return json.dumps({
            'success': False,
            'error': "An error occured"
        }), 500

'''
@TODO implement endpoint
    POST /drinks
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(token):
    """
    Requires Manager status
    Create new drink
    Return either the new drink's long description or an error 
    """
    if request.data:
        new_drink_data = json.loads(request.data.decode('utf-8'))
        new_drink = Drink(
            title=new_drink_data['title'],
            recipe=json.dumps(new_drink_data['recipe'])
            )
        print(new_drink)
    else:
        abort(400)
    try:
        Drink.insert(new_drink)
        drinks = list(map(Drink.long, Drink.query.all()))
        result = {
            "success": True,
            "drinks": drinks
        }
        return jsonify(result)
    except:
        return jsonify({
            'success': False,
            'error': "An error occurred"
        }), 500
'''
@TODO implement endpoint
    PATCH /drinks/<id>
'''
@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(token, id):
    """
    Requires Manager status
    Edit a drink
    Return either the edited drink's long description or an error 
    """
    try:
        data = dict(request.form or request.json or request.data)
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink:
            drink.title = data.get('title') if data.get(
                'title') else drink.title
            recipe = data.get('recipe') if data.get('recipe') else drink.recipe
            drink.recipe = recipe if type(recipe) == str else json.dumps(
                recipe)
            drink.update()
            return json.dumps({
                'success': True, 
                'drinks': [drink.long()]
                }), 200
        else:
            return json.dumps({
                'success': False,
                'error': 'Drink not found'
            }), 404
    except:
        return json.dumps({
            'success': False,
            'error': "An error occurred"
        }), 500

'''
@TODO implement endpoint
    DELETE /drinks/<id>
'''
@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(token, id):
    """
    Requires Manager status
    Delete a drink
    Return 200 and json {"success": True, "delete": id} or an error 
    """
    try:
        data = dict(request.form or request.json or request.data)
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink:
            drink.delete()
            return json.dumps({
                'success': True, 
                'drinks': [drink.long()]
                }), 200
        else:
            return json.dumps({
                'success': False,
                'error': 'Drink not found'
            }), 404
    except:
        return json.dumps({
            'success': False,
            'error': "An error occurred"
        }), 500

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
        }), 400

@app.errorhandler(401)
def unauthorised(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "unauthorised"
        }), 401

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def auth_error(err):
    response = jsonify(err.error)
    response.status_code = err.status_code
    return response