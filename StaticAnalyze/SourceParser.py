'''
--------------------------------------------------------
@File    :   SourceParser.py    
@Contact :   1183862787@qq.com
@License :   (C)Copyright 2017-2018, CS, WHU

@Create Time : 2018/11/24 11:09
@Author      : Liu Wang    
@Version     : 1.0   
@Desciption  : None
--------------------------------------------------------  
''' 

import sys
import os
import re
import numpy as np

def getContentOfBrace(code):
	"""
	:todo: Find the code between '{' and '}'.
	:param: string such as '{ print("hello world"); if(true){do();} } xxxx'.
			Insure that the first letter is '{'.
	:return: the code between '{' and '}'and include them.
	"""
	stack, index_end = 0, 0		# index_end is the matched index of '}'
	for index in range(len(code)):
		if code[index] == '{':
			stack += 1
		elif code[index] == '}':
			stack -= 1
			if stack == 0:
				index_end = index
				break
		else:
			pass
	return code[:index_end+1]

class Variable:
	""""""
	def __init__(self):
		self.var_name = ''
		self.var_authority = ''
		self.type =  ''

class Function:
	""""""
	def __init__(self, name='',params=list(), authority='public', code='', returns=list()):
		self.func_name = name
		self.func_params = params
		self.func_authority = authority
		self.func_code = code
		self.func_returns = returns
		self.__load(code)

	def __load(self, code):
		self.func_params = ''
		self.func_authority = 'public'
		self.func_returns = ''

class SmartContract:
	""""""
	def __init__(self, name='', code=''):
		self._name = name		# str, the name of smart contract
		self._code = code		# '{ .* }'
		self._status_vars = {} 	# status variables of the smart contract. dict:{ var_name : Variable }
		self._funcs = {} 		# function of the smart contract. dict:{ 'func_name': Function }
		self._constructor = None
		self.__load(code)

	def __load(self, code):
		self._status_vars = {}
		self._constructor = None
		self.__parse_functions(code)

	def __parse_functions(self, code):
		function_name_pattern = re.compile(r'function[ ]+?(?:([a-zA-Z_]\w*?)|.*?)\(\).*?\{', re.S)
		match_result = re.search(function_name_pattern, code)
		while match_result != None:
			code = code[match_result.end() - 1:]
			function_name = match_result.group(1)  		# name of matched function
			function_code = getContentOfBrace(code)  	# source code body of matched function
			print(function_name, function_code)
			function = Function(name=function_name,
								code=function_code)		# construct a new Function object
			if function_name == self._name:		# the function is constructor
				self._constructor = function
			else:
				self._funcs[function_name] = function  		# add Function object to self._funcs
			match_result = re.search(function_name_pattern, code)

	def __parse_status_vars(self, code):
		self.__types = ('struct', 'uint', 'address')

	def get_name(self):
		return self._name

	def get_functions(self):
		return self._funcs

	def get_status_variables(self):
		return self._status_vars

	def __str__(self):
		result = 'Name of contract : {}\n'.format(str(self._name))
		result += 'funcs of contract : {}\n'.format(str(self._funcs))
		return result

class Sol:
	"""Object contains messages about source file."""
	def __init__(self, name='', code=''):
		self._name = name		# name of the source file
		self._code = code		# source code in the source file
		self._contracts = {}	# contract in the sol file. dict:{ contracts_name : SmartContract }
		self.__load(self.__remove_comment(code))		# load contracts from comments-removed source code

	def __load(self,code):
		"""
		:todo: load contracts from comments-removed source code
		:param code: comments-removed source code
		:return: None
		"""
		# pattern to match name of smart contract
		contract_name_pattern = re.compile(r'contract[ ]+?([a-zA-Z_]\w*?)[\s]*?\{', re.S)
		match_result = re.search(contract_name_pattern, code)
		while match_result != None:
			code = code[match_result.end()-1:]
			contract_name = match_result.group(1)		# name of matched smart contract
			contract_code = getContentOfBrace(code)		# source code body of match smart contract
			print(contract_name, contract_code)
			contract = SmartContract(name=contract_name,	# construct a new SmartContract object
									 code=contract_code)
			self._contracts[contract_name] = contract		# add SmartContract object to self._contracts
			match_result = re.search(contract_name_pattern, code)


	def __remove_comment(self, source_code):
		"""remove solidity comment from source code"""
		comment_pattern = re.compile(r'(?:(\/\/.*?[\n\r])|(\/\*.*?\*\/))', re.S)
		return re.sub(comment_pattern, '\n', source_code)

	def __str__(self):
		result = ''
		result += 'Name of file : {}\n'.format(str(self._name))
		result += 'Source code without comments : {}\n'.format(str(self._code))
		result += 'Smart contracts : {}'.format(self._contracts)
		return result

class SolPasser:
	""""""
	def __init__(self, path):
		with open(path, encoding='utf-8') as f_sol:
			self.sol = Sol(name=path.split('/')[-1], code=f_sol.read())




if __name__ == '__main__':
	# print(getContentOfBrace('{ print("hello world"); if(true){do();} } xxxx'))
	SolPasser('../Tools/contracttest/sourcecode/BankDoS.sol')

	contract_code = """{
		struct User {
			address addr;
			uint bala;
		}
		address private owner;
		User[] private users;
		constructor() public { owner = msg.sender; }
		function payOut() public {
			for(uint i = 0; i < users.length; ++i){
				uint money = users[i].bala;
				users[i].bala = 0;  // comment
				users[i].addr.transfer(money);
			}
		}
	
		function diposite() payable public {
			users[users.length++] = User({addr:msg.sender, bala:msg.value});
		}
	}"""
	# SmartContract(code=contract_code)