import tkinter
import tkinter.filedialog

from PIL import Image
from PIL import ImageTk

def openFile() :
    fpath = fd.askopenfilename()
    if fpath :
        getPhoto(fpath)

def getPhoto(fpath) :
    image = Image.open(fpath)
    width, height = image.size
    if height > 800 :
        width_ = int(width * (800/height))
        if width_ > 1280 :
            height_ = int(800 * (1280/width_))
        else : height_ = 800
        image = image.resize((width_, height_))
    if width_ > 1280 :
        height_ = int(height * (1280/width))
        if height_ > 800 :
            width_ = int(1280 * (800/height_))
        else : width_ = 1280
        image = image.resize((width_, height_))

    imageData = ImageTk.PhotoImage(image)
    imageLabel.configure(image = imageData)
    imageLabel.image = imageData