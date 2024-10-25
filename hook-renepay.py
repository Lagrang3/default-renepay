#!/usr/bin/env python3

from pyln.client import Plugin
import sys
import copy
import os


plugin = Plugin()

def identity(x):
    return x

pay_param_names = ['bolt11', 'amount_msat', 'label', 'riskfactor',
    'maxfeepercent', 'retry_for', 'maxdelay', 'exemptfee', 'localinvreqid',
    'exclude', 'maxfee', 'description', 'partial_msat']

renepay_param_match = {'bolt11': ('invstring', identity), 
    'amount_msat': ('amount_msat', identity),
    'label': ('label', identity),
    'retry_for': ('retry_for', identity),
    'maxdelay': ('maxdelay', identity),
    'exclude': ('exclude', identity),
    'maxfee': ('maxfee', identity),
    'description': ('description', identity),
    # TODO: transform maxfeepercent and exemptfee to maxfee
    }


def param_from_list(param_list, param_names):
    N = len(param_list)
    assert N<=len(param_names)
    param_dict = {}
    for i in range(N):
        name = param_names[i]
        value = param_list[i]
        param_dict[name]=value
    return param_dict

def replace_pay(rpc):
    # change rpc method
    rpc['method']='renepay'
    
    pay_params = {}
    renepay_params = {}
    
    if isinstance(rpc['params'],list):
        # is a list of parameters? transform to dict
        pay_params = param_from_list(rpc['params'], pay_param_names)
    else:
        # otherwise copy
        pay_params = copy.deepcopy(rpc['params'])
    
    # map parameters
    for old_name, old_value in pay_params.items():
        # if this argument has a renepay equivalent we replace
        if old_name in renepay_param_match and old_value is not None:
            name, transf = renepay_param_match[old_name]
            renepay_params[name] = transf(old_value)
        # otherwise we discard
    
    # compulsory argument
    assert 'invstring' in renepay_params
    rpc['params']=renepay_params
    return rpc

@plugin.hook('rpc_command')
def on_pay(plugin, rpc_command, **kwargs):
    """Intercept calls to `pay` forward to `renepay`
    """
    if rpc_command['method'] != 'pay':
        return {'result':'continue'}
    
    # TODO: figure out if renepay is loaded
    has_renepay = True
    # has_renepay = False
    # plug_rpc = plugin.rpc.plugin('list')
    # for p in plug_rpc['plugins']:
    #     name = os.path.basename(p['name'])
    #     if name=='cln-renepay':
    #         has_renepay = True
    #         break
    
    if has_renepay:
        plugin.log("Received call to 'pay': "+str(rpc_command))
        new_rpc = replace_pay(rpc_command)
        plugin.log("Forwarding to 'renepay': "+str(new_rpc))
        return {'replace': new_rpc}
    # else fallback
    return {'result':'continue'}


plugin.run()
