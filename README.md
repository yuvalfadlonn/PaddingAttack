Padding Oracle Attack Implementation
This repository contains a Python implementation and demonstration of a Padding Oracle Attack against a block cipher in CBC (Cipher Block Chaining) mode. This attack exploits padding validation vulnerabilities to decrypt ciphertexts without the encryption key.

🔍 What is a Padding Oracle Attack?
A Padding Oracle Attack is a type of side-channel attack where an "oracle" tells the attacker whether the padding of a decrypted ciphertext is correct. Even if the oracle only gives a True/False response, this information is enough to:

Systematically decrypt each byte of the ciphertext.
Exploit incorrect padding handling in systems using CBC with padding schemes like PKCS#7.
This attack shows why secure padding validation and proper cryptographic practices are crucial.

🚀 Usage
To run this demonstration, make sure Python is installed on your machine.
The script should demonstrate how the attacker can decrypt the ciphertext using only the padding oracle responses.

⚠️ Disclaimer
This project is for educational and demonstrative purposes only. It is intended to help students and security professionals understand cryptographic vulnerabilities. Do not use this knowledge or code for malicious purposes.

👤 Contributor
Yuval Fadlon
