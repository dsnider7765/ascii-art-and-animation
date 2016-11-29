# Present.py
# David Snider(DAS)
# November 14, 2016

import sys; from PIL import Image; import numpy as np; from time import sleep
import tkinter; import os; import winsound

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
#edited for use as function(DAS)
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
#----------------------------------------------------------------------------
def scrolling_line_print(txt):
    for i in txt.split('\n'):
        print(i)
        sleep(0.00005)

class App(object):
    '''making the application'''
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('{}x{}+0+0'.format(self.root.winfo_screenwidth(),
                                              self.root.winfo_screenheight()))
        self.root.grid()
        self.create()
        self.root.mainloop()

    def create(self):
        pass #this is to be made by children of this class

class Animation(App):
    '''for the actual animation'''

    def create(self):
        self.messageCount = 0
        self.messages = ['''The name is staying, Ella.
You don't get to argue that.
The reasoning is fair and you know it.
''','''You will always be Mr. Fredricksen to me :P
''','''So, that being said,
HAPPY BIRTHDAY MR. FREDRICKSEN!
''','''You said I wasn't allowed to buy you anything.
So, I didn't. I've worked on this daily since early November.
''','''There's no way I could avoid giving you something.
You deserve so much more than you think you do.
''','''First of all, anyone that can stand me for this long
deserves a medal. I'm one of the most annoying little
shits ever. XD
''','''I'm not always great with words so I figured I'd
make you a little code instead of a card.
''','''The few words you need to know are these:
you're one of my best friends and I will continue
to treat you as such for as long as I'm around.
''','''Hope your birthday went how you wanted!
You deserve the best!
'''
                         ]
##        self.asciiImages = [asciinator('IMG_8897.JPG',.12,1,10/4),
##                            asciinator('IMG_8898.JPG',.12,1,10/4)]
        txtFiles = self.get_txt_files()
        asciiImages = []
        for file in txtFiles:
            f = open(file,'r')
            asciiImages.append(f)
        self.asciiImages = []
        for txt in asciiImages:
            outTxt = ''
            for line in txt:
                outTxt += line
            
            self.asciiImages.append(outTxt)
            #print(outTxt)
        
        self.imageCount = 0
        self.topLabel=tkinter.Label(self.root,text="This is Mr. Fredricksen",
                                    font='-size 20').grid()
        #smallFont = tkinter.font(family="Consolas",size='7')
        asciiArt = self.asciiImages[self.imageCount]
        self.text = tkinter.Text(self.root,width=len(asciiArt.split('\n')[0]),
                                 height=len(asciiArt.split('\n')),
                                 wrap=tkinter.W,font='-family Consolas -size 3')
        self.text.grid(rowspan=3)
        self.text.insert(tkinter.END,asciiArt)
        self.text.config(state=tkinter.DISABLED)

        tkinter.Button(self.root,text="Continue",font='-size 15',
                       command=self.continue_button).grid(column=1,row=2,
                                                          sticky=tkinter.NE)
        txt = self.messages[self.messageCount]
        self.messageWidget = tkinter.Text(self.root,font='-size 18',
                                          wrap=tkinter.W,width=51,
                                          height=3)
        self.messageWidget.grid(row=1,column=1)
        self.messageWidget.insert(0.0,txt)
        self.messageWidget.config(state=tkinter.DISABLED)

        

    def continue_button(self):
##        if self.messageCount == 0:
##            winsound.PlaySound('polarize.wav', winsound.SND_FILENAME)
        try:
            self.messageCount += 1
            txt = self.messages[self.messageCount]
            self.messageWidget.config(state=tkinter.NORMAL)
            self.messageWidget.delete(0.0,tkinter.END)
            self.messageWidget.insert(0.0,txt)
            self.messageWidget.config(state=tkinter.DISABLED)

            try:
                self.imageCount += 1
                asciiArt = self.asciiImages[self.imageCount]
            except:
                self.imageCount = 0
                asciiArt = self.asciiImages[self.imageCount]
            self.text.config(state=tkinter.NORMAL,
                             width=len(asciiArt.split('\n')[0]),
                             height=len(asciiArt.split('\n')))
            self.text.delete(0.0,tkinter.END)
            self.text.insert(0.0,asciiArt)
            self.text.config(state=tkinter.DISABLED)
        except:
            self.the_end()
    def the_end(self):
        self.root.destroy()

    def get_txt_files(self):
            
        txt_list = []
        
        directory_list = os.listdir(os.getcwd()) # Get list of files
        for entry in directory_list:
            if '.txt' in entry:
                #absolute_filename = os.path.join(directory, entry)
                txt_list += [entry]
        return txt_list

if __name__ == '__main__':
    '''scrolling_line_print(asciinator('89294.jpg',.135,1))
    open('ascii_out.txt','w').write(asciinator('89294.jpg',.135,1))'''
    #print(len(asciinator('89294.jpg',.1,1,WCF=10/4).split('\n')[0]),
    #      len(asciinator('89294.jpg',.1,1,WCF=10/4).split('\n')))
    ####length of ella-gun-hand is 255 and height is 146
##    print('please wait while the images process.')
    Animation()

##    asciiImages = [asciinator('89294.jpg',.12,1,10/4),
##                   asciinator('IMG_8770.JPG',.12,1,10/4),
##                   asciinator('IMG_8774.JPG',.12,1,10/4)]
##    for i in range(len(asciiImages)):
##        open('image{}.txt'.format(i),'w').write(asciiImages[i])
##    txt = asciinator('IMG_8897.JPG',.12,1,10/4)
##    open('image3.txt','w').write(txt)

    
