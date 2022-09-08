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
deployed_contract_address = w3.toChecksumAddress("0x54b9B6D9b029786Cdc8Ec43119eCedA7756bE021")
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
w3.eth.default_account = w3.eth.accounts[0]
# w3.toChecksumAddress(client.get("account").decode("utf-8"))
# "0x38773F6e467C15CF7D1CC8BF3D8F971a867Fa82C"
# contract.address
# w3.eth.accounts[0]
print('ACCOUNT : ', w3.eth.default_account)

################################# Methods

from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import time
from pprint import pprint
from .forms import AuctionForm
from .models import AuctionModelForm
import hashlib

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

def saveNewAuction2SQLite():
  # get the latest crated
  num_of_auctions = contract.functions.numAuctions_().call()
  auction = contract.functions.getAuction(num_of_auctions-1).call()
  record = AuctionModelForm.objects.create(
    type = 'new', # redundant
    id = num_of_auctions-1,
    beneficiary = auction[0],
    description = auction[1],
    deadline = auction[2],
    amount = auction[3],
    biggest_for_now = auction[3], # at the beginning the highest bidder is the beneficiary
    highest_bidder = auction[0],
    status = 'pending'
  )
  record.save()
  return

def updateEndedAuction2SQLite(auction, id):
  #update ended auction saved in relational db
  record = AuctionModelForm.objects.filter(id=id).first()
  if record is None:
    sys.exit('Record not found: exiting...')
  record.biggest_for_now = auction[3]
  record.highest_bidder = auction[4]
  record.status = 'closed'
  record.save()
  return

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
    deadline = 60 # [s], set a fixed deadline of +24 hours
    new_contract_txn = contract.functions.newAuction(
      w3.eth.default_account, result['description'], amount, deadline).buildTransaction({
      'nonce': w3.eth.getTransactionCount(w3.eth.default_account),
      'gasPrice': w3.eth.gas_price,
      'chainId': chain_id
    })
    tx_hash = w3.eth.send_transaction(new_contract_txn)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print('Transaction receipt for new auction method:')
    pprint(dict(tx_receipt))
    saveNewAuction2SQLite()
  except (ValueError, KeyError):
    raise ValueError('Invalid POST parameters')
  return JsonResponse({'result': str(tx_hash.hex())})

def send_end_auction_signal(id, auction):
  # Data to be written
  dictionary = {
    "id": id,
    "beneficiary": auction[0],
    "description": auction[1],
    "deadline": auction[2],
    "highestBid": auction[3],
    "highestBidder": auction[4],
    "completed": True
  }
  # Serializing json (from django-redis-project)
  jsoncontent = JsonResponse(dictionary, safe=False)
  # Create the hash
  hash = str(hashlib.sha256(jsoncontent.content).hexdigest())
  # Create transaction
  end_auction_txn = contract.functions.auctionEnd(int(id), hash).build_transaction({
    'nonce': w3.eth.getTransactionCount(w3.eth.default_account),
    'gasPrice': w3.eth.gas_price,
    'chainId': chain_id,
  })
  # Send transaction
  tx_hash = w3.eth.send_transaction(end_auction_txn)
  tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  print('Transaction receipt for end auction method:')
  pprint(dict(tx_receipt))
  # As requested, save in relational databse the result
  updateEndedAuction2SQLite(auction, id)
  return

@csrf_exempt
def contribute(request):
  try:
    # save account in redis db
    result = json.loads(request.body)
    amount = Web3.toWei(int(result['amount']), 'ether')
    id = int(result['id'])
    t = contract.functions.getAuction(id).call()
    print(id, amount, t)
    # if already closed or time is expired
    if (t[5] is True) or (t[2]-time.time() < 0): 
      record = AuctionModelForm.objects.filter(id=i).first()
      if record is not None:
        record.status = 'closed' # todo: this is redundant for already closed contracts
      # if time is over, call ending fucntion (only if auction is not yet labeled as ended)
      if (t[2]-time.time() < 0) and (t[5] is False):
        send_end_auction_signal(id, t)
      return JsonResponse({'result': 'Auction already closed.'})
    new_contribution_txn = contract.functions.newOffer(id).buildTransaction({
      'value': amount,
      'nonce': w3.eth.getTransactionCount(w3.eth.default_account),
      'gasPrice': w3.eth.gas_price,
      'chainId': chain_id
    })
    tx_receipt = w3.eth.send_transaction(new_contribution_txn)
    print('Transaction receipt for new auction method:')
    pprint(dict(tx_receipt))
  except (ValueError, KeyError):
    raise ValueError('Invalid POST parameters')
  return JsonResponse({'result': tx_receipt})

###############################################################
 
def get_pending_ended_auctions():
  pending = []
  ended = []
  # check if auction has been completed, and eventually make its status to 'closed'
  num_of_auctions = contract.functions.numAuctions_().call()
  # for each auction
  for i in range(num_of_auctions):
    t = contract.functions.getAuction(i).call()
    # transform time in readable date
    date = time.ctime(float(t[2]))
    # if already closed or time is expired
    if (t[5] is True) or (t[2]-time.time() < 0):
      record = AuctionModelForm.objects.filter(id=i).first()
      if record is not None:
        record.status = 'closed' # todo: this is redundant for already closed contracts
        print('closed in django')
      # take info directly from blockchain
      ended.append({'id':i, 'beneficiary':t[0], 'max_offer': t[3], 'deadline':date})
      # if time is over, call ending fucntion (only if auction is not yet labeled as ended)
      if (t[2]-time.time() < 0) and (t[5] is False):
        print(i)
        print(t)
        send_end_auction_signal(i, t)
    else:
      pending.append({'id':i, 'beneficiary':t[0], 'description':t[1], 'max_offer':t[3], 'bidder':t[4],
                      'deadline':date})
  return pending, ended

###############################################################
def homepage(request):
  print('################## PYTHON ###################')
  form = AuctionForm()
  if w3.isAddress(w3.eth.default_account):
    print('Using default : ', w3.eth.default_account)
    pending_auctions, ended_auctions = get_pending_ended_auctions()
  else:
    print('Empty')
    pending_auctions = ended_auctions = []
  context = {
    "pending_auctions": pending_auctions,
    "ended_auctions": ended_auctions,
    "form": form
  }
  return render(request=request, template_name='app/home.html', context=context)