# Application.py

import os, sys, time
from web3 import Web3
from tkinter import *

DEBUG_MODE = 1

registrar_address = '0x82C83D67E482729F69C4dBf8eE8885453BCF7E0E'
registrar_abi = [{'constant': True, 'inputs': [{'name': '', 'type': 'uint64'}], 'name': 'users', 'outputs': 
				[{'name': 'id_number', 'type': 'uint64'}, {'name': 'accAddr', 'type': 'address'}, {'name': 'RContract', 'type': 'address'}], 
				'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'name': 'id_number', 'type': 'uint64'}], 
				'name': 'getInfo', 'outputs': [{'name': '', 'type': 'address'}, {'name': '', 'type': 'address'}], 
				'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': 
				[{'name': 'id_number', 'type': 'uint64'}, {'name': 'accAddr', 'type': 'address'}, {'name': 'RContract', 'type': 'address'}], 
				'name': 'newRecord', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 
				'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}]

summary_address = '0x6e98137698A07bb8A7C2CFE1BD5a1292Ceea2B53'
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
	except:
		return 'Not enough money'

def newRecord_transact(obj, account, contract, id_number, accAddr, RC):
	# Unlock account
	pwd = input('Password: ')
	obj.eth.defaultAccount = account
	obj.personal.unlockAccount(obj.eth.defaultAccount, pwd)
	if not type(id_number) == int:
		return 'Invalid ID number'
	# Send function transaction
	try:
		# Send transaction
		tx_hash = contract.functions.newRecord(id_number, obj.toChecksumAddress(accAddr), obj.toChecksumAddress(RC)).transact()
		if DEBUG_MODE:
			# Wait for the transaction to be mined, and get the transaction receipt
			tx_receipt = obj.eth.waitForTransactionReceipt(tx_hash)
	except:
		return 'No permission or no gas enough'

def getRCInfo_call(contract, id_number):
	if not type(id_number) == int:
		return contract.functions.getInfo(0).call()
	else:
		return contract.functions.getInfo(id_number).call()

def newPPR_transact(obj, account, contract, id_number, ppr, stt):
	if not type(id_number) == int:
		return'Invalid ID number'
	if not type(stt) == int or stt > 1 or stt < 0:
		return 'Invalid status'
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
		return 'No permission or no gas enough'

def changeStt_transact(obj, account, contract, id_number, stt):
	if not type(id_number) == int:
		return 'Invalid ID number'
	if not type(stt) == int or stt > 1 or stt < 0:
		return 'Invalid status'
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
		return 'No permission or no gas enough'

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
		# Create the contract instance with the newly-deployed address
		registrar = web3.eth.contract(address=registrar_address, abi=registrar_abi)
		summary = web3.eth.contract(address=summary_address, abi=summary_abi)

		# Send Ether test
		print('\nTest send ether')
		acc1_balance = web3.fromWei(web3.eth.getBalance(web3.eth.accounts[1]), 'ether')
		send_Ether(web3, web3.eth.accounts[1], 5)
		assert(web3.fromWei(web3.eth.getBalance(web3.eth.accounts[1]), 'ether') == (acc1_balance + 5))
		
		# Test create new record
		print('\nTest create new record')
		print('Test #1')
		error = newRecord_transact(web3, web3.eth.accounts[1], 
									registrar, 
									201690345, 
									'0xc6478021b4ae27831fd6180fb92651bcc1c62e82', 
									'0x6e98137698A07bb8A7C2CFE1BD5a1292Ceea2B53')
		assert('No permission or no gas enough' == error)

		print('Test #2')
		error = newRecord_transact(web3, web3.eth.accounts[0], 
									registrar, 
									'hello', 
									'0xc6478021b4ae27831fd6180fb92651bcc1c62e82', 
									'0x6e98137698A07bb8A7C2CFE1BD5a1292Ceea2B53')
		assert('Invalid ID number' == error)

		print('Test #3')
		newRecord_transact(web3, web3.eth.accounts[0], 
								registrar, 
								201690345, 
								'0xc6478021b4ae27831fd6180fb92651bcc1c62e82', 
								'0x6e98137698A07bb8A7C2CFE1BD5a1292Ceea2B53')
		res = getRCInfo_call(registrar, 201690345)
		assert(web3.toChecksumAddress('0xc6478021b4ae27831fd6180fb92651bcc1c62e82') == web3.toChecksumAddress(res[0]))
		assert(web3.toChecksumAddress('0x6e98137698A07bb8A7C2CFE1BD5a1292Ceea2B53') == web3.toChecksumAddress(res[1]))

		#newPPR_transact(web3, web3.eth.accounts[1], summary, 123456789, '0x9dBfb6D87CF66944f99eE11263094D9f08ecB9c9', 1)
		#changeStt_transact(web3, web3.eth.accounts[1], summary, 123456789, 0)
		#print(getSCInfo_call(summary, 123456789))
		return

if __name__ == '__main__':
	main()