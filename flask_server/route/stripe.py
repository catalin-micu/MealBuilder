import stripe
import json
import os

from flask import Blueprint, jsonify, request
from dotenv import load_dotenv, find_dotenv
from initialize_flask_server import app

stripe_blueprint = Blueprint('stripe_blueprint', __name__)

# Setup Stripe python client library
load_dotenv(find_dotenv())
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'
# stripe.api_version = os.getenv('STRIPE_API_VERSION')


def product_details():
    return {
        'currency': 'USD',
        'amount': 2000
    }


@stripe_blueprint.route('/', methods=['GET'])
def home():
    return "Hello from API!"


@stripe_blueprint.route('/public-key', methods=['GET'])
def PUBLISHABLE_KEY():
    return jsonify({
        'publicKey': 'pk_test_51FrQwlBnheRwo4jaGI5iqBTAA9Z9KnwBOOCiNoTMhhLsox5vKpFPB8s61gacy9H4kQZ0Jol31w1KpAHtuS7MKO1100ZOqM7qyt'
    })


@stripe_blueprint.route('/product-details', methods=['GET'])
def get_product_details():
    product = product_details()
    return jsonify(product)


@stripe_blueprint.route('/create-payment-intent', methods=['POST'])
def post_payment_intent():
    # Reads application/json and returns a response
    data = json.loads(request.data or '{}')
    product = product_details()

    options = dict()
    options.update(data)
    options.update(product)

    # Create a PaymentIntent with the order amount and currency
    payment_intent = stripe.PaymentIntent.create(**options)

    try:
        return jsonify(payment_intent)
    except Exception as e:
        return jsonify(error=str(e)), 403


@stripe_blueprint.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = 'whsec_1234'
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    print('event ' + event_type)

    if event_type == 'payment_intent.succeeded':
        # Fulfill any orders, e-mail receipts, etc
        print("💰 Payment received!")

    if event_type == 'payment_intent.payment_failed':
        # Notify the customer that their order was not fulfilled
        print("❌ Payment failed.")

    return jsonify({'status': 'success'})
