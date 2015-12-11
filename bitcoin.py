#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: bitcoin
author: "Xavi S.B. @xavi_xsb"
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
requirements:
  - "python-bitcoinlib >= 0.5"
  - "bitcoind (bitcoin-core daemon)"
'''

EXAMPLES = '''
# Send 0.01 BTC to 1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF
- bitcoin: sendtoaddress=1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF amount=0.01
'''

import bitcoin

def send_transaction(module):
    cmd = "bitcoin-cli sendtoaddress %s %s" % (module.params['sendtoaddress'], module.params['amount'])
    return module.run_command(cmd)

def main():

    module = AnsibleModule(
        argument_spec = dict(
            sendtoaddress = dict(required=True, type='str'),
            amount = dict(required=True, type='str'),
        ),
        supports_check_mode = False
    )

    rc = None
    out = ''
    err = ''
    result = {}
    result['sendtoaddress'] = module.params['sendtoaddress']
    result['amount'] = module.params['amount']

    (rc, out, err) = send_transaction(module)
    if rc != 0:
        module.fail_json(sendtoaddress=module.params['sendtoaddress'], amount=module.params['amount'], msg=err, rc=rc)

    if rc is None:
        result['changed'] = False
    else:
        result['changed'] = True
    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err

    module.exit_json(**result)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
