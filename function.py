import myClass
from bitarray import bitarray
from PIL import Image
import cv2


#funkcije za kodiranje slike:


def loadImage(imageName):
    image=cv2.imread(imageName,cv2.IMREAD_UNCHANGED)
    return image


def calculateFrequency(image):
    height, width, channels= image.shape
    frequency={}
    x=0
    while x<height:
        y=0
        while y<width:
            z=0
            while z<channels:
                if str(image[x, y][z]) in frequency:
                    frequency[str(image[x, y][z])]+=1
                else:
                    frequency[str(image[x, y][z])]=1
                z+=1
            y+=1
        x+=1
    frequency=sorted(frequency.items(),key=lambda x: x[1], reverse=True)
    return frequency


def makeNodes(frequency):
    nodes=frequency
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = myClass.NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return nodes


def huffmanCodeTree(node, bitString=''): 
    if type(node) is str:
        return {node: bitString}
    (l, r) = node.children()
    d = dict()
    d.update(huffmanCodeTree(l, bitString + '0')) 
    d.update(huffmanCodeTree(r, bitString + '1')) 
    return d


def writeHuffmanFile(name, image, frequency, huffmanCode):
    huffmanFile = open(name,"w")
    huffmanFile.write('%s\n%s\n%s\n' % (image.shape))
    for (number, frequency) in frequency:
        huffmanFile.write('%s=>%s\n' % (number, huffmanCode[number]))
    huffmanFile.write('imageCode:\n')
    huffmanFile.close()


def getImageString(image, huffmanCode):
    height, width, channels= image.shape
    imageBits=''
    x=0
    while x<height:
        y=0
        while y<width:
            z=0
            while z<channels:
                imageBits+=str(huffmanCode[str(image[x, y][z])])
                z+=1
            y+=1
        x+=1
    return imageBits


def writeImageFile(name, image, huffmanCode):
    imageBits=getImageString(image, huffmanCode)
    imageFile = open(name,"ba")
    bitWriter=bitarray(imageBits)
    bitWriter.tofile(imageFile)
    imageFile.close()


def writeFile(name, image, frequency, huffmanCode):
    writeHuffmanFile(name, image, frequency, huffmanCode)
    writeImageFile(name, image, huffmanCode)


#funkcije za dekodiranje slike
    

def readHuffmanCodes(fileName):
    readingFile=open(fileName,"rb")
    height=int(readingFile.readline())
    width=int(readingFile.readline())
    channels=int(readingFile.readline())

    huffmanValues={}
    huffmanCodes=str(readingFile.readline())
    huffmanCodes=huffmanCodes.replace("'","").replace('b','').replace(r'\r\n',r'')
    while huffmanCodes != ('imageCode:'):
        value=huffmanCodes.split('=>')
        huffmanValues[int(value[0])]=value[1]
        huffmanCodes=str(readingFile.readline())
        huffmanCodes=huffmanCodes.replace("'","").replace('b','').replace(r'\r\n',r'')
    return [readingFile,height,width,channels,huffmanValues]


def isEqual(string, dictionary):
    for key, value in dictionary.items():
        if string==value:
            return True
    return False


def findEqual(string, dictionary):
    for key, value in dictionary.items():
        if string==value:
            return key


def reconstructImage(imageName, fileName):
    [readingFile,height,width,channels,huffmanValues]=readHuffmanCodes(fileName)
    if channels==4:
        image=Image.new( mode = "RGBA", size = (width, height) )
    elif channels==1:
        image=Image.new( mode = "L", size = (width, height) )
    elif channels==2:
        image=Image.new( mode = "LA", size = (width, height) )
    else:
        image=Image.new( mode = "RGB", size = (width, height) )
   
    image=image.save(imageName)
    bitReader=bitarray()
    bitReader.fromfile(readingFile)
    readingFile.close()

    image=cv2.imread(imageName,cv2.IMREAD_UNCHANGED)
    stack=''
    p=0
    x=0
    while x<height:
        y=0
        while y<width:
            z=0
            while z<channels:
                while not isEqual(stack, huffmanValues):
                    stack=stack+str(bitReader[p])
                    p+=1
                image[x, y][z]=findEqual(stack, huffmanValues)
                stack=''
                z+=1
            y+=1
        x+=1
    cv2.imwrite(imageName,image)
    cv2.imshow(imageName,image)
    

    
    

    












    
