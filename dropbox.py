#Rekha Tattamangalam Rajan
#1001164021
__author__ = 'Rekha'

import dropbox
import gnupg
import os
import time

gpg = gnupg.GPG(gnupghome='C:\Python27\gnu')
client = dropbox.client.DropboxClient('a_LLbo94HwAAAAAAAAALI0oqHXlAXhC49t-uRqS9O2Bn_hggxzPLlQGxRrdQXSqy')
#Monitored folder
folder_path = r'F:\CSE6331\cloud'

#sender and receiver parameters
sender_param = {
    'Key-Type': 'DSA',
    'Key-Length': 1024,
    'Passphrase': 'sender',
    'Subkey-Type': 'ELG-E',
    'Subkey-Length': 2048,
    'Name-Real': 'sender',
    'Name-Email': 'sender@uta.edu',
    'Expire-Date': 0,
}

receiver_param = {
    'Key-Type': 'DSA',
    'Key-Length': 1024,
    'Passphrase': 'receiver',
    'Subkey-Type': 'ELG-E',
    'Subkey-Length': 2048,
    'Name-Real': 'receiver',
    'Name-Email': 'receiver@uta.edu',
    'Expire-Date': 0,
}

#Generating key for sender and receiver
sender = gpg.gen_key_input(**sender_param)
senderkey = gpg.gen_key(sender)
#print senderkey

receiver = gpg.gen_key_input(**receiver_param)
receiverkey = gpg.gen_key(receiver)
#print receiverkey

print "Keys generated for sender and receiver"
print "Monitoring folder for files.."

#check folders/files already present
folder_bef = dict([(f, None) for f in os.listdir(folder_path)])

while 1:
    #check every 10 seconds
    time.sleep(10)
    folder_aft = dict([(f, None) for f in os.listdir(folder_path)])
    file_added = [f for f in folder_aft if not f in folder_bef]
    file_removed = [f for f in folder_bef if not f in folder_aft]
    #if new file added
    if file_added:
        localdropboxpath = folder_path + "\\" + ",".join(file_added)
        #open the file
        file = open(localdropboxpath)
        #encrypt the file and sign, encryption happens using receivers' key and digital signature happens using senders' key
        encrypted_file = gpg.encrypt_file(file, receiverkey, sign=senderkey, passphrase='sender',
                                     output=r'F:\CSE6331\cloud1\encr.txt')
        #open the encrypted file
        f = open(r"F:\CSE6331\cloud1\encr.txt", 'rb')
        #put the signed and encrypted file in dropbox
        response = client.put_file('/encrypted_file.txt', f)
        file.close()
        f.close()
        print "File uploaded"
    #if file removed
    if file_removed:
        #download the file from dropbox
        fd, metadata = client.get_file_and_metadata('/encrypted_file.txt')
        # open the file in write mode
        out = open(r"F:\CSE6331\cloud1\decrypted_file.txt", 'wb')
        out.write(fd.read())
        out.close()
        out1 = open(r'F:\CSE6331\cloud1\decrypted_file.txt', 'r').read()
        # verify the file with passphrase and decrypt it
        decrypted = gpg.decrypt(out1, passphrase='receiver', output=r'F:\CSE6331\cloud1\decrypted_file.txt')
        print "File verified and decrypted."
    folder_bef = folder_aft

"""
References:
https://www.dropbox.com/developers/core/start/python
http://python-gnupg.readthedocs.org/en/latest/gnupg.html
https://pythonhosted.org/python-gnupg/
"""