from tkinter import *
from PIL import Image, ImageTk
import sqlite3
from io import BytesIO

# Creating the main window
win = Tk()
win.title("Chicago Sky")
win.geometry("800x800")

# Gradient background effect
canvas = Canvas(win, width=800, height=800)
canvas.pack(fill="both", expand=True)
gradient = PhotoImage(file="D:/ChicagoSky/gradient_bg.png")  # Use a gradient image
canvas.create_image(0, 0, image=gradient, anchor=NW)

# Title label with shadow effect
title_lbl = Label(win, text="CHICAGO SKY", fg='dark blue', font=('Rockwell', 40, 'bold'), bg='#ADD8E6')
title_lbl.place(x=220, y=50)

# Motto label
motto_lbl = Label(win, text="Rise Above!", fg='gold', font=('Georgia', 16, 'italic'), bg='#ADD8E6')
motto_lbl.place(x=350, y=110)

# Logo Image
logo = PhotoImage(file="D:/ChicagoSky/ChiSky.png")
logo_lbl = Label(win, image=logo, bg='#ADD8E6')
logo_lbl.place(x=300, y=150)

# Search Bar Styling
en1 = Entry(win, width=20, font=('Arial', 14), bd=3, relief='ridge', justify='center')
en1.place(x=320, y=320)

# Search Button Styling with Hover Effect
def on_enter(e):
    btn1.config(bg='gold', fg='black')

def on_leave(e):
    btn1.config(bg='white', fg='black')

btn1 = Button(win, text='Search', font=('Helvetica', 12, 'bold'), bd=2, relief='solid', command=lambda: print("Search pressed"))
btn1.place(x=370, y=360)
btn1.bind("<Enter>", on_enter)
btn1.bind("<Leave>", on_leave)

# Chicago Sky-themed Icons (Example: a basketball image near search bar)
basketball_icon = PhotoImage(file="D:/ChicagoSky/basketball_icon.png")
ball_lbl = Label(win, image=basketball_icon, bg='#ADD8E6')
ball_lbl.place(x=280, y=320)

# Subtle Watermark in Background
watermark = PhotoImage(file="D:/ChicagoSky/watermark_logo.png")  # Semi-transparent logo
watermark_lbl = Label(win, image=watermark, bg='#ADD8E6')
watermark_lbl.place(x=200, y=500)

win.mainloop()
