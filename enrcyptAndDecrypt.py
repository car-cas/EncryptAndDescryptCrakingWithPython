import sys, math
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'
def main(mode,message):
    #Encripta o decripta un mensaje de un archivo
    filename = 'encrypted_file.txt'    

    if mode == 'encrypt':
        #Encripta message a encrypted_file       
        pubKeyFilename = 'test_publica.txt'
        encryptedText = encryptAndWriteToFile(filename, pubKeyFilename, message)

        return encryptedText

    elif mode == 'decrypt':
        privKeyFilename = 'test_privada.txt'
        decryptedText = readFromFileAndDecrypt(message, privKeyFilename)

        return decryptedText




def getBlocksFromText(message, blockSize):
    #Convierte un string a una lista de bloques
    for character in message:
        if character not in SYMBOLS:
            return ""
    blockInts = []
    for blockStart in range(0, len(message), blockSize):
        #Calculamos el bloque para el bloque de texto
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(message))):
            blockInt += (SYMBOLS.index(message[i])) * (len(SYMBOLS) ** (i % blockSize))
        blockInts.append(blockInt)
   
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize):
    #Convierte una lista de bloques enteros al mensaje original
    #Es necesario saber la longitud del mensaje original para descifrar
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                #Decodificamos el mensaje
                charIndex = blockInt // (len(SYMBOLS) ** i)
                blockInt = blockInt % (len(SYMBOLS) ** i)
                blockMessage.insert(0, SYMBOLS[charIndex])
        message.extend(blockMessage)
   
    return ''.join(message)


def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=None):
    #Encripta un mensaje y lo guarda en un archivo
    keySize, n, e = readKeyFile(keyFilename)
    if blockSize == None:
        #Si el tamaño del bloque es nulo, se pone como el tamaño mas grande permitido por el tamaño de la llave
        blockSize = int(math.log(2 ** keySize, len(SYMBOLS)))
    #Miramos que el tamaño de la llave no sea muy grande
    if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
        sys.exit('ERROR: Block size is too large for the key and symbol set size. Did you specify the correct key file and encrypted file?')
    #Ciframos el mensaje        
    encryptedBlocks = encryptMessage(message, (n, e), blockSize)
    #Convertimos los valores enteros de los bloques a strings
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)
   
    encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
    fo = open(messageFilename, 'w')
    fo.write(encryptedContent)
    fo.close()  
    return encryptedContent


def readFromFileAndDecrypt(message, keyFilename):
    #Lee un archivo encriptado y lo descifra
    keySize, n, d = readKeyFile(keyFilename)

    #Lee el archivo cifrado
    messageLength, blockSize, encryptedMessage = message.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)
    #Revisa si el tamaño de la llave es muy grande para el tamaño del bloque
    if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
        sys.exit('ERROR: Block size is too large for the key and symbol set size. Did you specify the correct key file and encrypted file?')
    #Convierte el mensaje cifrado en enteros        
    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))
    #Descifra los valores de enteros
    message=decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)
    return message



def encryptMessage(message, key, blockSize):
    encryptedBlocks = []
    n, e = key
    #Creamos los bloques a partir del texto y los ciframos elevando cada valor del bloque a la e con modulo n
   
    for block in getBlocksFromText(message, blockSize):
        #block**e % n
        encryptedBlocks.append(pow(block, e, n))    
    return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key, blockSize):
    decryptedBlocks = []
    n, d = key
    #Desciframos los bloques elevando cada valor de bloque a la d con modulo n y buscamos el valor de texto de cada bloque nuevo
    
    for block in encryptedBlocks:
        #block**d % n
        decryptedBlocks.append(pow(block, d, n))    
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFile(keyFilename):
    archivo = open(keyFilename)
    mensaje = archivo.read()
    #otroValor puede ser E o D
    tamaño, n, otroValor = mensaje.split(',')
    archivo.close()
    return int(tamaño), int(n), int(otroValor)
