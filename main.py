from tkinter import * # Import de la lib pour Gui et ses sous dépendances
from PIL import ImageTk,Image  # Import de la lib PIL pour la gestion des images png
from tkinter.ttk import Progressbar
import tkinter.messagebox
import binascii
import usb1 #Import Libusb1 https://pypi.org/project/libusb1/#installation

# Init Var
Cartridge_Info = 0

# Init Array

USB_Buffer_OUT=bytearray(64)
USB_Buffer_IN=bytearray(64)
Domestic_Title=bytearray(48)
International_Title=bytearray(48)
Release_Date=bytearray(8)
Serial_Number=bytearray(14)
Region_Flag=bytearray(3)
ROM_Checksum=bytearray(2)
ROM_Size=bytearray(4)
RAM_Flag=bytearray(2)
RAM_Type=bytearray(1)
RAM_Size=bytearray(4)
CHIP_ID=bytearray(2)
Dump_ROM=bytearray(1024*1024)

#for i in range(64):
    # USB_Buffer_OUT.append(0)
     #USB_Buffer_IN.append(0)
     
# Set the size of the tkinter window

window = Tk()
window.title("Python MD Dumper GUI")
window.geometry("1132x870") #550,450

# Define a Canvas widget

canvas = Canvas(window , width =1132, height =870)
canvas.pack(pady=20)

# Add Widget Debug

DebugArea = Text(window , height= 5 , width=60 , bg='black' , fg ='white')
DebugArea.window = canvas.create_window(0, 0, anchor=NW, window=DebugArea)
canvas.move(DebugArea.window ,60 ,680)
DebugArea.insert(END,'Welcome to MD Dumper GUI')
DebugArea.insert(END,'\nTry to init USB communication...')

# Add Widget Progress Bar

style = ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background='yellow')
bar = Progressbar(window, length=600, style='black.Horizontal.TProgressbar')
bar['value'] = 0
bar.window = canvas.create_window(0, 0, anchor=NW, window=bar)
canvas.move(bar.window ,120 ,615)

# USB Low Level Function

def __init__(self, idVendor, idProduct):
    self.context = usb1.USBContext()
    self.dev = self.context.openByVendorIDAndProductID(idVendor, idProduct)
    if not self.dev:
         #tkinter.messagebox.showinfo("USB Detect","MD Dumper device not found")
        DebugArea.insert(END,'\nMD Dumper device not found')
    if sys.platform.startswith('linux'):
        if self.dev.kernelDriverActive(0):
            self.dev.detachKernelDriver(0)
    self.dev.resetDevice()
    self.dev.claimInterface(0)
    DebugArea.insert(END,'\nMD Dumper detected Sucessfully !')

def openUsb(vid,pid):
     context = usb1.USBContext()
     for dev in context.getDeviceList(skip_on_error=True):
         if (dev.getVendorID()==vid) & (dev.getProductID()==pid):
                 return dev.open()
                
# Add Widget TXT Entry Box

txt_domestic = Entry(window,width=48, state = 'disabled')
txt_domestic.window = canvas.create_window(0, 0, anchor=NW, window=txt_domestic )
canvas.move(txt_domestic.window ,115 ,150)

txt_international = Entry(window,width=48, state = 'disabled')
txt_international .window = canvas.create_window(0, 0, anchor=NW, window=txt_international  )
canvas.move(txt_international .window ,115 ,216)

txt_release = Entry(window,width=20, state = 'disabled')
txt_release.window = canvas.create_window(0, 0, anchor=NW, window=txt_release )
canvas.move(txt_release.window ,115 ,282)

txt_serial = Entry(window,width=18, state = 'disabled')
txt_serial.window = canvas.create_window(0, 0, anchor=NW, window=txt_serial )
canvas.move(txt_serial.window ,500 ,278)

txt_region = Entry(window,width=9, state = 'disabled')
txt_region.window = canvas.create_window(0, 0, anchor=NW, window=txt_region )
canvas.move(txt_region.window ,115 ,348)

