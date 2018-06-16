# Application.py

import os, sys, time
from web3 import Web3

DEBUG_MODE = 1

registrar_address = '0x3C02D620dd4b5310DCe7B9Ce5205b5BE60413E20'
registrar_abi = [{'constant': True, 'inputs': [{'name': '', 'type': 'uint64'}], 'name': 'users', 'outputs': 
				[{'name': 'id_number', 'type': 'uint64'}, {'name': 'accAddr', 'type': 'address'}, {'name': 'RContract', 'type': 'address'}], 
				'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'name': 'id_number', 'type': 'uint64'}], 
				'name': 'getInfo', 'outputs': [{'name': '', 'type': 'address'}, {'name': '', 'type': 'address'}], 
				'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': 
				[{'name': 'id_number', 'type': 'uint64'}, {'name': 'accAddr', 'type': 'address'}, {'name': 'RContract', 'type': 'address'}], 
				'name': 'newRecord', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 
				'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}]

summary_address = '0x734aCB61D837c1e94cb9196dfe0616390e69A2f2'
summary_abi = [{'constant': False, 'inputs': [{'name': 'id_number', 'type': 'uint64'}, {'name': 'ppr', 'type': 'address'}, {'name': 'stt', 'type': 'uint8'}], 
				'name': 'newPPR', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 
				'inputs': [{'name': 'id_number', 'type': 'uint64'}, {'name': 'stt', 'type': 'uint8'}], 'name': 'changeStatus', 'outputs': [], 'payable': False, 
				'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [{'name': 'id_number', 'type': 'uint64'}], 'name': 'getInfo', 
				'outputs': [{'name': '', 'type': 'address'}, {'name': '', 'type': 'uint8'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, 
				{'constant': True, 'inputs': [], 'name': 'ownerAddr', 'outputs': [{'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'view', 
				'type': 'function'}, {'constant': True, 'inputs': [{'name': '', 'type': 'uint64'}], 'name': 'PPR', 'outputs': [{'name': 'id_number', 'type': 'uint64'}, 
				{'name': 'ppr', 'type': 'address'}, {'name': 'stt', 'type': 'uint8'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'inputs': 
				[{'name': 'owner', 'type': 'address'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}]

ppr_address = ''
ppr_abi = []

def send_Ether(obj, receiver, amount):
	# Unlock account
	pwd = input('Password: ')
	obj.eth.defaultAccount = obj.eth.coinbase
	obj.personal.unlockAccount(obj.eth.coinbase, pwd)
	try:
		# Send transaction
		tx_hash = obj.eth.sendTransaction({'from':obj.eth.coinbase, 'to':obj.toChecksumAddress(receiver), 'value': obj.toWei(amount, 'ether')})
		if DEBUG_MODE:
			# Wait for the transaction to be mined, and get the transaction receipt
			tx_receipt = obj.eth.waitForTransactionReceipt(tx_hash)
			print('Current balance: ' + str(obj.fromWei(obj.eth.getBalance(obj.eth.coinbase), 'ether')))
	except:
		print('Not enough money')

def newRecord_transact(obj, account, contract, id_number, accAddr, RC):
	if not type(id_number) == int:
		print('Invalid ID number')
		return
	# Unlock account
	pwd = input('Password: ')
	obj.eth.defaultAccount = account
	obj.personal.unlockAccount(obj.eth.defaultAccount, pwd)
	# Send function transaction
	try:
		# Send transaction
		tx_hash = contract.functions.newRecord(id_number, obj.toChecksumAddress(accAddr), obj.toChecksumAddress(RC)).transact()
		if DEBUG_MODE:
			# Wait for the transaction to be mined, and get the transaction receipt
			tx_receipt = obj.eth.waitForTransactionReceipt(tx_hash)
	except:
		print('No permission or no gas enough')

def getRCInfo_call(contract, id_number):
	if not type(id_number) == int:
		print('Invalid ID number')
		return contract.functions.getInfo(0).call()
	else:
		return contract.functions.getInfo(id_number).call()

def newPPR_transact(obj, account, contract, id_number, ppr, stt):
	if not type(id_number) == int:
		print('Invalid ID number')
		return
	if not type(stt) == int or stt > 1 or stt < 0:
		print('Invalid status')
		return
	# Unlock account
	pwd = input('Password: ')
	obj.eth.defaultAccount = account
	obj.personal.unlockAccount(obj.eth.defaultAccount, pwd)
	try:
		# Send function transaction
		tx_hash = contract.functions.newPPR(id_number, obj.toChecksumAddress(ppr), stt).transact()
		if DEBUG_MODE:
			# Wait for the transaction to be mined, and get the transaction receipt
			tx_receipt = obj.eth.waitForTransactionReceipt(tx_hash)
	except:
		print('No permission or no gas enough')

def changeStt_transact(obj, account, contract, id_number, stt):
	if not type(id_number) == int:
		print('Invalid ID number')
		return
	if not type(stt) == int or stt > 1 or stt < 0:
		print('Invalid status')
		return
	# Unlock account
	pwd = input('Password: ')
	obj.eth.defaultAccount = account
	obj.personal.unlockAccount(obj.eth.defaultAccount, pwd)
	try:
		# Send function transaction
		tx_hash = contract.functions.changeStatus(id_number, stt).transact()
		if DEBUG_MODE:
			# Wait for the transaction to be mined, and get the transaction receipt
			tx_receipt = obj.eth.waitForTransactionReceipt(tx_hash)
	except:
		print('No permission or no gas enough')

def getSCInfo_call(contract, id_number):
	if not type(id_number) == int:
		print('Invalid ID number')
		return contract.functions.getInfo(0).call()
	else:
		return contract.functions.getInfo(id_number).call()

# Test system
def main():
	web3 = Web3(Web3.HTTPProvider('http://localhost:8080', request_kwargs={'timeout': 60}))
	# Check connectrion status
	if web3.isConnected() == False:
		print('Cannot connect to the Ethereum Network')
		return
	else:
		print('Successfully connected to the Ethereum Network')
		print('------------------------------------------------------')
		print('Address: ' + str(web3.eth.coinbase))
		print('Balance: ' + str(web3.fromWei(web3.eth.getBalance(web3.eth.coinbase), 'ether')))
		print('Block number: ' + str(web3.eth.blockNumber))
		print('------------------------------------------------------')

		# Create the contract instance with the newly-deployed address
		registrar = web3.eth.contract(address=registrar_address, abi=registrar_abi)
		summary = web3.eth.contract(address=summary_address, abi=summary_abi)
		#newRecord_transact(web3, registrar, 201690345, '0xc6478021b4ae27831fd6180fb92651bcc1c62e82', '0x734aCB61D837c1e94cb9196dfe0616390e69A2f2')
		#newPPR_transact(web3, web3.eth.accounts[1], summary, 123456789, '0x9dBfb6D87CF66944f99eE11263094D9f08ecB9c9', 1)
		#changeStt_transact(web3, web3.eth.accounts[1], summary, 123456789, 0)
		#print(getSCInfo_call(summary, 123456789))
		return

if __name__ == '__main__':
	main()