"""
                    ****  download contract from etherscan  ****
contract containing source code, abi and bytecode will store in diretory:contractdata
    @ author : liuwang
    @ school : Wuhan University
    @ date   : 2018.10.22
"""

import os
import requests
from pyquery import PyQuery as pq
import logging

# config log file
logging.basicConfig(level=logging.INFO, filename='./logs/download.log',
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    filemode='a', datefmt='%Y-%m-%d%I:%M:%S %p')

# print msg in console and log file
def doLogging(msg):
    print(msg)
    logging.info(msg)
    pass


# https://etherscan.io/contractsVerified/<page_num>
# 25 contracts each etherscan page, totally have 1898 pages in current time
etherScan_url_prefix = 'https://etherscan.io/contractsVerified/'

# https://etherscan.io/address/<code_address>#code
# the page of contract, containing source code, abi and bytecode
code_url_prefix = 'https://etherscan.io/address/'

# the diretory to store source code files
SOURCECODE_DIR = "./contractdata/sourcecode/"

# the diretory to store abi files
ABI_DIR = "./contractdata/abi/"

if not os.path.exists(SOURCECODE_DIR):
    os.makedirs(SOURCECODE_DIR)
    doLogging('create directory {}'.format(SOURCECODE_DIR))
if not os.path.exists(ABI_DIR):
    os.makedirs(ABI_DIR)
    doLogging('create directory {}'.format(ABI_DIR))

# single thread to download contracts from etherscan
# and th page between page_from and page_to.
def downloadContracts(page_from, page_to):
    for page in range(page_from, page_to + 1):
        try:
            addrs = getContractAddressByPageNum(page)
            for addr in addrs:
                try:
                    getCodeAndStore(addr)
                except Exception as e:
                    doLogging(e)
                    continue
        except Exception as e:
            doLogging(e)
    pass

# get the addresses from the page of page_num
# return [(str)address1,(str)address2,...]
def getContractAddressByPageNum(page_num):
    etherScan_url = etherScan_url_prefix + str(page_num)
    try:
        pqObj = pq(requests.get(etherScan_url).content)
    except Exception as e:
        raise Exception("Connected EtherScan page {} error!".format(page_num))
    else:
        addrs = pqObj('.address-tag').text().split(' ')
        doLogging('get Contract addresses in page {} Finished : '.format(page_num))
        return addrs
    pass

# download source code , Abi json code, and bytecode
def getCodeAndStore(addr):
    try:
        codeUrl = code_url_prefix + str(addr) + '#code'
        pqObj = pq(requests.get(codeUrl).content)
    except Exception as e:
        raise Exception("Connected code page error!" + e.__str__())
    else:
        try:
            contractName = getContractName(pqObj)
            sourceCode = getContractSource(pqObj)
            abi = getContractAbi(pqObj)
            sourceFile = open(SOURCECODE_DIR + contractName + '.sol', 'w', encoding='utf-8')
            abiFile = open(ABI_DIR + contractName + '.json', 'w', encoding='utf-8')
            sourceFile.write(sourceCode)
            abiFile.write(abi)
            sourceFile.close()
            abiFile.close()
        except Exception as e:
            raise Exception("Open or write file error!" + e.__str__())
        # Log in console and logfile
        doLogging('downloaded contract:{} at address:{}'.format(contractName, addr))
        pass
    pass

# get the contract name, return a string
def getContractName(pqObj):
    """get the contract name"""
    contractName = pqObj('#ContentPlaceHolder1_contractCodeDiv .col-md-6') \
        .find('td').eq(1).text()
    return contractName

# get the solidity source code
def getContractSource(pqObj):
    """get the solidity source code"""
    sourceCode = pqObj('.js-sourcecopyarea').html()
    return sourceCode.replace('\n', '')

# get the contract abi
def getContractAbi(pqObj):
    """get the contract abi"""
    abi = pqObj('.js-copytextarea2').html()
    return abi

if __name__ == "__main__":
    downloadContracts(1, 1898)
    # getContractSolAbiBytecode('0xef8028b0e68eb6458bdb2c7ba39b39fefea02719')