txt_checksum = Entry(window,width=9, state = 'disabled')
txt_checksum.window = canvas.create_window(0, 0, anchor=NW, window=txt_checksum )
canvas.move(txt_checksum.window ,370 ,348)

txt_romsize = Entry(window,width=9, state = 'disabled')
txt_romsize.window = canvas.create_window(0, 0, anchor=NW, window=txt_romsize )
canvas.move(txt_romsize.window ,620 ,348)

txt_savetype = Entry(window,width=9, state = 'disabled')
txt_savetype.window = canvas.create_window(0, 0, anchor=NW, window=txt_savetype )
canvas.move(txt_savetype.window ,112 ,410)

txt_savesize = Entry(window,width=9, state = 'disabled')
txt_savesize.window = canvas.create_window(0, 0, anchor=NW, window=txt_savesize )
canvas.move(txt_savesize.window ,370 ,410)

txt_saveadr = Entry(window,width=9, state = 'disabled')
txt_saveadr.window = canvas.create_window(0, 0, anchor=NW, window=txt_saveadr )
canvas.move(txt_saveadr.window ,620 ,410)

txt_chipid = Entry(window,width=9, state = 'disabled')
txt_chipid.window = canvas.create_window(0, 0, anchor=NW, window=txt_chipid )
canvas.move(txt_chipid.window ,112 ,480)

txt_chipinfos = Entry(window,width=28, state = 'disabled')
txt_chipinfos.window = canvas.create_window(0, 0, anchor=NW, window=txt_chipinfos )
canvas.move(txt_chipinfos.window ,368 ,480)

txt_version = Entry(window,width=48, state = 'disabled')
txt_version.window = canvas.create_window(0, 0, anchor=NW, window=txt_version )
canvas.move(txt_version.window ,116 ,540)

### Déclaration des Actions ###

def DetectUSB():
     __init__(usb1.USBContext(), 0x0483,0x5740)
     
