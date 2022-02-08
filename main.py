import json
from flask import Flask, request
from web3 import Web3, HTTPProvider

# load json config
data = json.load(open('config.json'))

default_account = Web3.toChecksumAddress(data['deployer_addr'])

# connect to the node
w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161'))
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
  nonce = w3.eth.getTransactionCount(default_account)
  tx_hash = contract.functions.sendEther(address).buildTransaction({'gas': 300000,'gasPrice': w3.toWei('4', 'gwei'),'nonce': nonce,})
  signed_txn = w3.eth.account.sign_transaction(tx_hash, private_key=data['private_key'])
  w3.eth.sendRawTransaction(signed_txn.rawTransaction)

  return 'sent!'

if __name__ == '__main__':

  app.run(debug=True, host='0.0.0.0')
