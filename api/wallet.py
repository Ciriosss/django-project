from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/3142e3f6eca34a7fb2417781dc7463c6'))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print(f'your adress {address} \nyour key {privateKey} ')