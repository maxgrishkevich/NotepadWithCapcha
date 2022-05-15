import string
import tkinter as tk
import random
from tkinter import messagebox, ttk, simpledialog, filedialog
from PIL import ImageTk, Image
from captcha.image import ImageCaptcha

alp = 'abcdefghijklmnopqrstuvwxyz'


def on_yscrollcommand(*args):
    scroll.set(*args)
    numbers.yview_moveto(args[0])


def scroll_command(*args):
    text.yview(*args)
    numbers.yview(*args)


def insert_numbers():
    count_of_lines = text.get(1.0, tk.END).count('\n') + 1
    numbers.config(state=tk.NORMAL)
    numbers.delete(1.0, tk.END)
    numbers.insert(1.0, '\n'.join(map(str, range(1, count_of_lines))))
    numbers.config(state=tk.DISABLED)


def on_edit(event):
    insert_numbers()
    text.edit_modified(False)


def todocx():
    tab_control.add(tab1, text='new*.docx')


def topdf():
    tab_control.add(tab1, text='new*.pdf')


def savefile():
    try:
        path = window.title().split('-')[1][1:]
    except:
        path = ''
    if path != '':
        with open(path, 'w') as f:
            content = text.get('1.0', tk.END)
            f.write(content)

    else:
        savefileas()

    text.edit_modified(False)


def savefileas():
    try:
        path = filedialog.asksaveasfile(filetypes=(("Text files", "*.txt"), ("All files", "*.*"))).name
        window.title('Cipher - ' + path)

    except:
        return

    with open(path, 'w') as f:
        f.write(text.get('1.0', tk.END))


def encrypt():
    t = text.get('1.0', tk.END)
    key = simpledialog.askstring('Wiegener', 'Enter key:')
    t = t.lower()[:-1]
    res = ""
    n = 0
    for i in t:
        letter = ((ord(i) - ord('a')) + ord(key[n]) - ord('a') + 1) % 26 + ord('a')
        res += chr(letter)
        n = (n + 1) % len(key)
    text.delete('1.0', tk.END)
    text.insert('1.0', res)


def decrypt():
    coded_text = text.get('1.0', tk.END)
    key = simpledialog.askstring('Wiegener', 'Enter key:')
    coded_text = coded_text.lower()[:-1]
    res = ""
    n = 0
    for i in coded_text:
        new_letter = (ord('z') + ((ord(i) - ord('a')) - ord(key[n]) + ord('a') - 1) - ord('a') + 1) % 26 + ord('a')
        res += chr(new_letter)
        n = (n + 1) % len(key)
    text.delete('1.0', tk.END)
    text.insert('1.0', res)


def clean():
    text.delete('1.0', tk.END)


def open_file():
    if not text.edit_modified():
        try:
            path = filedialog.askopenfile(filetypes=(("Text files", "*.txt"), ("All files", "*.*"))).name
            window.title('Cipher - ' + path)
            with open(path, 'r') as f:
                content = f.read()
                text.delete('1.0', tk.END)
                text.insert('1.0', content)
                text.edit_modified(False)
                tab_control.add(tab1, text=path)
        except:
            pass
    else:
        text.edit_modified(False)
        open_file()


def start_info():
    messagebox.showinfo('Warning!', 'This is a demo version so you can\'t save files')


def create_image():
    window.withdraw()
    captcha.deiconify()
    global random_string
    global image_label
    global image_display
    global entry
    global verify_label

    entry.delete(0, tk.END)

    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    image_captcha = ImageCaptcha(width=250, height=150)
    image_generated = image_captcha.generate(random_string)
    image_display = ImageTk.PhotoImage(Image.open(image_generated))

    image_label.grid_forget()
    image_label = tk.Label(captcha, image=image_display)
    image_label.grid(row=1, column=0, columnspan=3)


def check(x, y):
    if x.lower() == y.lower():
        captcha.withdraw()
        window.deiconify()
        start_info()
    else:
        messagebox.showinfo('Captcha', 'Wrong')
        create_image()


def on_closing():
    window.quit()


def window_config():
    window.title('Wiegener cipher')
    window.geometry('780x505')
    x = (window.winfo_screenwidth() - window.winfo_width() - 780) / 2
    y = (window.winfo_screenheight() - window.winfo_height() - 505) / 2
    window.wm_geometry("+%d+%d" % (x, y))

    tab_control.add(tab1, text='new*.txt')
    tab_control.pack(expand=1, fill='both')

    numbers.grid(row=0, column=0, sticky='NS')

    scroll.grid(row=0, column=2, sticky='NS')

    text.grid(row=0, column=1, sticky='NSWE')

    scroll.config(command=scroll_command)
    insert_numbers()
    text.bind('<<Modified>>', on_edit)
    tab1.grid_columnconfigure(1, weight=1)
    tab1.grid_rowconfigure(0, weight=1)

    menu = tk.Menu(window)
    menu.add_command(label="Open", command=open_file)
    menu.add_command(label="Clean", command=clean)
    menu.add_command(label="Save", command=savefile)
    menu.add_command(label="Save As", command=savefileas)
    menu.add_command(label="To .docx", command=todocx)
    menu.add_command(label="To .pdf", command=topdf)
    menu.add_command(label="Encrypt", command=encrypt)
    menu.add_command(label="Decrypt", command=decrypt)
    menu.add_command(label="Exit", command=window.quit)
    window.config(menu=menu)


def captcha_config():
    captcha.title('My Captcha')
    captcha.geometry('250x185')
    x = (captcha.winfo_screenwidth() - captcha.winfo_width() - 250) / 2
    y = (captcha.winfo_screenheight() - captcha.winfo_height() - 185) / 2
    captcha.wm_geometry("+%d+%d" % (x, y))
    captcha.resizable(width=False, height=False)

    entry.grid(row=2, column=0)
    create_image()

    submit_button = tk.Button(captcha, text="Submit", font="Calibri 10", width=4, borderwidth=2,
                           command=lambda: check(entry.get(), random_string))
    submit_button.grid(row=2, column=1)
    change_button = tk.Button(captcha, text="Change", font="Calibri 10", width=4, borderwidth=2, command=create_image)
    change_button.grid(row=2, column=2)
    captcha.bind('<Return>', func=lambda event: check(entry.get(), random_string))

    captcha.protocol("WM_DELETE_WINDOW", on_closing)


window = tk.Tk()
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
text = tk.Text(tab1, yscrollcommand=on_yscrollcommand, wrap=tk.NONE, font=('Calibri', 13))
numbers = tk.Text(tab1, width=3, bg='lightgray', state=tk.DISABLED, relief=tk.FLAT, font=('Calibri', 13))
scroll = ttk.Scrollbar(tab1)
window_config()


captcha = tk.Toplevel()
entry = tk.Entry(captcha, width=9, borderwidth=2, font="Calibri 15")
image_label = tk.Label(captcha)
captcha_config()


window.mainloop()
