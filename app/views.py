################################# Connect to redis server
from xml.etree.ElementTree import tostring
import redis
redis_host = '127.0.0.1'
client = redis.StrictRedis(host=redis_host, port=6379, password='',db=0)

try:
  client.client_list()
  print('CONNECTION TO REDIS OK')
except:
  sys.exit('CONNECTION TO REDIS SERVER FAILED: exiting...')
  

################################# Fetch deployed conract
import sys
from django.conf import settings
BLOCKCHAIN = settings.BLOCKCHAIN
if BLOCKCHAIN == 'ganache':
  blockchain_address = 'http://127.0.0.1:7545'
  chain_id = 1337
elif BLOCKCHAIN == 'ropsten':
  blockchain_address = 'https://ropsten.infura.io/v3/7340ba294b4f4b1da1ffdd1d23ef3022'
  chain_id = 3
else:
  sys.exit('No valid blockchain provided: exiting...')

from web3 import Web3
w3 = Web3(Web3.HTTPProvider(blockchain_address))
if not w3.isConnected():
  sys.exit('BLOCKCHAIN NOT CONNECTED: exiting...')
else:
  print('CONNECTION TO WEB3 OK')

# retrieve contract vars
import json
deployed_contract_address = w3.toChecksumAddress("0xf9afeb0471114a544F1D5Ddf7DecA49f246B29e5")
if not w3.isAddress(deployed_contract_address):
  sys.exit('CONTRACT ADDRESS NOT VALID: exiting...')
else:
  print('CONTRACT ADDRESS OK')
compiled_contract_path = 'truffle/build/Platform.json'
with open(compiled_contract_path) as file:
  contract_json = json.load(file)  # load contract info as JSON
  contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# create contract instance
contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)

# set as default account as empty for safety reason
w3.eth.default_account = contract.address#w3.eth.accounts[0] # client.get("account").decode("utf-8")

################################# Methods

from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import time
from pprint import pprint
from .forms import AuctionForm
from .models import AuctionModelForm

# the following decorator allows to avoid 403 forbidden error since post methods is unsafe
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def test(request):
  try:
    # save account in redis db for history purpose
    result = json.loads(request.body)
    client.set("account", result['account'])
    # update default account
    w3.eth.default_account = w3.toChecksumAddress(result['account'])
  except (ValueError, KeyError):
    raise ValueError('Invalid POST parameters')
  return JsonResponse({'result': result['account']})

@csrf_exempt
def new(request):
  try:
    result = json.loads(request.body)
    if not (w3.eth.default_account==w3.toChecksumAddress(result['currentAccount'])):
      sys.exit('Account is not equal to the last one stored: exiting...')
    amount = Web3.toWei(int(result['amount']), 'ether')
    if amount <= 0:
      return JsonResponse({'result': 'Amount must be greater than 0.'})
    
    # vars are ok
    now = int(time.time()) # unix epoch
    deadline = 60 # [s], set a fixed deadline of +24 hours
    print('---------------------->CALLING CONTRACT FUNCTIONS')
    new_contract_txn = contract.functions.newAuction(
      w3.eth.default_account, result['description'], amount, deadline).buildTransaction({
      'nonce': w3.eth.getTransactionCount(w3.eth.default_account),
      'gasPrice': w3.eth.gas_price,
      'chainId': chain_id
    })
    print('---------------------->SEND TRANSACTION')
    tx_hash = w3.eth.send_transaction(new_contract_txn)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print('Transaction receipt for new auction method:')
    pprint(dict(tx_receipt))
  except (ValueError, KeyError):
    raise ValueError('Invalid POST parameters')
  return JsonResponse({'result': str(tx_hash.hex())})

@csrf_exempt
def contribute(request):
  try:
    # save account in redis db
    result = json.loads(request.body)
    amount = Web3.toWei(result['amount'], 'ether')
    t = contract.functions.getAuction(result['id']).call()
    print(id, amount, t)
    if (t[5] is True): 
      return JsonResponse({'result': 'Auction already closed.'})
    new_contribution_txn = contract.functions.newOffer(result['id']).buildTransaction({
      'value': amount,
      'nonce': w3.eth.getTransactionCount(w3.eth.default_account),
      'gasPrice': w3.eth.gas_price,
      'chainId': chain_id
    })
    tx_receipt = w3.eth.send_transaction(new_contribution_txn)
    print('Transaction receipt for new contract method:')
    pprint(dict(tx_receipt))
  except (ValueError, KeyError):
    raise ValueError('Invalid POST parameters')
  return JsonResponse({'result': 'ok'})

###############################################################
def get_pending_ended_auctions():
  pending = []
  ended = []
  # check if auction has been completed, and eventually make its status to 'closed'
  num_of_contracts = contract.functions.numAuctions_().call()
  for i in range(num_of_contracts):
    t = contract.functions.getAuction(i).call()
    if (t[5] is True) or (t[2]-time.time() < 0): # auction is completed/ended
      record = AuctionModelForm.objects.filter(id=i).first()
      if record is not None:
        record.status = 'closed' # todo: this is redundant for already closed contracts
      ended.append({'id':i, 'beneficiary':t[0], 'max_offer': t[3], 'deadline':t[4]})
    else:
      print('------------------')
      print(t[2]-time.time())
      print('------------------')
      pending.append({'id':i, 'beneficiary':t[0], 'description':t[1], 'max_offer':t[3], 'bidder':t[4],
                      'deadline':round((t[2]-time.time()))}) # deadline in seconds
  return pending, ended

###############################################################
def homepage(request):
  print('################## PYTHON ###################')
  form = AuctionForm()
  
  pending_auctions, ended_auctions = get_pending_ended_auctions()
  context = {
    "pending_auctions": pending_auctions,
    "ended_auctions": ended_auctions,
    "form": form
  }
  return render(request=request, template_name='app/home.html', context=context)