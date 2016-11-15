# scrolling_ascii_converter.py
# David Snider
# November 14, 2016

import sys; from PIL import Image; import numpy as np; from time import sleep

def make_grayscale(imgPath):
    img = Image.open(imgPath).convert('RGB')
    
    width,height = img.size
    for x in range(width):
        for y in range(height):
            pixelColor = img.getpixel((x,y))
            gValue = max(pixelColor)
            pixelColor = (gValue,gValue,gValue)
            img.putpixel((x,y),pixelColor)
    return img
            
                

def asciinator(imgPath,SC,GCF,WCF=7/4):
# code from https://gist.github.com/cdiener/10491632 ------------------------
    chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))

    #if len(sys.argv) != 4: 
    #    print( 'Usage: ./asciinator.py image scale factor' )
    #    sys.exit()
    SC, GCF = float(SC), float(GCF)

    img = make_grayscale(imgPath)
    S = ( round(img.size[0]*SC*WCF), round(img.size[1]*SC) )
    img = np.sum( np.asarray( img.resize(S) ), axis=2)
    img -= img.min()
    img = (1.0 - img/img.max())**GCF*(chars.size-1)

    return "\n".join( ("".join(r) for r in chars[img.astype(int)]) )

def scrolling_line_print(txt):
    for i in txt.split('\n'):
        print(i)
        sleep(0.00005)
        
if __name__ == '__main__':
    scrolling_line_print(asciinator('89294.jpg',.135,1))
    open('ascii_out.txt','w').write(asciinator('89294.jpg',.135,1))