def Infos():
    context = usb1.USBContext()
    handle = context.openByVendorIDAndProductID(
        0x483,
        0x5740,
        skip_on_error=True,
    )
    if handle is None:
        # Device not present, or user is not allowed to access device.
              DebugArea.insert(END,'\nMD Dumper device not found')
    with handle.claimInterface(0):
        # Do stuff with endpoints on claimed interface.
              DebugArea.insert(END,'\nMD Dumper detected Sucessfully !')
              Cartridge_Info = 1
        # Domestic Title
              Address=144
              USB_Buffer_OUT[0]=0x11
              USB_Buffer_OUT[1] = Address & 0xFF 
              USB_Buffer_OUT[2] = (Address & 0xFF00)>>8
              USB_Buffer_OUT[3]=(Address & 0xFF0000)>>16
              handle.bulkWrite(0x01,USB_Buffer_OUT,timeout=5000)
              DebugArea.insert(END,'\nUSB packets send sucessfully!')
              USB_Buffer_IN = handle.bulkRead(0x82,64,timeout=5000)
              DebugArea.insert(END,'\nUSB packets received sucessfully!')
              txt_domestic.configure(state= 'normal')
              #print(USB_Buffer_IN)
              for i in range(48): Domestic_Title[i] = USB_Buffer_IN[i]
              txt_domestic.insert(INSERT,bytes(Domestic_Title))        
        # International Title
              Address=168
              USB_Buffer_OUT[0]=0x11
              USB_Buffer_OUT[1] = Address & 0xFF 
              USB_Buffer_OUT[2] = (Address & 0xFF00)>>8
              USB_Buffer_OUT[3]=(Address & 0xFF0000)>>16
              handle.bulkWrite(0x01,USB_Buffer_OUT,timeout=5000)
              USB_Buffer_IN = handle.bulkRead(0x82,64,timeout=5000)
              txt_international.configure(state= 'normal')
              for i in range(48): International_Title[i] = USB_Buffer_IN[i]
              txt_international.insert(INSERT,bytes(International_Title))
         # Release Date
              Address=140
              USB_Buffer_OUT[0]=0x11
              USB_Buffer_OUT[1] = Address & 0xFF 
              USB_Buffer_OUT[2] = (Address & 0xFF00)>>8
              USB_Buffer_OUT[3]=(Address & 0xFF0000)>>16
              handle.bulkWrite(0x01,USB_Buffer_OUT,timeout=5000)
              USB_Buffer_IN = handle.bulkRead(0x82,64,timeout=5000)
              txt_release.configure(state= 'normal')
              for i in range(8): Release_Date[i] = USB_Buffer_IN[i]
              txt_release.insert(INSERT,bytes(Release_Date))
         # Serial Number
              Address=192
              USB_Buffer_OUT[0]=0x11
              USB_Buffer_OUT[1] = Address & 0xFF 
              USB_Buffer_OUT[2] = (Address & 0xFF00)>>8
              USB_Buffer_OUT[3]=(Address & 0xFF0000)>>16
              handle.bulkWrite(0x01,USB_Buffer_OUT,timeout=5000)
              USB_Buffer_IN = handle.bulkRead(0x82,64,timeout=5000)
              txt_serial.configure(state= 'normal')
              for i in range(14): Serial_Number[i] = USB_Buffer_IN[i]
              txt_serial.insert(INSERT,bytes(Serial_Number))        
         # Region Flag
              Address=248
              USB_Buffer_OUT[0]=0x11
              USB_Buffer_OUT[1] = Address & 0xFF 
              USB_Buffer_OUT[2] = (Address & 0xFF00)>>8
              USB_Buffer_OUT[3]=(Address & 0xFF0000)>>16
              handle.bulkWrite(0x01,USB_Buffer_OUT,timeout=5000)
              USB_Buffer_IN = handle.bulkRead(0x82,64,timeout=5000)
              txt_region.configure(state= 'normal')
              for i in range(3): Region_Flag[i] = USB_Buffer_IN[i]
              txt_region.insert(INSERT,bytes(Region_Flag))
        # ROM Checksum
              Address=199
              USB_Buffer_OUT[0]=0x11
              USB_Buffer_OUT[1] = Address & 0xFF 
              USB_Buffer_OUT[2] = (Address & 0xFF00)>>8
              USB_Buffer_OUT[3]=(Address & 0xFF0000)>>16
              handle.bulkWrite(0x01,USB_Buffer_OUT,timeout=5000)
              USB_Buffer_IN = handle.bulkRead(0x82,64,timeout=5000)
              txt_checksum.configure(state= 'normal')
              for i in range(2): ROM_Checksum[i] = USB_Buffer_IN[i]
              txt_checksum.insert(INSERT,binascii.hexlify(bytearray(ROM_Checksum)))
        # ROM Size
              Address=210
              USB_Buffer_OUT[0]=0x11
              USB_Buffer_OUT[1] = Address & 0xFF 
              USB_Buffer_OUT[2] = (Address & 0xFF00)>>8
              USB_Buffer_OUT[3]=(Address & 0xFF0000)>>16
              handle.bulkWrite(0x01,USB_Buffer_OUT,timeout=5000)
              USB_Buffer_IN = handle.bulkRead(0x82,64,timeout=5000)
              txt_romsize.configure(state= 'normal')
              for i in range(4): ROM_Size[i] = USB_Buffer_IN[i]
              Size_ROM = ((int.from_bytes(ROM_Size,byteorder='big', signed=False))+1)/1024
              txt_romsize.insert(INSERT,Size_ROM )
        # RAM Flag
              Address=216
              USB_Buffer_OUT[0]=0x11
              USB_Buffer_OUT[1] = Address & 0xFF 
              USB_Buffer_OUT[2] = (Address & 0xFF00)>>8
              USB_Buffer_OUT[3]=(Address & 0xFF0000)>>16
              handle.bulkWrite(0x01,USB_Buffer_OUT,timeout=5000)
              USB_Buffer_IN = handle.bulkRead(0x82,64,timeout=5000)
              txt_savetype.configure(state= 'normal')
              for i in range(2): RAM_Flag[i] = USB_Buffer_IN[i]
              if (RAM_Flag[0] == 0x20 and RAM_Flag[1] == 0x20  ): txt_savetype.insert(INSERT,"NO RAM")
              else : txt_savetype.insert(INSERT,"Bckp RAM")
        # RAM Type
              Address=216
              USB_Buffer_OUT[0]=0x11
              USB_Buffer_OUT[1] = Address & 0xFF 
              USB_Buffer_OUT[2] = (Address & 0xFF00)>>8
              USB_Buffer_OUT[3]=(Address & 0xFF0000)>>16
              handle.bulkWrite(0x01,USB_Buffer_OUT,timeout=5000)
              USB_Buffer_IN = handle.bulkRead(0x82,64,timeout=5000)
              txt_savesize.configure(state= 'normal')
              RAM_Type[0] = USB_Buffer_IN[2]
              if (RAM_Type[0] == 0xF0) : txt_savesize.insert(INSERT,"SRAM")
              if (RAM_Type[0] == 0xF8) : txt_savesize.insert(INSERT,"SRAM")
              if (RAM_Type[0] == 0xB0) : txt_savesize.insert(INSERT,"SRAM")
              if (RAM_Type[0] == 0xB8) : txt_savesize.insert(INSERT,"SRAM")
              if (RAM_Type[0] == 0xE0) : txt_savesize.insert(INSERT,"SRAM")
              if (RAM_Type[0] == 0xA0) : txt_savesize.insert(INSERT,"SRAM")
              if (RAM_Type[0] == 0xE8) : txt_savesize.insert(INSERT,"EEPROM")
              if (RAM_Type[0] == 0x20) : txt_savesize.insert(INSERT,"NO RAM")
         # RAM Size
              Address=220
              USB_Buffer_OUT[0]=0x11
              USB_Buffer_OUT[1] = Address & 0xFF 
              USB_Buffer_OUT[2] = (Address & 0xFF00)>>8
              USB_Buffer_OUT[3]=(Address & 0xFF0000)>>16
              handle.bulkWrite(0x01,USB_Buffer_OUT,timeout=5000)
              USB_Buffer_IN = handle.bulkRead(0x82,64,timeout=5000)
              txt_saveadr.configure(state= 'normal')
              for i in range(4): RAM_Size[i] = USB_Buffer_IN[i]
              Size_RAM = ((int.from_bytes(RAM_Size,byteorder='big', signed=False))+1)/1024
              Size_RAM =Size_RAM - 2048
              txt_saveadr.insert(INSERT,Size_RAM )
              if (RAM_Size[1] == 0x20) : txt_saveadr.delete(0, 'end')
              if (RAM_Size[1] == 0x20) : txt_saveadr.insert(INSERT,"NO RAM")
          # Chip ID
              Address=0
              USB_Buffer_OUT[0]=0x11
              USB_Buffer_OUT[1] = Address & 0xFF 
              USB_Buffer_OUT[2] = (Address & 0xFF00)>>8
              USB_Buffer_OUT[3]=(Address & 0xFF0000)>>16
              handle.bulkWrite(0x01,USB_Buffer_OUT,timeout=5000)
              USB_Buffer_IN = handle.bulkRead(0x82,64,timeout=5000)
              txt_chipid.configure(state= 'normal')
              for i in range(2): CHIP_ID[i] = USB_Buffer_IN[i]
              txt_chipid.configure(state= 'normal')
              txt_chipid.insert(INSERT,binascii.hexlify(bytearray(CHIP_ID)))
           # Chip Infos
              txt_chipinfos.configure(state= 'normal')
              txt_chipinfos.insert(INSERT,"SEGA Original Maskrom")
          # Cartridge Extra infos
              txt_version.configure(state= 'normal')
              if (RAM_Type[0] == 0xF0) : txt_version.insert(INSERT,"Cartridge with backup Memory : 8 bit SRAM (even addr)")
              if (RAM_Type[0] == 0xF8) : txt_version.insert(INSERT,"Cartridge with backup Memory : 8 bit SRAM (odd addr)")
              if (RAM_Type[0] == 0xB0) : txt_version.insert(INSERT,"Cartridge with volatile Memory : 8 bit SRAM (odd addr)")
              if (RAM_Type[0] == 0xB8) : txt_version.insert(INSERT,"Cartridge with volatile Memory : 8 bit SRAM (even addr)")
              if (RAM_Type[0] == 0xE0) : txt_version.insert(INSERT,"Cartridge with backup Memory : 16 bit SRAM")
              if (RAM_Type[0] == 0xA0) : txt_version.insert(INSERT,"Cartridge with volatile Memory : 16 bit SRAM")
              if (RAM_Type[0] == 0xE8) : txt_version.insert(INSERT,"Cartridge with backup Memory : Serial EEPROM")
              if (RAM_Type[0] == 0x20) : txt_version.insert(INSERT,"Sega Classic cartridge with no Backup RAM")
                          
