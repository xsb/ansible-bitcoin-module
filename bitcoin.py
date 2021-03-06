#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: bitcoin
author: "Xavi S.B. @xsb"
short_description: automate bitcoin transactions
description:
  - Automates Bitcoin transactions using a Bitcoin Core full node running locally
options:
  sendtoaddress:
    description:
      - Public bitcoin address
    required: false
    default: null
  amount:
    description:
      - Amount to transact
    required: false
    default: null
  getnewaddress:
    description:
      - Generate a new bitcoin address
    required: false
    default: no
    choices: [ "yes", "no" ]
  getbalance:
    description:
      - Get current wallet balance. "confirmed" expects al least 1 confirmation, "total" is for 0 confirmations.
    required: false
    default: no
    choices: [ "confirmed", "total", "no" ]
  testnet:
    description:
      - If "yes", use testnet instead of mainnet
    required: false
    default: no
    choices: [ "yes", "no" ]
  service_url:
    description:
      - If not specified, the username and password are read out of the file
    required: false
    default: null
  service_port:
    description:
      - The default port is set according to the chain parameters in use: mainnet, testnet
    required: false
    default: null
  btc_conf_file:
    description:
      - If not specified "~/.bitcoin/bitcoin.conf" or equivalent is used by default.
    required: false
    default: null
requirements:
  - "python-bitcoinlib >= 0.5.0"
  - "bitcoind (Bitcoin Core daemon) >= v0.11.0"
'''

EXAMPLES = '''
# Send 0.01 BTC to 1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF
- bitcoin: sendtoaddress=1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF amount=0.01

# Send a transaction using testnet
- bitcoin: sendtoaddress=n1LzM8zxDvtsdTVbc4yeY4vixa2H2uF5Ev amount=0.01 testnet=yes

# Generate new bitcoin address
- bitcoin: getnewaddress=yes

# Get confirmed wallet balance
- bitcoin: getbalance=confirmed
'''

RETURN = '''
txid:
  description: transaction id
  returned: success
  type: string
  sample: f5d8ee39a430901c91a5917b9f2dc19d6d1a0e9cea205b009ca73dd04470b9a6
newaddress:
  description: new bitcoin address
  returned: success
  type: string
  sample: 17Y7ZaAZYF3Gz8Sa9c5UifciVuthWfxx7F
balance:
  description: wallet balance
  returned: success
  type: float
  sample: 1.23965164
'''

from bitcoin import SelectParams, rpc

def amount_convert_from_btc(a):
    """
    Receives an amount in BTC and returns the value in satoshis
    """
    amount = float(a)*100000000
    return amount

def amount_convert_to_btc(a):
    """
    Receives an amount in satoshis and returns the value in BTC
    """
    amount = float(a)/100000000
    return amount

def transaction(m, p, sendtoaddress, amount):
    """
    Sends a standard bitcoin transaction to the network
    """
    txid = ''
    if not m.check_mode:
        txid = p.sendtoaddress(sendtoaddress, amount)
    return txid

def getnewaddress(m, p):
    """
    Generates a new bitcoin address
    """
    address = ''
    if not m.check_mode:
        address = str(p.getnewaddress())
    return address

def getbalance(p, balance_type):
    """
    Get current balance
    """
    if balance_type == 'confirmed':
        balance = p.getbalance(minconf=1)
    elif balance_type == 'total':
        balance = p.getbalance(minconf=0)
    return amount_convert_from_btc(balance)

def main():

    module = AnsibleModule(
        argument_spec = dict(
            sendtoaddress = dict(required=False, default=None, type='str'),
            amount        = dict(required=False, default=None, type='str'),
            getnewaddress = dict(required=False, default='no', choices=['yes', 'no']),
            getbalance    = dict(required=False, default='no', choices=['confirmed', 'total', 'no']),
            testnet       = dict(required=False, default='no', choices=['yes', 'no']),
            service_url   = dict(required=False, default=None, type='str'),
            service_port  = dict(required=False, default=None, type='int'),
            btc_conf_file = dict(required=False, default=None, type='str'),
        ),
        supports_check_mode = True
    )

    p = module.params

    if p['testnet'] == 'yes':
        SelectParams("testnet")
    else:
        SelectParams("mainnet")

    proxy = rpc.Proxy(
        p['service_url'],
        p['service_port'],
        p['btc_conf_file']
    )

    result = {}
    result['changed'] = False

    if p['sendtoaddress'] and p['amount']:
        sendtoaddress = p['sendtoaddress']
        amount = amount_convert_from_btc(p['amount'])

        result['sendtoaddress'] = sendtoaddress
        result['amount'] = p['amount']

        try:
            txid = transaction(module, proxy, sendtoaddress, amount)
            result['changed'] = True
            result['txid'] = txid.encode("hex")
        except Exception as e:
            module.fail_json(msg=str(e), changed=False, sendtoaddress=sendtoaddress, amount=p['amount'])

    if p['getnewaddress'] == 'yes':
        try:
            newaddress = getnewaddress(module, proxy)
            result['changed'] = True
            result['newaddress'] = newaddress
        except Exception as e:
            module.fail_json(msg=str(e), changed=False)

    if p['getbalance'] != 'no':
        try:
            balance = getbalance(proxy, p['getbalance'])
            result['balance'] = balance
        except Exception as e:
            module.fail_json(msg=str(e), changed=False)

    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
