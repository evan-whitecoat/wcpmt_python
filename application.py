import os
import json
from flask import Flask, redirect, request, Response

app = Flask(__name__)


@app.route('/')
def home():
    return "HealthyPay"


@app.route('/payment', methods = ['POST', 'GET'])
def payment():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success_url = request.form['success_url']
        failure_url = request.form['failure_url']
        amount = request.form['amount']
        order_id = request.form['order_id']

        # web hook
        return redirect(success_url, code=302)
    else:
        args = request.args
        # oauth2 token issued by healthypay platform
        access_token = args.get('access_token')
        # valid access token
        valid_token(access_token)
        # redirect urls
        success_url = args.get("success_url")
        failure_url = args.get("failure_url")
        # transaction
        amount = args.get("amount")
        order_id = args.get("order_id")
        return Response('''
            <p>You'll pay ${amount} using HealthyPay. The reference number is {order_id}
            <form action="" method="post">
               <p><input type=text name=username placeholder=User Name>
               <p><input type=password name=password placeholder=Password>
               <p><input type=submit value=Pay>
               <p><input type=hidden name=success_url value={success_url}>
               <p><input type=hidden name=failure_url value={failure_url}>
               <p><input type=hidden name=amount value={amount}>
               <p><input type=hidden name=order_id value={order_id}>
            </form>
           '''.format(success_url=success_url, failure_url=failure_url, amount=amount, order_id=order_id))


def valid_token(token):
    return True


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9000))
    app.run(host='0.0.0.0', port=port)
