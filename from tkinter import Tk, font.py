

from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import sqlite3
from io import BytesIO


def convert_to_blob(image_path):
    with open(image_path, 'rb') as image_file:
        image_blob = image_file.read()
    return image_blob


# Connecting to the database

def connect_to_db():
    connection = sqlite3.connect(r"D:\ChicagoSky\CSData.db")
    print("Database connection established")
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("Tables in the database:", cursor.fetchall())
    return connection

def insert_player_image(player_name, image_path):
    connection = connect_to_db()
    cursor = connection.cursor()

    # Convert the image to binary data
    image_blob = convert_to_blob(image_path)

    # Update the picture column
    query = """UPDATE Roster SET picture = ? WHERE name = ?"""
    cursor.execute(query, (image_blob, player_name))
    connection.commit()
    connection.close()


# Search button: fetching player details, including the picture
def search_player():
    player_name = en1.get().strip()
    if player_name:
        logo_lbl.pack_forget()
        Cslbl.pack_forget()

        connection = connect_to_db()
        cursor = connection.cursor()

        try:
            roster_query = '''SELECT name, pos, bio, picture FROM Roster WHERE name = ? '''
            cursor.execute(roster_query, (player_name,))
            player = cursor.fetchone()


            stats_query = """SELECT GP, GS, MIN, PTS, REB, AST, STL, BLK, TOV
                             FROM Stats
                             WHERE id = (
                             SELECT id FROM Roster WHERE name = ?); """

            cursor.execute(stats_query, (player_name,))
            stats = cursor.fetchone()  # Fetch player stats

            if player:
                name, pos, bio, pic = player

                # Update text labels
                name_label.config(text=f"Name: {name}\nPosition: {pos}")
                bio_label.config(text=f"{bio}")


                # Update player picture
                if pic:

                    try:
                        image = Image.open(BytesIO(pic))
                        image = image.resize((150, 100), Image.LANCZOS)  # Resize image
                        photo = ImageTk.PhotoImage(image)

                        #display image in the label
                        pic_label.config(image=photo, text='')
                        pic_label.image = photo
                        print("Image displayed successfully.")
                    except Exception as e:
                        print(f"Error displaying image: {e}")
                        pic_label.config(text="Error loading image.", image="")

                else:
                    pic_label.config(text="No Image Available", image="")



                # Update stats if they exist
                if stats:
                    gp, gs, minutes, points, rebounds, assists, steals, blocks, turnovers = stats
                    stats_label.config(text=f"Points: {points}\nRebounds: {rebounds}\nAssists: {assists}\n"
                                            f"Steals: {steals}\nBlocks: {blocks}\nTurnovers: {turnovers}")
                else:
                    stats_label.config(text="No stats available.")

                pic_label.pack(anchor="nw")
                name_label.pack(pady=5)
                bio_label.pack(fill="x")
                stats_label.pack(pady=5, padx=15)


            else:
                name_label.config(text="Player not found.")
                bio_label.config(text="")
                stats_label.config(text="")
                pic_label.config(image="", text="No Image Available")

                name_label.pack_forget()
                bio_label.pack_forget()
                stats_label.pack_forget()
                pic_label.pack_forget()

        except sqlite3.Error as e:

            print("Error executing query:", e)
        finally:
            connection.close()

    else:
        name_label.config(text="Please enter a player's name.")
        bio_label.config(text="")
        stats_label.config(text="")
        pic_label.config(image="", text="No Image Available")



# Creating the main window
win = Tk()
win.title("Chicago Sky")
win.geometry("800x800")
win.config(background='powder blue')

# Title label
Cslbl = Label(win, text="Chicago Sky", fg='dark blue',bg = 'Powder Blue',font=("Goudy Stout", 40 ))
Cslbl.pack(pady=2)

logo = PhotoImage(file="D:/ChicagoSky/ChiSky.png")
logo_lbl = Label(win, image=logo, bg='powderblue')
logo_lbl.pack(pady=50)


# Input for player name
en1 = Entry(win, width=20)
en1.pack(pady=5)

# Search button
btn1 = Button(win, text='Search', font='Helvetica 10 bold', command=search_player)
btn1.pack(pady=5)

# Display player's picture
pic_label = Label(win, text="", fg='dark blue',font='Helvetica 10 bold')



# Display player's name and position
name_label = Label(win, fg='dark blue',bg='powder blue', font='Arial 14')


# Display player's stats
stats_label = Label(win, text="",fg='yellow',bg='dark blue', bd=10, relief="groove", font=("Perpetua", 14 ))


# Display player's bio
bio_label = Label(win, text="", fg='yellow', bg='dark blue',font='Perpetua 10 bold', wraplength=500, bd=14, relief="groove" )


pic_label.pack_forget()
name_label.pack_forget()
bio_label.pack_forget()
stats_label.pack_forget()

win.mainloop()