def ReadFlash():
              context = usb1.USBContext()
              handle = context.openByVendorIDAndProductID(0x483,0x5740,skip_on_error=True,)
              handle.claimInterface(0)
              Address=0
              offset=0
              i=0
              USB_Buffer_OUT[0]=0x11
              USB_Buffer_OUT[1] = Address & 0xFF 
              USB_Buffer_OUT[2] = (Address & 0xFF00)>>8
              USB_Buffer_OUT[3]=(Address & 0xFF0000)>>16
              USB_Buffer_OUT[4]= 0
              handle.bulkWrite(0x01,USB_Buffer_OUT,timeout=5000)
              USB_Buffer_IN = handle.bulkRead(0x82,64,timeout=5000)
              while i < (1024*1024)/64:
                   USB_Buffer_OUT[0]=0x11
                   USB_Buffer_OUT[1] = Address & 0xFF 
                   USB_Buffer_OUT[2] = (Address & 0xFF00)>>8
                   USB_Buffer_OUT[3]=(Address & 0xFF0000)>>16
                   USB_Buffer_OUT[4]= 0
                   handle.bulkWrite(0x01,USB_Buffer_OUT,timeout=5000)
                   USB_Buffer_IN = handle.bulkRead(0x82,64,timeout=5000)
                   for j in range(64): Dump_ROM[(i*64)+j] = USB_Buffer_IN[j]
                   Address = Address+32 # SMD works in word mode so 2 bytes = 1 word
                   j=0;
                   i=i+1
              bar['value'] = 100
              file =  open("dump_smd.bin", "wb")
              file.write(Dump_ROM)
              messagebox.showinfo('DUMP ROM','Dump ROM Completed ! ')

     
     
              
              
