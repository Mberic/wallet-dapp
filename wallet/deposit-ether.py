from web3 import Web3
import json
import web3

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
execLayerData = "Some ether coins"

byte_value = execLayerData.encode() # Convert the string to a byte-like object
hexData = '0x' + byte_value.hex() # Convert to a hex string

transaction = contract.functions.depositEther( CartesiDapp, hexData ).build_transaction( {
    'gasPrice': w3.eth.gas_price, 
    'chainId': 31337, 
    'from': HardhatWalletAddress, 
    'value': 503450,
    'nonce': nonce,  
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key = PrivateKey) # sign the transaction
result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)  
tx_hash = result.hex()

print("Transaction hash: " + tx_hash)
