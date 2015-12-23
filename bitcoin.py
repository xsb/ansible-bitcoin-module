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
    required: true
  amount:
    description:
      - Amount to transact
    required: true
  testnet:
    description:
      - If true, use testnet instead of mainnet
    required: false
    default: false
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
- bitcoin: sendtoaddress=1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF amount=0.01 testnet=true
'''

RETURN = '''
txid:
  description: transaction id
  returned: success
  type: string
  sample: f5d8ee39a430901c91a5917b9f2dc19d6d1a0e9cea205b009ca73dd04470b9a6
'''

from bitcoin import SelectParams, rpc

def main():

    module = AnsibleModule(
        argument_spec = dict(
            sendtoaddress = dict(required=True, type='str'),
            amount = dict(required=True, type='str'),
            testnet = dict(required=False, default=False, type='bool'),
            service_url = dict(required=False, default=None, type='str'),
            service_port = dict(required=False, default=None, type='int'),
            btc_conf_file = dict(required=False, default=None, type='str'),
        ),
        supports_check_mode = True
    )

    if module.params['testnet']:
        SelectParams("testnet")
    else:
        SelectParams("mainnet")

    proxy = rpc.Proxy(
            module.params['service_url'],
            module.params['service_port'],
            module.params['btc_conf_file']
    )

    sendtoaddress = module.params['sendtoaddress']
    raw_amount = module.params['amount']
    amount = float(raw_amount)*100000000

    err = ''
    txid = ''
    result = {}
    result['sendtoaddress'] = sendtoaddress
    result['amount'] = raw_amount

    if not module.check_mode:
        try:
            txid = proxy.sendtoaddress(sendtoaddress, amount)
        except Exception as e:
            err = str(e)

    if err:
        module.fail_json(sendtoaddress=sendtoaddress, amount=raw_amount, msg=err)
        result['changed'] = False
    else:
        result['txid'] = txid.encode("hex")
        result['changed'] = True

    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
