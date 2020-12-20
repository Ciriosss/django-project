from web3 import Web3

def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/3142e3f6eca34a7fb2417781dc7463c6'))
    address = '0x2D9b61AD03f892968a9531C86DC39ee3743E47ab'
    privateKey = '0x63dc8067dc2bbd756cbc3a85e61e3acdd1f04e3356b2b3446506407265fb019d'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce = nonce,
        gasPrice = gasPrice,
        gas = 100000,
        to = '0x0000000000000000000000000000000000000000',
        value = value,
        data = message.encode('utf-8')
    ),privateKey)

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return(txId)

