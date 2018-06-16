# DeploySummaryContract.py

import os, sys, time
from web3 import Web3
from solc import compile_source

def main():
	web3 = Web3(Web3.HTTPProvider('http://localhost:8080', request_kwargs={'timeout': 60}))
	# Check connectrion status
	if web3.isConnected() == False:
		print('Cannot connect to the Ethereum Network')
	else:
		print('Successfully connected to the Ethereum Network')
		print('------------------------------------------------------')
		contract_name = 'SummaryContract'
		contract_path = os.path.dirname(__file__) + '/../Contracts/' + contract_name + '.sol'
		
		# Check contract file is existed
		if os.path.exists(contract_path) == False:
			print('No contract file')
		else:
			# Read source file
			contract_source = open(contract_path, 'r').read()
			# Compile source code
			compiled_sol = compile_source(contract_source)
			# Get contract interface
			contract_interface = compiled_sol['<stdin>:'+contract_name]
			# Check compiling error
			if contract_interface['abi'] == "" or contract_interface['bin'] == "":
				print('Failed compile source code')
			else:
				# Instantiate and deploy contract
				contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
				# Unlock account
				pwd = input('Password: ')
				web3.eth.defaultAccount = web3.eth.coinbase
				web3.personal.unlockAccount(web3.eth.defaultAccount, pwd)
				# Submit the transaction that deploys the contract
				address = input('Owner address: ')
				tx_hash = contract.constructor(web3.toChecksumAddress(address)).transact()
				# Wait for the transaction to be mined, and get the transaction receipt
				tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

				# Write contract information to file
				file = open(os.path.dirname(__file__) + '/../' + contract_name + '.txt', 'a')
				file.write(contract_name + '\n')
				file.write(tx_receipt.contractAddress + '\n')
				file.write(str(contract_interface['abi']) + '\n\n')
				file.close()
				print('Contract is deployed')

if __name__ == '__main__':
	main()