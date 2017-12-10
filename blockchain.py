# coding: UTF-8

from time import time

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
        # ブロックをハッシュ化させる
        pass

    @property
    def last_block(self):
        return self.chain[-1]