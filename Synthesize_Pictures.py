import os
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import *
from tkinter import filedialog
from PIL import Image

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = Tk()
root.title("hyunsoo GUI")

#file frame(add file, select delete)
file_frame = Frame(root)
file_frame.pack(fill="x", padx=5, pady=5) #clear space

#add file 
def add_file():
    files = filedialog.askopenfilenames(title="choose image file", \
        filetypes=(("PNG files", "*.png"), ("all files", "*.*")), \
        initialdir=r"C:\PythonWorkspace") #show C:/ path at first that user appoint
    
    #print file list that user select
    for file in files:
        list_file.insert(END,file)

#select delete
def del_file():
    #print(list_file.curselection())
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

#save path (folder)
def brouse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == "": #when user select cancel
        return 
    #print(folder_selected)
    txt_des_path.delete(0,END)
    txt_des_path.insert(0,folder_selected)

#merge image
def merge_image():
    # print("width : ",cmb_width.get())
    # print("distance : ",cmb_space.get())
    # print("format : ",cmb_format.get())

    try:
        #width
        img_width = cmb_width.get()
        if img_width == "Original":
            img_width = -1 #when -1(merge with original size)
        else:
            img_width = int(img_width)

        #interval
        img_space = cmb_space.get()
        if img_space == "narrow":
            img_space = 30
        elif img_space == "standard":
            img_space = 60
        elif img_space == "wide":
            img_space = 90
        else: #no
            img_space = 0

        #format
        img_format = cmb_format.get().lower() # take PNG, JPG, BMP value and change to small letter

        ###################################################

        images = [Image.open(x) for x in list_file.get(0,END)]

        #put image size list and process one by one
        image_sizes = [] #[(width1, height1), (width2, height2), ...]
        if img_width > -1:
            #change width value
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            #use original size
            image_sizes = [(x.size[0], x.size[1]) for x in images]

        #calculate formula
        #if the image size is '100 * 60' -> what is height when the width is '80'
        #(original width) : (original height) = (changed width) : (changed height)
        #      100        :         60        =        80       :       ?
        #       x         :          y        =         x'      :       y'
        #     xy' = x'y
        #     y' = x'y / x -> apply this formula
        # 100:60=80:48

        #substitute this code
        # x = width = size[0]
        # y = height = size[1]
        # x' = img_width (have to change this value)
        # y' = x'y / x = img_width * size[1] / size[0]

        widths, heights = zip(*(image_sizes))

        #demand max width, total height  
        max_width, total_height = max(widths), sum(heights)
        
        #make sketch book
        if img_space > 0: #image interval option apply
            total_height += (img_space * (len(images) - 1))

        result_image = Image.new("RGB",(max_width,total_height),(255, 255, 255)) #white background
        y_offset = 0 #y position

        for idx, img in enumerate(images):
            #if width is not original -> resize image
            if img_width > -1:
                img = img.resize(image_sizes[idx])

            result_image.paste(img, (0,y_offset))
            y_offset += (img.size[1] + img_space) #height value + interval that user select

            progress = (idx + 1) / len(images) * 100 #calculate actuall percent information
            p_var.set(progress)
            progress_bar.update()

        #format option progress 
        file_name = "hyunsoo_photo." + img_format
        dest_path = os.path.join(txt_des_path.get(),file_name)
        result_image.save(dest_path)
        msgbox.showinfo("notification","operation complete")
    except Exception as err: #exceptions process
        msgbox.showerror("error", err)

#start
def start():
    #check each options values
    # print("width : ",cmb_width.get())
    # print("distance : ",cmb_space.get())
    # print("format : ",cmb_format.get())

    #file list check
    if list_file.size() == 0:
        msgbox.showwarning("warning","please add the image file")
        return 

    #check save path 
    if len(txt_des_path.get()) == 0: 
        msgbox.showwarning("warning","please specify a save path")
        return 

    #merge image 
    merge_image()

btn_add_file = Button(file_frame, padx=5, pady=5, width = 12, text = "add file",command = add_file)
btn_add_file.pack(side="left")

btn_del_file = Button(file_frame, padx=5, pady=5, width = 12, text = "delete file", command=del_file)
btn_del_file.pack(side="right")

#list frame
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

#save path frame
path_frame = LabelFrame(root, text="save path")
path_frame.pack(fill="x", padx=5, pady=5)

txt_des_path = Entry(path_frame) 
txt_des_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) #change height 

btn_dest_path = Button(path_frame, text="search", width=10, command=brouse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5, ipady=5)

#option frame
frame_option = LabelFrame(root, text = "option")
frame_option.pack(padx=5, pady=5, ipady=5)

#1. width option
#1.1 width label
lbl_width = Label(frame_option, text = "width", width=8)
lbl_width.pack(side="left", padx=5, pady=5)

#1.2 width combo
opt_width = ["Original", "1024", "800", "640"]
cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width, width=10)
cmb_width.current(0)
cmb_width.pack(side="left", padx=5, pady=5)


#2. space option
#2.1 space option label
lbl_space = Label(frame_option, text = "space", width=8)
lbl_space.pack(side="left", padx=5, pady=5)

#2.2 space option combo
opt_space = ["no", "narrow", "standard", "wide"]
cmb_space = ttk.Combobox(frame_option, state="readonly", values=opt_space, width=10)
cmb_space.current(0)
cmb_space.pack(side="left", padx=5, pady=5)

#3. file format option
#3.1 file format option label
lbl_format = Label(frame_option, text = "format", width=8)
lbl_format.pack(side="left", padx=5, pady=5)

#3.2 file format option combo
opt_format = ["png", "jpg", "bmp"]
cmb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format, width=10)
cmb_format.current(0)
cmb_format.pack(side="left", padx=5, pady=5)

#progress (progress bar)
frame_progress = LabelFrame(root, text="progress")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var  = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5)

# execute frame
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="close", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text = "start", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False,False)
root.mainloop()