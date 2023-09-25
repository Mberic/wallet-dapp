from web3 import Web3, AsyncWeb3
import json

HARDHAT_DEFAULT_RPC_URL = 'http://localhost:8545/'
INPUT_BOX = '0x59b22D57D4f067708AB0c00552767405926dc768'
CARTESI_DAPP = '0x70ac08179605AF2D9e75782b8DEcDD3c22aA4D0C'

HARDHAT_WALLET_ADDRESS = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
PRIVATE_KEY = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
 
w3 = Web3(Web3.HTTPProvider(HARDHAT_DEFAULT_RPC_URL))

with open("InputBox.json") as f:  # load InputBox ABI
    info_json = json.load(f)
ABI = info_json

contract = w3.eth.contract(address = INPUT_BOX, abi = ABI) # Instantiate smart contract 
nonce = w3.eth.get_transaction_count(HARDHAT_WALLET_ADDRESS)  

msg = 'token_balances'

byte_value = msg.encode() # Convert the string to a byte-like object
inputBytes = '0x' + byte_value.hex() # Convert to a hex string

transaction = contract.functions.addInput(CARTESI_DAPP, inputBytes).build_transaction( {
    "gasPrice": w3.eth.gas_price, 
    "chainId": 31337, 
    "from": HARDHAT_WALLET_ADDRESS, 
    "nonce": nonce, 
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key = PRIVATE_KEY) # sign the transaction
result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)  

print("Transaction: " + result.hex())
