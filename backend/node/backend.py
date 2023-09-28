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
import json

from web3 import Web3
from eth_account import Account
from eth_abi_ext import decode_packed

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

HardhatWalletAddress = Web3.to_checksum_address('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266')
EtherPortal = Web3.to_checksum_address('0xFfdbe43d4c855BF7e0f105c400A50857f53AB044') 
ERC20Portal= Web3.to_checksum_address('0x9C21AEb2093C32DDbC53eEF24B873BDCd1aDa1DB')
ERC721Portal= Web3.to_checksum_address('0x237F8DD094C0e47f4236f12b4Fa01d6Dae89fb87')
ERC1155SinglePortal= Web3.to_checksum_address('0x7CFB0193Ca87eB6e48056885E026552c3A941FC4')

ether_balance = 0
erc20_balance = 0
erc1155_balance = 0

def handle_advance(data):
    logger.info(f"Received advance request data")
    decode_payload(data)

    logger.info("Adding notice")
    notice = {"payload": data["payload"]}
    response = requests.post(rollup_server + "/notice", json=notice)
    logger.info(f"Received notice status {response.status_code} body {response.content}")
    return "accept"

def decode_payload(data):

    metadata = data["metadata"]
    msg_sender = metadata["msg_sender"]
    payload = data["payload"]

    if Web3.to_checksum_address(msg_sender) == EtherPortal:
        binary = bytes.fromhex(payload[2:])
        decoded = decode_packed(['address','uint256'],binary)
        print('Transaction info: ' + str(decoded))
    elif Web3.to_checksum_address(msg_sender) == ERC20Portal:
        binary = bytes.fromhex(payload[2:])
        decoded = decode_packed(['bool','address','address','uint256'],binary)
        global erc20_balance
        erc20_balance += amount
        print('Transaction info: ' + str(decoded))
    elif Web3.to_checksum_address(msg_sender) == ERC721Portal:
        binary = bytes.fromhex(payload[2:])
        decoded = decode_packed(['address','address','uint256'],binary)
        print('Transaction info: ' + str(decoded))
    elif Web3.to_checksum_address(msg_sender) == ERC1155SinglePortal:
        binary = bytes.fromhex(payload[2:])
        decoded = decode_packed(['address', 'address', 'uint25', 'uint256'],binary)
        global erc1155_balance 
        erc1155_balance += erc115value
        print('Transaction info: ' + str(decoded))
    elif Web3.to_checksum_address(msg_sender) == HardhatWalletAddress:
        dapp_msg = bytes.fromhex(payload[2:]).decode()

        if dapp_msg == 'token_balances':
            balance_check()
        else:
            print("Unknown DApp message")
            print("Message : " + dapp_msg)

def balance_check():
        print("\nEther Balance: " + str(ether_balance))
        print("ERC20 Balance: " + str(erc20_balance))
        print("ERC1155 Balance: " + str(erc1155_balance) + "\n")
    
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
