from web3 import Web3
import json

HARDHAT_DEFAULT_RPC_URL = 'http://127.0.0.1:8545'

HardhatWalletAddress = Web3.to_checksum_address('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266')
PrivateKey = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'

EtherPortal = Web3.to_checksum_address('0xFfdbe43d4c855BF7e0f105c400A50857f53AB044') 
CartesiDapp = Web3.to_checksum_address('0x70ac08179605AF2D9e75782b8DEcDD3c22aA4D0C')

w3 = Web3(Web3.HTTPProvider(HARDHAT_DEFAULT_RPC_URL))

with open("EtherPortal.json") as f:  # load EtherPortal ABI
    info_json = json.load(f)
ABI = info_json

contract = w3.eth.contract(address = EtherPortal, abi = ABI) # Instantiate smart contract 
nonce = w3.eth.get_transaction_count(HardhatWalletAddress)  

transaction = { # txn to be processed by wallet DApp on execution layer (i.e Cartesi node)
    'gas': 25000000,
    'gasPrice': 450000, 
    'chainId': 48750, # arbitrary chainID to mean Cartesi network
    'from': HardhatWalletAddress, 
    'value': 5,
    'nonce': nonce,  
}

signed = w3.eth.account.sign_transaction(transaction, PrivateKey)
msg = str(signed)

byte_value = msg.encode() # Convert the string to a byte-like object
txn_info = '0x' + byte_value.hex() # Convert to a hex string

transaction = contract.functions.depositEther( CartesiDapp, txn_info ).build_transaction( {
    'gasPrice': w3.eth.gas_price, 
    'chainId': 31337, 
    'from': HardhatWalletAddress, 
    'value': 3,
    'nonce': nonce,  
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key = PrivateKey) # sign the transaction
result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)  
tx_hash = result.hex()

print(tx_hash)

