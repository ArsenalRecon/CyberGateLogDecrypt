## CyberGate Keylogger Decryption Tool ##

Arsenal's CyberGate Keylog Decrypter script is a python tool that can be used against CyberGate encrypted keylogger files (either whole or in part, provided that the individual record is intact) to decode the cipher text an return the original plaintext that was captured by the RAT.

Fragmented entries from the file must start with '####'.

It is assumed that you know what your decryption key is. If you do not know your decryption key, but do have the
RAT live/installed on a system you control, a chosen-text attack is a good way to derive the key. Note that '\n' and '\r'
are not included in the XOR.

## Usage ##
Run with python3: python3 CyberGateLogDecrypt.py INPUTFILE

The script will write the decrypted output to a file called INPUTFILE_decrypted


## Contributions ##

Contributions and improvements to the code are welcomed.

## License ##

Distributed under the MIT License

## More Information ##

To learn more about Arsenal’s digital forensics software (Hibernation Recon, Registry Recon, and more!), please visit https://ArsenalRecon.com

To learn more about Arsenal’s digital forensics consulting services, please visit us at https://ArsenalExperts.com
