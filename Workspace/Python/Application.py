# Application.py

import os, sys, time
from web3 import Web3

registrar_address = '0x0d8c9d10Ca79388587AC4F71A425e4952AD49293'
registrar_abi = [{'constant': True, 'inputs': [{'name': '', 'type': 'uint64'}], 'name': 'users', 'outputs': 
				[{'name': 'id_number', 'type': 'uint64'}, {'name': 'accAddr', 'type': 'address'}, {'name': 'RContract', 'type': 'address'}], 
				'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'name': 'id_number', 'type': 'uint64'}], 
				'name': 'getInfo', 'outputs': [{'name': '', 'type': 'address'}, {'name': '', 'type': 'address'}], 
				'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': 
				[{'name': 'id_number', 'type': 'uint64'}, {'name': 'accAddr', 'type': 'address'}, {'name': 'RContract', 'type': 'address'}], 
				'name': 'newRecord', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 
				'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}]
summary_address = ''
summary_abi = []

def send_Ether(obj, receiver, amount):
	# Unlock account
	pwd = input('Password: ')
	obj.eth.defaultAccount = obj.eth.coinbase
	obj.personal.unlockAccount(obj.eth.defaultAccount, pwd)
	try:
		# Send transaction
		tx_hash = obj.eth.sendTransaction({'from':obj.eth.coinbase, 'to':obj.toChecksumAddress(receiver), 'value': obj.toWei(amount, "ether")})
		# Wait for the transaction to be mined, and get the transaction receipt
		tx_receipt = obj.eth.waitForTransactionReceipt(tx_hash)
		print('Current balance: ' + str(obj.fromWei(obj.eth.getBalance(obj.eth.coinbase), 'ether')))
	except:
		print('Not enough money')

def newRecord_transact(obj, contract, id_number, accAddr, RC):
	if not type(id_number) == int:
		print('Invalid ID number')
		return
	# Unlock account
	pwd = input('Password: ')
	obj.eth.defaultAccount = obj.eth.accounts[0]
	obj.personal.unlockAccount(obj.eth.defaultAccount, pwd)
	# Send function transaction
	try:
		tx_hash = contract.functions.newRecord(id_number, obj.toChecksumAddress(accAddr), obj.toChecksumAddress(RC)).transact()
		# Wait for the transaction to be mined, and get the transaction receipt
		tx_receipt = obj.eth.waitForTransactionReceipt(tx_hash)
	except:
		print('No permission')

def getInfo_call(contract, id_number):
	if not type(id_number) == int:
		print('Invalid ID number')
		return contract.functions.getInfo(0).call()
	else:
		return contract.functions.getInfo(id_number).call()

def main():
	web3 = Web3(Web3.HTTPProvider('http://localhost:8080', request_kwargs={'timeout': 60}))
	# Check connectrion status
	if web3.isConnected() == False:
		print('Cannot connect to the Ethereum Network')
	else:
		print('Successfully connected to the Ethereum Network')
		print('------------------------------------------------------')
		print('Address: ' + str(web3.eth.coinbase))
		print('Balance: ' + str(web3.fromWei(web3.eth.getBalance(web3.eth.coinbase), 'ether')))
		print('------------------------------------------------------')

		# Create the contract instance with the newly-deployed address
		registrar = web3.eth.contract(address=registrar_address, abi=registrar_abi)
		#newRecord_transact(web3, registrar, 201690347, '0xc6478021b4ae27831fd6180fb92651bcc1c62e82', '0xc6478021b4ae27831fd6180fabcde1bcc1c62e82')
		#print(getInfo_call(registrar, 201690345))

if __name__ == '__main__':
	main()