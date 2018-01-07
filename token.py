#!/usr/bin/env python3

import hashlib
import random
import json
import os
import binascii
import time

class Token:

	# expire Token : 60s 
	# function     : @dump   , @load
	# @dump        : take ( text )  lik mail,username,passowrd  return str( Token ) 
	# @load        : take ( Token ) return ( Text For the Token ) 


	def __init__(self):

		# Read JsonFile 
		self.token_file = open("token.json","r+").read()
		# Time 
		self.t = time.strftime("%H:%M:%S",time.localtime())

	def uptime(self):
		self.t = time.strftime("%H:%M:%S",time.localtime())

	def upJson(self):
		self.token_file = open("token.json","r").read()

	def dump(self,db):
		self.upJson()
		self.uptime()

		tk       = {}

		# ENCODE 
		dbt      = hashlib.md5(hashlib.sha224(db.encode("u8")).digest()).digest()
		urange   = binascii.b2a_base64(os.urandom(random.randint(20,50))+dbt).strip(b"\n")
		token    = hashlib.md5(urange).hexdigest()

		# Time Create Token 
		time_crate     = self.t.split(":")
		time_crate[-1] = str(60-int(time_crate[-1]))

		# IF file.json is empty
		if self.token_file != "":

			tk = json.loads(self.token_file)
			# add To JSON 
			tk[token] = (db,":".join(time_crate))

		else:

			tk[token] = (db,":".join(time_crate))

		# Write in File JSON 
		open("token.json","w").write(json.dumps(tk,indent=4))


		return token 

	def load(self,token):
		# IF file.json is empty
		self.upJson()
		self.uptime()

		if self.token_file != "":
			# get From JSON 
			tk = json.loads(self.token_file)
			tkg = tk.get(token)

			if tkg != None:
				# chack expire 
				if tkg[1] < self.t:

					del tk[token]
					open("token.json","w").write(json.dumps(tk,indent=4))

					return None

				return tkg[0]

			return tkg

