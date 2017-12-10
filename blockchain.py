# coding: UTF-8

import hashlib
import json

from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from textwrap import dedent

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self, proof, previous_hash=None):
        """
        ブロックチェーンに新しいブロックを作る
        :param proof:  プルーフ・オブ・ワークアルゴリズムから得られるグループ
        :param previous_hash:  前のブロックのハッシュ
        :return: 新しいブロック
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hush': previous_hash or self.hash(chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

        # 新しいブロックを作り、チェーンに加える
        pass

    def new_transaction(self, sender, recipient, amount):
        """
        次に採掘されるブロックに加える新しいトランザクションを作る
        :param sender: <str> 送信者のアドレス
        :param recipient: <str> 受信者のアドレス
        :param amount: <int> 量
        :return: <int> このトランザクションを含むブロックのアドレス
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        ブロックをSHA-256でハッシュ化させる
        :param block: ブロック
        :return:
        """
        # 必ずディクショナリ（辞書型のオブジェクト）がソートされている必要がある。そうでないと、一貫性のないハッシュとなってしまう
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]


    def proof_of_work(self, last_proof):
        """
        シンプルなプルーフ・オブ・ワークのアルゴリズム:
            - hash(pp')の最初の4つが0となるようなp'を探す
            - p は前のプルーフ、p'は新しいプルーフ
        :param last_proof:
        :return:
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        プルーフが正しいかを確認する: hash(last_proof, proof)の最初の4つが0となっているのか？
        :param last_proof: 前のプルーフ
        :param proof:  現在のプルーフ
        :return: 正しければ、true, そうでなければfalse
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest
        return guess_hash[:4] == "0000"


# ノードを作成
app = Flask(__name__)

# このノードのグローバルにユニークなアドレスを作成
node_identifire = str(uuid4()).replace('-', '')

# ブロックチェーンクラスをインスタンス化する
blockchain = Blockchain()

# メソッドはGETで/mineエンドポイントを作る
@app.route('/mine', methods=['GET'])
def mine():
    return '新しいブロックを採掘します'

# メソッドはPOSTで/transactions/newエンドポイントを作る。メソッドはPOSTなのでデータを送信する
@app.route('/transactions/new', methods=['POST'])
def new_transactions():
    values = request.get_json()
    # Postされたデータに必要なデータがあるか確認
    required = ['sender','recipient','amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # 新しいトランザクションを作成
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'トランザクションはブロック {index} に追加されました'}
    return jsonify(response), 201

# メソッドはGETで、フルのブロックチェーンをリターンする/chainエンドポイントを作る
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

# port5000でサーバーを起動する
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)