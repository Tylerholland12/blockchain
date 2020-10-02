class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)
    
    
    def new_block(self, proof, previous_hash=None):
        #This function creates new blocks and then adds to the existing chain
        """This method will contain two parameters proof, previous hash"""
        block = {
            'index': len(self.chain) + 1,
            'timestamp' : time(),
            'proof': proof,
            
            previous_hash: previous_hash or self.hash(self.chain[-1]),
            }
            
            # Set the current transaction list to empty.
            
        self.current_transactions=[]
        self.chain.append(block)
        
        return block
        
    def new_transaction(self):
        #This function adds a new transaction to already existing transactions
        
        """This will create a new transaction which will be sent to the next block. It will contain
        three variables including sender, recipient and amount
        """
        
        self.current_transactions.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
                }
                )
        return self.last_block['index'] + 1
        
        @staticmethod
    
        def hash(block):
            #Used for hashing a block
            """The follow code will create a SHA-256 block hash and also ensure that the dictionary is ordered"""
            block_string = json.dumps(block, sort_keys=True).encode()
            return hashlib.sha256(block_string).hexdigest()
            
        @property
        
        def last_block(self):
            # Calls and returns the last block of the chain
            
            return self.chain[-1]

    def proof_of_work(self, last_proof):
        """This method is where you the consensus algorithm is implemented.
        It takes two parameters including self and last_proof"""
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof +=1

        return proof

        @staticmethod
        
        def valid_proof(last_proof, proof):
            
            """This method validates the block"""
            
            guess = f'{last_proof}{proof}'.encode()
            
            guess_hash = hashlib.sha256(guess).hexigest()
        
        return guess_hash[:4] == "0000"

    



app = Flask(__name__)

node_identifier = str(uuid4()).replace('-','')

# Initializing blockchain

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])

def mine():

   """Here we make the proof of work algorithm work"""

   last_block = blockchain.last_block

   last_proof = last_block['proof']

   proof = blockchain.proof_of_work(last_proof)




   # rewarding the miner for his contribution. 0 specifies new coin has been mined

   blockchain.new_transaction(

       sender="0",

       recipient = node_identifier,

       amount = 1,

   )




   # now create the new block and add it to the chain

   previous_hash = blockchain.hash(last_block)

   block = blockchain.new_block(proof, previous_hash)




   response = {

       'message': 'The new block has been forged',

       'index': block['index'],

       'transactions': block['transactions'],

       'proof': block['proof'],

       'previous_hash' : block['previous_hash']

   }

   return jsonify(response), 200




@app.route('/transactions/new', methods=['POST'])

def new_transaction():
    values = request.get_json()
    # Checking if the required data is there or not
    required = ['sender','recipient','amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # creating a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient', values['amount']])
    response = {'message': f’Transaction is scheduled to be added to Block No. {index}'}
    return jsonify(response), 201


@app.router('/chain', methods=['GET'])




def full_chain():

   response = {

       'chain' : blockchain.chain,

       'length' : len(blockchain.chain)

   }

   return jsonify(response), 200




if __name__ == '__main__':

   app.run(host="0.0.0.0", port=5000)