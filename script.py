from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad,unpad
import sys

def xor(a,b,c):
    return bytes([a ^ b ^ c])

def oracle(ciphertext, key, iv):
    decryptionFunc = DES.new(key, DES.MODE_CBC, iv = iv)

    plainSen = decryptionFunc.decrypt(ciphertext)

    try:
        unnpaddedPlainText = unpad(plainSen, DES.block_size)
        return True
    except:
        return False

def getBlock(cipher,key, iv, index, initializeBlock):
    init = bytearray(initializeBlock)

    for i in range(256):
        init[index] = i                     
        c = bytes(init) + cipher            
        if oracle(c, key, iv):           
            return bytes(init)               

    return bytes(init)

def getPlainBlock(currentBlock, prevBlock, key, iv):
    plainBlock = bytearray(bytes([0] * DES.block_size))
    Xj = bytearray([0] * DES.block_size)
    for i in range(DES.block_size-1, -1,-1):
        Xj = getBlock(currentBlock, key, iv, index=i, initializeBlock = Xj)
        plainByte = xor((DES.block_size - i), prevBlock[i], Xj[i])
        plainBlock[i] = plainByte[0]

        new_Xj = bytearray([0] * DES.block_size)
        for j in range(i,DES.block_size):
            new_Xj[j] = xor((DES.block_size - i + 1), prevBlock[j], plainBlock[j])[0]
        Xj = new_Xj
    return plainBlock

def encryptText(plainText, key, iv):
    encryptionFunc = DES.new(key, DES.MODE_CBC, iv = iv)
    cipher = encryptionFunc.encrypt(plainText)
    return cipher
    

def startImplement(iv, key, cipherText):

    numBlocks = len(cipherText) // DES.block_size  

    plainText = bytearray()
    for i in range(numBlocks):
        if i == 0:
            firstBlock = iv
        else:
            firstBlock = cipherText[(i-1)*DES.block_size:(i)*DES.block_size]

        secondBlock = cipherText[(i)*DES.block_size:(i+1)*DES.block_size]
        plainText += getPlainBlock(secondBlock,firstBlock,key,iv)

    return unpad((bytes(plainText)), DES.block_size)

def main():
    key = None
    plaintext = None
    iv = None
    ciphertext = None

    while True:
        print("DES CBC Oracle Attack Tool Menu:")
        print("1) Enter KEY (8 bytes)")
        print("2) Enter IV (8 bytes)")
        print("3) Enter PLAINTEXT")
        print("4) Encrypt (show ciphertext & blocks)")
        print("5) CRACK THE CIPHERTEXT")
        print("0) Exit")
        choice = input("Choose option: ").strip()

        if choice == '1':
            key = input("Enter KEY (8 bytes): ").strip()
            if len(key) != 8:
                print("Key must be exactly 8 bytes.")
                key = None
            else:
                key = key.encode()
        
        elif choice == '2':
            iv = input("Enter IV (8 bytes): ").strip()
            if len(iv) != 8:
                print("IV must be exactly 8 bytes.")
                iv = None
            else:
                iv = iv.encode()

        elif choice == '3':
            plaintext = input("Enter PLAINTEXT: ").strip()
            if not plaintext:
                print("Plaintext cannot be empty.")
                plaintext = None
            else:
                plaintext = bytes(plaintext, 'utf-8')
                paddedSen = pad(plaintext,DES.block_size)
                plaintext = paddedSen

        elif choice == '4':
            if key and iv and plaintext:
                print("Encrypting...")
                ciphertext = encryptText(plaintext, key, iv)
                print("Ciphertext (hex):", ciphertext.hex())
            else:
                print("Please set KEY, IV, and PLAINTEXT first.")

        elif choice == '5':
            if ciphertext:
                print("Cracking ciphertext!")
                plainText = startImplement(iv, key, ciphertext)
                print("Cracked the ciphertext:", plainText.decode())
            else:
                print("No ciphertext available.")

        elif choice == '0':
            print("Exiting...")
            sys.exit(0)

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
