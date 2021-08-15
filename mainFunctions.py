import function


def codeImage(imagePath, filePath):
    image=function.loadImage(imagePath)
    frequency=function.calculateFrequency(image)
    nodes=function.makeNodes(frequency)
    huffmanCode = function.huffmanCodeTree(nodes[0][0])
    function.writeFile(filePath,image,frequency,huffmanCode)
    
def decodeFile(filePath, imagePath):
    function.reconstructImage(imagePath,filePath)
























