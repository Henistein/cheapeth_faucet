import json
import time
from flask import Flask, request
from web3 import Web3, HTTPProvider

# cooldowns
class Cooldowns:
  def __init__(self, path):
    self.path = path
    try:
      self.addresses = json.load(open(path))
    except:
      self.addresses = {}
    self.period = 604800 # 7 days

  def update_file(self):
    f = open(self.path, 'w')
    f.write(json.dumps(self.addresses))
    f.close()
    
C = Cooldowns('cooldowns.json')

# load json config
data = json.load(open('config.json'))

default_account = Web3.toChecksumAddress(data['deployer_addr'])

# connect to the node
w3 = Web3(Web3.HTTPProvider('https://node.cheapeth.org/rpc'))
w3.eth.default_account = default_account

# load abi file
abi = json.load(open('faucet.json'))

# load contract
faucet_address = Web3.toChecksumAddress(data['faucet_contract_addr'])
contract = w3.eth.contract(faucet_address, abi=abi)

app = Flask(__name__)

@app.route('/')
def index():
  return "HELLO"

@app.route('/faucet')
def faucet():
  address = Web3.toChecksumAddress(request.args.get('address'))

  # check if address is on cooldown
  if (address in C.addresses) and ((C.addresses[address] + C.period) > time.time()):
    return f"{address} still in cooldown"
  else:
    # send cheapeth
    nonce = w3.eth.getTransactionCount(default_account)
    tx_hash = contract.functions.sendEther(address).buildTransaction({'chainId':777, 'gas': 300000,'gasPrice': w3.toWei('1', 'gwei'),'nonce': nonce,})
    signed_txn = w3.eth.account.sign_transaction(tx_hash, private_key=data['private_key'])
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    # update cooldowns
    C.addresses[address] = time.time()
    C.update_file()

    return 'sent!'

if __name__ == '__main__':

  app.run(debug=True, host='0.0.0.0')
