# Copyright 2022 Cartesi Pte. Ltd.
#
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from os import environ
import logging
import requests
from web3 import Web3, AsyncWeb3

from eth_account import Account
import json

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

HardhatWalletAddress = Web3.to_checksum_address('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266')
EtherPortal = Web3.to_checksum_address('0xFfdbe43d4c855BF7e0f105c400A50857f53AB044') 
hardhat_rpc_url= 'http://127.0.0.1:8545/'
w3 = Web3(Web3.HTTPProvider(hardhat_rpc_url))

with open("EtherPortal.json") as f:  # load EtherPortal ABI
    info_json = json.load(f)
ABI = info_json

contract = w3.eth.contract(address = EtherPortal, abi = ABI) 

def handle_advance(data):
    logger.info(f"Received advance request data")

    metadata = data["metadata"]
    block = w3.eth.get_block(metadata["block_number"])
    tx_hash = block.transactions[0].hex()
    tx = w3.eth.get_transaction(tx_hash)
    func_obj, func_params = contract.decode_function_input(tx["input"])
    stringMessage = func_params["_execLayerData"].decode('utf-8')
    print(func_params)

    signedData = func_params["_execLayerData"].decode('utf-8')
    raw_transaction = signedData[43:215] # extract raw transaction from signed data
    acct = Account.recover_transaction(raw_transaction)

    if HardhatWalletAddress ==  acct:
        print("\nSignature succefully verified\n")
    else:
        print("\nInvalid signature.\n")

    logger.info("Adding notice")
    notice = {"payload": data["payload"]}
    response = requests.post(rollup_server + "/notice", json=notice)
    logger.info(f"Received notice status {response.status_code} body {response.content}")
    return "accept"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")
    report = {"payload": data["payload"]}
    response = requests.post(rollup_server + "/report", json=report)
    logger.info(f"Received report status {response.status_code}")
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
