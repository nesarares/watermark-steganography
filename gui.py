from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from PIL import ImageTk, Image
import stego


class Application(Frame):
    def __init__(self, window=None):
        super().__init__(window)

        self.watermark_path = None
        self.input_path = None
        self.input_watermarked_path = None

        self.window = window
        self.window.title('Steganography encoder and decoder')
        self.window.geometry('600x520')
        self.center()
        self.create_widgets()

    def center(self):
        """
        https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
        """
        self.window.update_idletasks()
        width = self.window.winfo_width()
        frm_width = self.window.winfo_rootx() - self.window.winfo_x()
        win_width = width + 2 * frm_width
        height = self.window.winfo_height()
        titlebar_height = self.window.winfo_rooty() - self.window.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.window.winfo_screenwidth() // 2 - win_width // 2
        y = self.window.winfo_screenheight() // 2 - win_height // 2
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.window.deiconify()

    def create_widgets(self):
        tab_control = ttk.Notebook(self.window)
        tab_encode = ttk.Frame(tab_control)
        tab_decode = ttk.Frame(tab_control)

        self.tab_encode = tab_encode
        self.tab_decode = tab_decode

        tab_control.add(tab_encode, text='Encoder')
        tab_control.add(tab_decode, text='Decoder')
        tab_control.pack(expand=1, fill='both')

        self.create_widgets_encode()
        self.create_widgets_decode()

    def create_widgets_encode(self):
        self.tab_encode.columnconfigure(0, pad=20, weight=0)
        self.tab_encode.columnconfigure(1, pad=60, weight=1)
        self.tab_encode.rowconfigure(0, weight=0)
        self.tab_encode.rowconfigure(1, weight=1)
        self.tab_encode.rowconfigure(2, weight=0)
        self.tab_encode.rowconfigure(3, weight=1)
        self.tab_encode.rowconfigure(4, weight=0)

        lbl1 = Label(self.tab_encode, text='Select an image (.png)',
                     font=("Arial Bold", 14))
        lbl1.grid(column=0, row=0, sticky=W+N, padx=(20, 20), pady=(20, 20))

        lbl1 = Label(self.tab_encode,
                     text='Select a watermark (.png)', font=("Arial Bold", 14))
        lbl1.grid(column=0, row=2, sticky=W+N, padx=(20, 20), pady=(0, 20))

        button_select_image = Button(
            self.tab_encode, text='Choose', command=self.choose_input, font=("Arial", 12))
        button_select_image.grid(column=0, row=1, sticky=W+N, padx=(20, 20))

        button_select_watermark = Button(
            self.tab_encode, text='Choose', command=self.choose_watermark, font=("Arial", 12))
        button_select_watermark.grid(
            column=0, row=3, sticky=W+N, padx=(20, 20))

        buttton_save_watermarked = Button(
            self.tab_encode, text='Encode', command=self.save_watermarked_image, font=("Arial", 12))
        buttton_save_watermarked.grid(
            column=0, row=4, sticky=W, padx=(20, 20), pady=(0, 20))

    def create_widgets_decode(self):
        self.tab_decode.columnconfigure(0, pad=20, weight=0)
        self.tab_decode.columnconfigure(1, pad=60, weight=1)
        self.tab_decode.rowconfigure(1, weight=0)
        self.tab_decode.rowconfigure(2, weight=1)
        self.tab_decode.rowconfigure(3, weight=0)

        lbl1 = Label(self.tab_decode, text='Select an image (.png)',
                     font=("Arial Bold", 14))
        lbl1.grid(column=0, row=0, sticky=W+N, padx=(20, 20), pady=(20, 20))

        button_select_image = Button(
            self.tab_decode, text='Choose', command=self.choose_input_watermarked, font=("Arial", 12))
        button_select_image.grid(column=0, row=1, sticky=W+N, padx=(20, 20))

        buttton_save_watermarked = Button(
            self.tab_decode, text='Decode', command=self.save_decoded_image, font=("Arial", 12))
        buttton_save_watermarked.grid(
            column=0, row=2, sticky=W, padx=(20, 20), pady=(0, 20))

    def choose_input(self):
        input_path = askopenfilename(filetypes=[('Png files', '.png')])
        if not input_path:
            return
        self.input_path = input_path
        print(input_path)
        img = Image.open(input_path)
        img.thumbnail((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        panel = Label(self.tab_encode, image=img)
        panel.image = img
        panel.grid(column=1, row=0, rowspan=2)

    def choose_watermark(self):
        watermark_path = askopenfilename(filetypes=[('Png files', '.png')])
        if not watermark_path:
            return
        self.watermark_path = watermark_path
        print(watermark_path)
        img = Image.open(watermark_path)
        img.thumbnail((170, 170), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        panel = Label(self.tab_encode, image=img)
        panel.image = img
        panel.grid(column=1, row=2, rowspan=2)

    def choose_input_watermarked(self):
        input_path = askopenfilename(filetypes=[('Png files', '.png')])
        if not input_path:
            return
        self.input_watermarked_path = input_path
        print(input_path)
        img = Image.open(input_path)
        img.thumbnail((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        panel = Label(self.tab_decode, image=img)
        panel.image = img
        panel.grid(column=1, row=0, rowspan=2)

    def save_watermarked_image(self):
        path = asksaveasfilename(filetypes=[('Png files', '.png')])
        if not path:
            return
        if self.watermark_path is None or self.input_path is None:
            messagebox.showerror(
                "Error", "You must select an input image and a watermark image")
            return
        if not path.endswith('.png'):
            path = path + '.png'
        stego.encrypt({
            'input_path':           self.input_path,
            'watermark_path':       self.watermark_path,
            'output_path':          path,
            'max_watermark_size':   128
        })
        messagebox.showinfo("Success", "Conversion finished!")

    def save_decoded_image(self):
        path = asksaveasfilename(filetypes=[('Png files', '.png')])
        if not path:
            return
        if self.input_watermarked_path is None:
            messagebox.showerror(
                "Error", "You must select an input image")
            return
        if not path.endswith('.png'):
            path = path + '.png'
        stego.decrypt({
            'input_path':           self.input_watermarked_path,
            'output_path':          path,
        })
        messagebox.showinfo("Success", "Conversion finished!")


root = Tk()
app = Application(window=root)
app.mainloop()
