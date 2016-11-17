# scrolling_ascii_converter.py
# David Snider
# November 14, 2016

import sys; from PIL import Image; import numpy as np; from time import sleep
import tkinter

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

class App(object):
    '''making the application'''
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.grid()
        self.create()
        self.root.mainloop()

    def create(self):
        pass #this is to be made by children of this class

class Animation(App):
    '''for the actual animation'''
            
    def create(self):
        self.messageCount = 0
        self.messages = ['''
This is you, Ella. You don't get to argue that.
The reasoning is fair and you know it.
''','''
Look, I know you said I couldn't get you anything
for your birthday, so I made you this.
''','''
I just want you to know that you're not
unimportant.
''','''
You're important to me, you're important to Ethan,
and you're definitely important to your mother.
''','''
So, happy birthday(belated or early if you opened
this on a different day).
'''
                         ]
        self.topLabel=tkinter.Label(self.root,text="This is Mr. Fredricksen",
                                    font='-size 20').grid()
        #smallFont = tkinter.font(family="Consolas",size='7')
        asciiArt = asciinator('89294.jpg',.12,1,WCF=10/4)
        self.text = tkinter.Text(self.root,width=len(asciiArt.split('\n')[0]),
                                 height=len(asciiArt.split('\n')),
                                 wrap=tkinter.W,font='-family Consolas -size 3')
        self.text.grid(rowspan=3)
        self.text.insert(tkinter.END,asciiArt)
        self.text.config(state=tkinter.DISABLED)

        tkinter.Button(self.root,text="Continue",font='-size 15',
                       command=self.continue_button).grid(column=1,row=2,
                                                          sticky=tkinter.NE)
        messageText = self.messages[self.messageCount]
        self.messageWidget = tkinter.Text(self.root,font='-size 10',
                                          wrap=tkinter.W)
        self.messageWidget.grid(row=1,column=1)
        self.messageWidget.insert(0.0,messageText)
        self.messageWidget.config(state=tkinter.DISABLED)

    def continue_button(self):
        self.messageCount += 1
        txt = self.messages[self.messageCount]
        self.messageWidget.config(state=tkinter.NORMAL)
        self.messageWidget.delete(0.0,tkinter.END)
        self.messageWidget.insert(0.0,txt)
        self.messageWidget.config(state=tkinter.DISABLED)
        
        
        
        
if __name__ == '__main__':
    '''scrolling_line_print(asciinator('89294.jpg',.135,1))
    open('ascii_out.txt','w').write(asciinator('89294.jpg',.135,1))'''
    #print(len(asciinator('89294.jpg',.1,1,WCF=10/4).split('\n')[0]),
    #      len(asciinator('89294.jpg',.1,1,WCF=10/4).split('\n')))
    ####length of ella-gun-hand is 255 and height is 146
    Animation()