# Add some picture widget to the canevas

image_domestic = ImageTk.PhotoImage(Image.open("icons2/domestic.png"))  
img_domestic  = canvas.create_image(0, 0, anchor=NW, image=image_domestic)
canvas.move(img_domestic,30 ,140)

image_international = ImageTk.PhotoImage(Image.open("icons2/international.png"))  
img_international  = canvas.create_image(0, 0, anchor=NW, image=image_international)
canvas.move(img_international,30 ,205)

image_release = ImageTk.PhotoImage(Image.open("icons2/release.png"))  
img_release  = canvas.create_image(0, 0, anchor=NW, image=image_release)
canvas.move(img_release,30 ,270)

image_serial = ImageTk.PhotoImage(Image.open("icons2/version.png"))  
img_serial  = canvas.create_image(0, 0, anchor=NW, image=image_serial)
canvas.move(img_serial,420 ,270)

image_region = ImageTk.PhotoImage(Image.open("icons2/region.png"))  
img_region  = canvas.create_image(0, 0, anchor=NW, image=image_region)
canvas.move(img_region,30 ,335)

image_checksum = ImageTk.PhotoImage(Image.open("icons2/checksum.png"))  
img_checksum  = canvas.create_image(0, 0, anchor=NW, image=image_checksum )
canvas.move(img_checksum ,280 ,340)

image_romsize = ImageTk.PhotoImage(Image.open("icons2/romsize.png"))  
img_romsize  = canvas.create_image(0, 0, anchor=NW, image=image_romsize )
canvas.move(img_romsize ,530 ,340)

