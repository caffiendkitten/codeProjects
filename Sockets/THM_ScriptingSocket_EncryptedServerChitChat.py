#!/usr/bin/env python
# This script was built for TryHackMe Scripting room[Task 3] [Hard] Encrypted Server Chit Chat

# This script will connect to a socket, send a message, and set a few veriables.
# It will then recursivly send a new message(s) to test if the returned value is the desired flag and 
# the checksum matches

import os
import base64
import hashlib
import socket
import re
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

# Change HOST to the victim machine"
HOST="x.x.x.x"
PORT = 4000
serverAddress = HOST, PORT
bufferSize  = 2048


try:
	UDPs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	UDPs.connect((HOST, int(PORT)))
	print("connected to UDP server", serverAddress)

	message = b"ready"
	UDPs.sendto(message, serverAddress)
	response = UDPs.recv(bufferSize)
	data = response.split(b' ')

	key1 = str(data[0]).strip("b\'").split(":")[1]
	key = bytes(key1, 'utf-8')
	print("Key is: ", data[0])

	iv1 = str(data[1]).strip("b\'").split(":")[1]
	iv = bytes(iv1, 'utf-8')
	print("IV is: ",iv1)

	Checksum = data[14]
	print("Checksum: ",Checksum)


	hashCheck = base64.b16encode(Checksum).lower()
	print("HashCheck: ",hashCheck)

	while True:
		finalMessage = b"final"
		UDPs.send(finalMessage)
		flag = UDPs.recv(bufferSize)
		# flag = bytes(flag)
		print("Flag is: ",flag)

		UDPs.send(finalMessage)
		tag = UDPs.recv(bufferSize)		
		print("Tag is: ",tag)

		try:
			decryptor = Cipher(algorithms.AES(key), modes.GCM(iv, bytes(tag)), backend=default_backend()).decryptor()
			messageDe = decryptor.update(bytes(flag)) + decryptor.finalize()
			# print("decrypted message is: ", str(messageDe).strip("b\'"))
			# break
		except:
			print("error encrypting: nope")

		hash_object = hashlib.sha256(messageDe)
		hash_object = hash_object.hexdigest()
		# print("hash Flag: ",hash_object)
		if hashCheck == hash_object.encode():

			print("Final Flag is: ", str(messageDe).strip("b\'"))
			break
		else:
			continue
	UDPs.close()
except socket.error as err:
	print(err)
	UDPs.close()
