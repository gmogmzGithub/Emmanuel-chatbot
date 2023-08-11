from flask import Flask, request
import stripe

app = Flask(__name__)

# Replace with your Stripe webhook secret key
stripe_endpoint_secret = "your_stripe_endpoint_secret"

@app.route('/', methods=['GET'])
def homepage():
    content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Emma Webhook Server</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #282c34;
                color: #61dafb;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                padding: 20px;
                border-radius: 8px;
                background-color: #20232a;
                box-shadow: 0 2px 12px rgba(0,0,0,0.1);
            }
            h1 {
                margin-top: 0;
            }
            p {
                font-size: 1.2em;
            }
            a {
                color: #61dafb;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Emma Webhook Server</h1>
            <p>This server handles payment webhooks and other related tasks.</p>
            <p>Check the server's <a href="/alive">status</a>.</p>
        </div>
    </body>
    </html>
    """
    return content



@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        # Verify the event by checking its signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_endpoint_secret
        )
    except Exception as e:
        # Invalid payload
        return str(e), 400

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        # TODO: Perform actions based on the payment success, like updating user status

    return '', 200


@app.route('/alive', methods=['GET'])
def check_alive():
    message = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Server Status</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #282c34;
                color: #61dafb;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                padding: 20px;
                border-radius: 8px;
                background-color: #20232a;
                box-shadow: 0 2px 12px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Emma Webhook Server</h1>
            <p>Status: Alive and kicking!</p>
        </div>
    </body>
    </html>
    """
    return message, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

