import plaid
from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response

# CONFIGURATION SETTINGS
PLAID_REDIRECT_URI='https://us-central1-niftmint.cloudfunctions.net/'
PLAID_CLIENT_ID='6069040283c0da001182aece'
PLAID_SECRET='3be943a36853176b520a107a88316b'
PLAID_ENV='sandbox'
PLAID_PRODUCTS=['transactions']

access_token = None
item_id = None

client = plaid.Client(client_id=PLAID_CLIENT_ID,
                      secret=PLAID_SECRET,
                      environment=PLAID_ENV)

def format_error(e):
    return {
        'error': {
            'display_message': e.display_message, 
            'error_code': e.code,
            'error_type': e.type,
            'error_message': e.message
            }
        }

def create_link_token(request):
    if request.method == 'OPTIONS':
        # allows GET requests from any origin with the Content-Type
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    # set CORS headers for the main request
    headers = { 'Access-Control-Allow-Origin': '*' }
    
    # UPDATE
    client_user_id = 'user-id'

    try:
        # Create a link_token for user
        response = client.LinkToken.create({
          'user': {
            'client_user_id': client_user_id,
          },
          'products': PLAID_PRODUCTS,
          'client_name': 'Niftmint',
          'country_codes': ['US', 'CA'],
          'language': 'en',
          'redirect_uri': PLAID_REDIRECT_URI,
        })
        link_token = response['link_token']

        # Send the data to the client
        return jsonify(response)
    except plaid.errors.PlaidError as e:
        message = jsonify(format_error(e))
        return make_response(message, 400)


# Exchange token flow - exchange a Link public_token for
# an API access_token
# https://plaid.com/docs/#exchange-token-flow
def set_access_token(request):
    if request.method == 'OPTIONS':
        # allows GET requests from any origin with the Content-Type
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    # set CORS headers for the main request
    headers = { 'Access-Control-Allow-Origin': '*' }
    
    global access_token
    global item_id
    public_token = None
    
    if request.args and 'public_token' in request.args:
        # get public token from client
        public_token = request.args.get('public_token')

    try:
        exchange_response = client.Item.public_token.exchange(public_token)
    except plaid.errors.PlaidError as e:
        message = jsonify(format_error(e))
        return make_response(message, 400)

    access_token = exchange_response['access_token']
    item_id = exchange_response['item_id']

    return jsonify(exchange_response)

def info(request):
    # set CORS headers for preflight request
    if request.method == 'OPTIONS':
        # allows GET requests from any origin with the Content-Type
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    # set CORS headers for the main request
    headers = { 'Access-Control-Allow-Origin': '*' }
    
    global access_token
    global item_id
    return jsonify({
        'item_id': item_id,
        'access_token': access_token,
        'products': PLAID_PRODUCTS
        })
