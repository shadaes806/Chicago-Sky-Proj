from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import sqlite3
from io import BytesIO
import os

def convert_to_blob(image_path):
    with open(image_path, 'rb') as image_file:
        image_blob = image_file.read()
    return image_blob

# Connecting to the database
def connect_to_db():
    db_path = "C:\\Users\\keyon\\PycharmProjects\\ChicagoSky\\CSData.db"
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return None
    return sqlite3.connect(db_path)

def insert_player_image(player_name, image_path):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()

        # Convert the image to binary data
        image_blob = convert_to_blob(image_path)

        # Update the picture column
        query = """UPDATE Roster SET picture = ? WHERE name = ?; """
        cursor.execute(query, (image_blob, player_name))
        connection.commit()
        connection.close()

# Search button: fetching player details, including the picture
def search_player():
    player_name = en1.get().strip()
    if not player_name:
        name_label.config(text="Please enter a player's name.")
        bio_label.config(text="")
        stats_label.config(text="")
        pic_label.config(image="", text="No Image Available")
        return

    connection = connect_to_db()
    if not connection:
        name_label.config(text="Error connecting to the database.")
        bio_label.config(text="")
        stats_label.config(text="")
        pic_label.config(image="", text="No Image Available")
        return

    cursor = connection.cursor()

    # Query for player details
    roster_query = """SELECT name, pos, bio, picture FROM Roster WHERE name = ?;"""
    cursor.execute(roster_query, (player_name,))
    player = cursor.fetchone()

    # Query for player stats
    stats_query = """SELECT GP, GS, MIN, PTS, REB, AST, STL, BLK, TOV
                     FROM Stats
                     WHERE id = (
                     SELECT id FROM Roster WHERE name = ?); """
    cursor.execute(stats_query, (player_name,))
    stats = cursor.fetchone()  # Fetch player stats

    connection.close()

    if player:
        name, pos, bio, pic = player

        # Update text labels
        name_label.config(text=f"Name: {name}\nPosition: {pos}")
        bio_label.config(text=f"Bio: {bio}")

        # Update player picture
        if pic:
            image = Image.open(BytesIO(pic))
            image = image.resize((150, 150), Image.ANTIALIAS)  # Resize image
            photo = ImageTk.PhotoImage(image)
            pic_label.config(image=photo, text='')
            pic_label.image = photo
        else:
            pic_label.config(text="No Image Available", image="")

        # Update stats if they exist
        if stats:
            gp, gs, minutes, points, rebounds, assists, steals, blocks, turnovers = stats
            stats_label.config(text=f"Points: {points}\nRebounds: {rebounds}\nAssists: {assists}\n"
                                        f"Steals: {steals}\nBlocks: {blocks}\nTurnovers: {turnovers}")
        else:
            stats_label.config(text="No stats available.")

    else:
        name_label.config(text="Player not found.")
        bio_label.config(text="")
        stats_label.config(text="")
        pic_label.config(image="", text="No Image Available")

# Creating the main window
win = Tk()
win.title("Chicago Sky")
win.geometry("500x600")
win.config(background='powder blue')

# Title label
Cslbl = Label(win, text="Chicago Sky", fg='dark blue',bg='powder blue', font='Helvetica 30 bold')
Cslbl.pack(pady=20)

# Input for player name
en1 = Entry(win, width=20)
en1.pack(pady=5)

# Search button
btn1 = Button(win, text='Search', command=search_player)
btn1.pack(pady=5)

# Display player's name and position
name_label = Label(win, fg='dark blue',bg='powder blue', font='Arial 14')
name_label.pack(pady=5)

# Display player's stats
stats_label = Label(win, text="Player stats will appear here.",fg='dark blue',bg='powder blue', font='Helvetica 30 bold')
stats_label.pack(pady=5)

# Display player's bio
bio_label = Label(win, text="Bio will appear here.", fg='dark blue',bg='powder blue', font='Helvetica 30 bold')
bio_label.pack(pady=5)

# Display player's picture
pic_label = Label(win, text="Player picture will appear here.", fg='dark blue',bg='powder blue',font='Helvetica 30 bold')
pic_label.pack(pady=5)

win.mainloop()
