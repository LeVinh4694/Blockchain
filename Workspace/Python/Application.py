# Application.py

import os, sys, time
from web3 import Web3
from tkinter import *

DEBUG_MODE = 1

class HealthCare:
	def __init__(self, obj, debug):
		self.DEBUG_MODE = debug
		self.obj = obj

		self.registrar_address = '0x64070232d0aC078a12E5839B4112ABc8ca31D932'
		self.registrar_abi = [{'constant': True, 'inputs': [{'name': '', 'type': 'uint64'}], 'name': 'users', 'outputs': 
							[{'name': 'id_number', 'type': 'uint64'}, {'name': 'accAddr', 'type': 'address'}, {'name': 'RContract', 'type': 'address'}], 
							'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'name': 'id_number', 'type': 'uint64'}], 
							'name': 'getInfo', 'outputs': [{'name': '', 'type': 'address'}, {'name': '', 'type': 'address'}], 
							'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': 
							[{'name': 'id_number', 'type': 'uint64'}, {'name': 'accAddr', 'type': 'address'}, {'name': 'RContract', 'type': 'address'}], 
							'name': 'newRecord', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 
							'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}]

		self.summary_address = '0x6e98137698A07bb8A7C2CFE1BD5a1292Ceea2B53'
		self.summary_abi = [{'constant': False, 'inputs': [{'name': 'id_number', 'type': 'uint64'}, {'name': 'ppr', 'type': 'address'}, {'name': 'stt', 'type': 'uint8'}], 
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

		# Create the contract instance with the newly-deployed address
		self.registrar = self.obj.eth.contract(address=self.registrar_address, abi=self.registrar_abi)					

	def send_Ether(self, receiver, amount):
		# Unlock account
		if not DEBUG_MODE:
			self.pwd = input('Password: ')
		else:
			self.pwd = '123456'
		self.obj.personal.unlockAccount(self.obj.eth.coinbase, self.pwd)

		if not self.obj.isAddress(receiver):
			return 'Invalid address'

		try:
			# Send transaction
			self.tx_hash = self.obj.eth.sendTransaction({'from':self.obj.eth.coinbase, 
													'to':self.obj.toChecksumAddress(receiver), 
													'value': self.obj.toWei(amount, 'ether')})
			if self.DEBUG_MODE:
				# Wait for the transaction to be mined, and get the transaction receipt
				self.tx_receipt = self.obj.eth.waitForTransactionReceipt(self.tx_hash)
			return 'OK'
		except:
			return 'Invalid value'

	def newRecord(self, account, id_number, accAddr, RC):
		# Unlock account
		if not DEBUG_MODE:
			self.pwd = input('Password: ')
		else:
			self.pwd = '123456'

		if not self.obj.isAddress(account) or \
		   not self.obj.isAddress(accAddr) or \
		   not self.obj.isAddress(RC):
			return 'Invalid address'
		if not type(id_number) == int:
			return 'Invalid ID number'

		self.obj.eth.defaultAccount = self.obj.toChecksumAddress(account)
		self.obj.personal.unlockAccount(self.obj.eth.defaultAccount, self.pwd)

		try:
			# Send transaction
			self.tx_hash = self.registrar.functions.newRecord(id_number, 
														self.obj.toChecksumAddress(accAddr), 
														self.obj.toChecksumAddress(RC)).transact()
			if self.DEBUG_MODE:
				# Wait for the transaction to be mined, and get the transaction receipt
				self.tx_receipt = self.obj.eth.waitForTransactionReceipt(self.tx_hash)
			return 'OK'
		except:
			return 'Wrong owner'

	def getRCInfo(self, id_number):
		if not type(id_number) == int:
			return 'Invalid ID number'
		else:
			return self.registrar.functions.getInfo(id_number).call()

# Test system
def main():
	web3 = Web3(Web3.HTTPProvider('http://localhost:8545', request_kwargs={'timeout': 60}))
	# Check connectrion status
	if web3.isConnected() == False:
		print('Cannot connect to the Ethereum Network')
		return 
	else:
		healthcare = HealthCare(web3, 1)

		# Test send ether
		print('TEST SEND ETHER FUNCTION')
		print('-----------------------------------------')
		print('Test #1: Invalid address')
		ret = healthcare.send_Ether('0x172e212b63f9fdc767705739ee746f2315bd0d86a', 5)
		assert('Invalid address' == ret)
		print('Passed')
		print('Test #2: Invalid value')
		ret = healthcare.send_Ether('0x172e212b63f9fdc767705739ee746f2315bd0d86', 'a')
		assert('Invalid value' == ret)
		print('Passed')
		print('Test #3: correct address & value')
		balance = web3.fromWei(web3.eth.getBalance(web3.eth.accounts[1]), 'ether')
		ret = healthcare.send_Ether('0x172e212b63f9fdc767705739ee746f2315bd0d86', 5)
		assert('OK' == ret)
		assert((balance + 5) == web3.fromWei(web3.eth.getBalance(web3.eth.accounts[1]), 'ether'))
		print('Passed')

		# Test registrar contract
		print('\nTEST NEW RECORD FUNCTION')
		print('-----------------------------------------')
		print('Test #4: Invalid address')
		ret = healthcare.newRecord('0x0f8cccddbd89be8029df82ad4f5706a0b63067eba', 201690345, 
									'0x172e212b63f9fdc767705739ee746f2315bd0d86', 
									'0x64070232d0aC078a12E5839B4112ABc8ca31D93A')
		assert('Invalid address' == ret)
		print('Passed')
		ret = healthcare.newRecord('0x0f8cccddbd89be8029df82ad4f5706a0b63067eb', 201690345, 
									'0x172e212b63f9fdc767705739ee746f2315bd0d86a', 
									'0x64070232d0aC078a12E5839B4112ABc8ca31D93A')
		assert('Invalid address' == ret)
		print('Passed')
		ret = healthcare.newRecord('0x0f8cccddbd89be8029df82ad4f5706a0b63067eb', 201690345, 
									'0x172e212b63f9fdc767705739ee746f2315bd0d86', 
									'0x64070232d0aC078a12E5839B4112ABc8ca31D93Aa')
		assert('Invalid address' == ret)
		print('Passed')
		print('Test #5: Invalid id number')
		ret = healthcare.newRecord(web3.eth.coinbase, 'hello', 
									'0x172e212b63f9fdc767705739ee746f2315bd0d86', 
									'0xe19B16284c572E55DFd7d6d05AC22b19Cf622Fa9')
		assert('Invalid ID number' == ret)
		print('Passed')
		print('Test #6: Correct value but wrong owner')
		ret = healthcare.newRecord(web3.eth.accounts[1], 201690345, 
									'0x172e212b63f9fdc767705739ee746f2315bd0d86', 
									'0xe19B16284c572E55DFd7d6d05AC22b19Cf622Fa9')
		assert('Wrong owner' == ret)
		print('Passed')
		print('Test #7: Correct value')
		ret = healthcare.newRecord(web3.eth.coinbase, 201690345, 
									'0x172e212b63f9fdc767705739ee746f2315bd0d86', 
									'0xe19B16284c572E55DFd7d6d05AC22b19Cf622Fa9')
		assert('OK' == ret)
		ret = healthcare.getRCInfo(201690345)
		assert(web3.toChecksumAddress('0x172e212b63f9fdc767705739ee746f2315bd0d86') == web3.toChecksumAddress(ret[0]))
		assert(web3.toChecksumAddress('0xe19B16284c572E55DFd7d6d05AC22b19Cf622Fa9') == web3.toChecksumAddress(ret[1]))
		print('Passed')

if __name__ == '__main__':
	main()