image_savetype = ImageTk.PhotoImage(Image.open("icons2/savetype.png"))  
img_savetype  = canvas.create_image(0, 0, anchor=NW, image=image_savetype )
canvas.move(img_savetype ,30 ,400)

image_savesize = ImageTk.PhotoImage(Image.open("icons2/savesize.png"))  
img_savesize  = canvas.create_image(0, 0, anchor=NW, image=image_savesize )
canvas.move(img_savesize ,280 ,400)

image_saveadr = ImageTk.PhotoImage(Image.open("icons2/saveadr.png"))  
img_saveadr  = canvas.create_image(0, 0, anchor=NW, image=image_saveadr )
canvas.move(img_saveadr ,530 ,400)

image_chipid = ImageTk.PhotoImage(Image.open("icons2/chipid.png"))  
img_chipid  = canvas.create_image(0, 0, anchor=NW, image=image_chipid )
canvas.move(img_chipid ,30 ,465)

image_chipinfos = ImageTk.PhotoImage(Image.open("icons2/chipinfos.png"))  
img_chipinfos  = canvas.create_image(0, 0, anchor=NW, image=image_chipinfos )
canvas.move(img_chipinfos ,280 ,465)

image_version = ImageTk.PhotoImage(Image.open("icons2/version.png"))  
img_version  = canvas.create_image(0, 0, anchor=NW, image=image_version )
canvas.move(img_version ,30 ,530)

image_time = ImageTk.PhotoImage(Image.open("icons2/time.png"))  
img_time  = canvas.create_image(0, 0, anchor=NW, image=image_time)
canvas.move(img_time ,30 ,595)

image_SMD = ImageTk.PhotoImage(Image.open("icons2/SMD2.png"))  
img_SMD  = canvas.create_image(0, 0, anchor=NW, image=image_SMD)
canvas.move(img_SMD ,800 ,15)



# Add Widget Buttons

infos_btn = Button(window, text="Infos" , width = 20 , bg='#FFFFFF',command=Infos)
infos_btn.window = canvas.create_window(0, 0, anchor=NW, window=infos_btn)
canvas.move(infos_btn.window ,800 ,240)

readflash_btn = Button(window, text="Read Flash" , width = 20 , bg='#FFFFFF',command=ReadFlash)
readflash_btn.window = canvas.create_window(0, 0, anchor=NW, window=readflash_btn)
canvas.move(readflash_btn.window ,800 ,320)

loadfile_btn = Button(window, text="Read Save" , width = 20 , bg='#FFFFFF')
loadfile_btn.window = canvas.create_window(0, 0, anchor=NW, window=loadfile_btn)
canvas.move(loadfile_btn.window ,800 ,400)

writeflash_btn = Button(window, text="Write Flash" , width = 20 , bg='#FFFFFF')
writeflash_btn.window = canvas.create_window(0, 0, anchor=NW, window=writeflash_btn)
canvas.move(writeflash_btn.window ,800 ,480)

writesave_btn = Button(window, text="Write Save" , width = 20 , bg='#FFFFFF')
writesave_btn.window = canvas.create_window(0, 0, anchor=NW, window=writesave_btn)
canvas.move(writesave_btn.window ,800 ,560)

Megadrive_btn = Button(window, text="Megadrive" , width = 20 , bg='blue' , fg='White')
Megadrive_btn.window = canvas.create_window(0, 0, anchor=NW, window=Megadrive_btn)
canvas.move(Megadrive_btn.window ,30 ,30)

MasterSystem_btn = Button(window, text="Master System" , width = 20 , bg='#FFFFFF')
MasterSystem_btn.window = canvas.create_window(0, 0, anchor=NW, window=MasterSystem_btn)
canvas.move(MasterSystem_btn.window ,320 ,30)


# surnameEntry = tk.Entry(form)

#button1 = Button(self, text = "Quit", command = self.quit, anchor = W)
#button1.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
#button1_window = canvas1.create_window(10, 10, anchor=NW, window=button1)


# Main Window loop

window.mainloop()

                                         
