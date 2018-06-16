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

def newRecord_transact(obj, contract, id_number, accAddr, RC):
	# Unlock account
	pwd = input('Password: ')
	obj.eth.defaultAccount = obj.eth.coinbase
	obj.personal.unlockAccount(obj.eth.defaultAccount, pwd)
	# Send function transaction
	tx_hash = contract.functions.newRecord(id_number, obj.toChecksumAddress(accAddr), obj.toChecksumAddress(RC)).transact()
	# Wait for the transaction to be mined, and get the transaction receipt
	tx_receipt = obj.eth.waitForTransactionReceipt(tx_hash)

def getInfo_call(contract, id_number):
	return contract.functions.getInfo(id_number).call()

def main():
	web3 = Web3(Web3.HTTPProvider('http://localhost:8080', request_kwargs={'timeout': 60}))
	# Check connectrion status
	if web3.isConnected() == False:
		print('Cannot connect to the Ethereum Network')
	else:
		print('Successfully connected to the Ethereum Network')
		print('------------------------------------------------------')

		# Create the contract instance with the newly-deployed address
		registrar = web3.eth.contract(address=registrar_address, abi=registrar_abi)
		#newRecord_transact(web3, registrar, 201690345, '0xc6478021b4ae27831fd6180fb92651bcc1c62e82', '0xc6478021b4ae27831fd6180fabcde1bcc1c62e82')
		print(getInfo_call(registrar, 201690346))

if __name__ == '__main__':
	main()