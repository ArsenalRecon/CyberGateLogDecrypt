

import sys
import re
import codecs


### KEY ###
# Set your decryption key. If you do not know what the decryption key is, 
# it appears to be a 38 character string. See description above for attacking this key
KEY = b"""PUTYOURKEYHERE"""
### KEY ###


### Code Page ###
# Set your code page if
# dealing with non US/ASCII
DecodePage='ascii'
EncodePage='ascii'
### Code Page ###


### getMessage ###
# getMessage
# inputs, the key, the cipher text and a file handle
# returns the decrypted plaintext, writes plaintext to file
###
def getMessage(key, cipher, FH):
    i = 0
    DEBUG = False
    #Debug flag, can leave False most of the time
    print ("\n[*] cipher:",cipher)

    ## write new entry header..
    FH.write(b'####')
    ### while i < len(key) ###
    # allows us to cycle through they key
    # if your ciphertext is longer than our
    # key.
    ###
    while i < len(key):
        tmpKey = key[i:]
        if i > 0:
            tmpKey += key[:i]
        message = bytearray()
        j = 0
        k = 0
        print ("[*] key:",tmpKey)
        printableChars = 32
        ### while j < len(cipher) ###
        # keep track of the character offset in the cipher
        ###
        while j < len(cipher):
            if (cipher[j]) == 10 or (cipher[j]) == 13:
            	##if the current cipher character is a newline
            	## skip it
                k = k + 2
                j = j + 2
                if DEBUG:
                    print ("CR/LF")
                message.append(10)
                try:
	                FH.write(b'\x0a')
                except Exception as e:
                	print ("...")
                	print (e)
                continue
            if DEBUG:
                 print (chr(cipher[j]),"(",cipher[j],")\t", chr(tmpKey[k%len(tmpKey)]),"(",tmpKey[k%len(tmpKey)],")", "\t-->\t", chr(cipher[j] ^ tmpKey[k%len(tmpKey)]),"(",cipher[j] ^ tmpKey[j%len(tmpKey)],")"),
            if cipher[j] ^ tmpKey[j%len(tmpKey)] < 32:
            	## if cipher text character is < 32 (non printable character)
            	## bump it's value by 32 to get to where we should be
                try:
                    FH.write( ( (cipher[j]^tmpKey[j%len(tmpKey)])+32).to_bytes(1,'little').decode(DecodePage).encode(EncodePage))
                    message.append((cipher[j]^tmpKey[j%len(tmpKey)])+32)
                except Exception as e:
                    print(e)
                if DEBUG:
                	print ("\t-->\t", chr((cipher[j]) ^ (tmpKey[k%len(tmpKey)])+32),"(",(cipher[j] ^ (tmpKey[k%len(tmpKey)]))+32,")")
            elif (cipher[j] ^ tmpKey[j%len(tmpKey)]) > 127 and (cipher[j] ^ tmpKey[j%len(tmpKey)]) < 192:
            	## if cipher text character is 127 < N < 192, then
            	## it's also a non-printable character
            	## bump it by 64
                message.append((cipher[j] ^ tmpKey[k%len(tmpKey)])+64)
                try:
                    FH.write(((cipher[j]^tmpKey[j%len(tmpKey)])+64).to_bytes(1,'little').decode(DecodePage).encode(EncodePage))            	
                except Exception as e:
                    print ("64")
                if DEBUG:
                	print ("\t-->\t", chr((cipher[j]) ^ (tmpKey[k%len(tmpKey)])+64),"(",(cipher[j] ^ (tmpKey[k%len(tmpKey)]))+64,")")
            else:
                ## else, our character falls into the pritable character range
	            try:
	                message.append(cipher[j] ^ tmpKey[k%len(tmpKey)])
	                FH.write((cipher[j] ^ tmpKey[k%len(tmpKey)]).to_bytes(1,'little').decode(DecodePage).encode(EncodePage))
	            except Exception as e:
	            	print (e)


            j = j+1
            k = k+1
        FH.write(b'\x0a')
        print ("[*] message:", end="")
        for m in message:
        	print ((m).to_bytes(1,'little').decode(DecodePage),end="")

        i = i+1
        return message 
### getMessage ###

### Main ###
if __name__ == '__main__':

	if len(sys.argv) < 2:
		print ("Usage: "+sys.argv[0]+" fileName")
		exit(0)

	try:
		inputFile = codecs.open(sys.argv[1], 'rb')
	except Exception as e:
		print ("Problem opening file: "+sys.argv[1]+"\nQuitting...")
		print (e)
		exit(0)
	try:
		outputFile = codecs.open(sys.argv[1]+"_decrypted", 'wb')
	except Exception as e:
		print ("Problem opening file: "+sys.argv[1]+"_decrypted\nQuitting...")
		print (e)
		exit(0)

	try:
		print ("Reading file...")
		buffer = inputFile.read()
	except Exception as e:
		print (e)
		exit(0)

	try:
		print ("Searching for entries...")
		m = re.findall(b'##(.+?)(?:\r\n|\n\n)##', buffer, re.S)

	except Exception as e:
		print (e)
		exit(0)

	if m:
		print ("Processing entries...")
		for cipher in m:
			try:
				## remove extra ##s at the start
				n = re.search(b'##(.+)', cipher, re.S)
				if n:
					cipher = n.group(1)
				message = getMessage(KEY,cipher, outputFile)
			except Exception as e:
				print (e)
				exit(0)
	else:
		print ("Found no entries...")
