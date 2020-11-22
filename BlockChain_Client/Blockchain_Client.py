from collections import OrderedDict

import binascii
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from datetime import datetime
import random
from random import choice
from random import shuffle
from random import randint
import base64
import socket

from flask import Flask, jsonify, request, render_template


class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, data):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.data = data
        # self.sender_name = sender_name
        # self.sender_surname = sender_surname
        # self.recipient_name = recipient_name
        # self.recipient_surname = recipient_surname

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
        return OrderedDict({'sender_address': self.sender_address,
                            'recipient_address': self.recipient_address,
                            'data': self.data})

    def sign_transaction(self):
        private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/budget/change')
def change_budget():
    # Name = request.form['Name']
    # Surname = request.form['Surname']
    # Login_Pass = request.form['Login_Pass']
    # con = pyodbc.connect(
    #     "Driver={ODBC Driver 17 for SQL Server};"
    #     "Server=DELL-AGA-N2B84T;"
    #     "Database=Client_List;"
    #     "Trusted_Connection=yes;"
    # )

    return render_template('change_budget.html')


@app.route('/make/transaction')
def make_transaction():
    return render_template('./make_transaction.html')


@app.route('/wallet/new', methods=['GET', 'POST'])
def new_wallet():
    Key_Size = 1024
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(Key_Size, random_gen)
    public_key = private_key.publickey()
    # login_pass = randint(10000000, 99999999)
    # if request.method == 'GET':
    response = {
        # 'login_pass': login_pass,
        'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
        'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
        }

    return jsonify(response), 200
    # else:
        # # TODO Delete Client
        # Name = request.form["Name"]
        # Surname = request.form["Surname"]
        # Computer_Id = request.form["Computer_Id"]
        # Private_Key = binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii')
        # Public_Key = binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
        # Login_Pass = login_pass
        # Time_Stamp = datetime.now()
        # con = pyodbc.connect(
        #     "Driver={ODBC Driver 17 for SQL Server};"
        #     "Server=DELL-AGA-N2B84T;"
        #     "Database=Client_List;"
        #     "Trusted_Connection=yes;"
        # )
        #
        # cursor = con.cursor()
        # cursor.execute(
        #     'INSERT INTO Client_List(Name,Surname,Computer_Id,Public_Key,Private_Key,Login_Pass,Time_Stamp) VALUES(?,?,?,?,?,?,?);',
        #     (Name, Surname, Computer_Id, Public_Key, Private_Key, Login_Pass, Time_Stamp)
        # )
        # con.commit()

    return render_template('./index.html')


@app.route('/generate/transaction', methods=['POST'])
def generate_transaction():
    sender_address = request.form['sender_address']
    sender_private_key = request.form['sender_private_key']
    recipient_address = request.form['recipient_address']
    data = request.form['data']
    # con = pyodbc.connect(
    #     "Driver={ODBC Driver 17 for SQL Server};"
    #     "Server=DELL-AGA-N2B84T;"
    #     "Database=Client_List;"
    #     "Trusted_Connection=yes;"
    # )
    # cursor = con.cursor()
    # cursor.execute("SELECT * FROM Client_List WHERE Private_Key =  " + sender_address)
    # user = cursor.fetchone()
    # a = user[2]

    transaction = Transaction(sender_address, sender_private_key, recipient_address, data)

    response = {'transaction': transaction.to_dict(),
                'signature': transaction.sign_transaction()
                }

    return jsonify(response), 200


@app.route('/view/transactions', methods=["GET"])
def view_transaction():
    # con = pyodbc.connect(
    #     "Driver={ODBC Driver 17 for SQL Server};"
    #     "Server=DELL-AGA-N2B84T;"
    #     "Database=Client_List;"
    #     "Trusted_Connection=yes;"
    # )
    #
    # cur = con.cursor()
    # cur.execute('select * from Transactions')
    # data = cur.fetchall()

    return render_template("./view_transactions.html")


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', debug=True, port=port)
