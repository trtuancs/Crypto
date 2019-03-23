#!/usr/bin/python3

from Crypto import Random
from Crypto.Cipher import Blowfish
import os

class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (Blowfish.block_size - len(s) % Blowfish.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(Blowfish.block_size)
        cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:Blowfish.block_size]
        cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[Blowfish.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

file_key = open(input("Open key: "),"r")
key_ = file_key.readline()
key = key_.encode()
if (len(key) in range(4,57)):
    enc = Encryptor(key)

    choice = int(input(
            "1. Press '1' to encrypt file.\n2. Press '2' to decrypt file.\n3. Press '3' to exit.\n"))
    if choice == 1:
        enc.encrypt_file(str(input("Enter name of file to encrypt: ")))
    elif choice == 2:
        enc.decrypt_file(str(input("Enter name of file to decrypt: ")))
    elif choice == 3:
        exit()
    else:
        print("Please select a valid option!")
else:
    print("Error key.Length of key must be in range (4,57)")