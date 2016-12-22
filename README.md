## CyberGate Keylogger Decryption Tool ##

Arsenal's CyberGate Keylog Decrypter script is a python tool that can be used against CyberGate encrypted keylogger files (either whole or in part, provided that the individual record is intact) to decode the cipher text an return the original plaintext that was captured by the RAT.

Fragmented entries from the file must start with '####'.

It is assumed that you know what your decryption key is. If you do not know your decryption key, but do have the
RAT live/installed on a system you control, a chosen-text attack is a good way to derive the key. Note that '\n' and '\r'
are not included in the XOR.

## Usage ##
Run with python3: python3 CyberGateLogDecrypt.py <inputFile>
The script will write the decrypted output to a file called <inputFile>_decrypted


## Contributions ##

Contributions and improvements to the code are welcomed.

## License ##

Distributed under the MIT License

