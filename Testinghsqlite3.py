import sqlite3

def insert_image(player_name, image_path):
    connection = sqlite3.connect(r"D:\ChicagoSky\CSData.db")  # Use the correct path to your database
    cursor = connection.cursor()

    try:
        # Read the image file in binary mode
        with open(image_path, 'rb') as file:
            blob_data = file.read()

        # Update the picture column for the specific player
        cursor.execute('''
            UPDATE Roster
            SET picture = ?
            WHERE name = ?;
        ''', (blob_data, player_name))

        connection.commit()
        print(f"Image successfully inserted for {player_name}.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    # Example: Add images for players
    players = [
        {"name": "Kamilla Cardoso", "image": r"D:\ChicagoSky\KamillaCardoso.jpg"},
        {"name": "Lindsay Allen", "image": r"D:\ChicagoSky\LindsayAllen.jpg"},
        {"name": "Kaela Davis", "image": r"D:\ChicagoSky\KaelaDavis.jpg"},
        {"name": "Dana Evans", "image": r"D:\ChicagoSky\DanaEvans.jpg"},
        {"name": "Isabelle Harrison", "image": r"D:\ChicagoSky\IsabelleHarrison.jpg"},
        {"name": "Moriah Jefferson", "image": r"D:\ChicagoSky\MoriahJefferson.jpg"},
        {"name": "Brianna Turner", "image": r"D:\ChicagoSky\BriannaTurner.jpg"},
        {"name": "Diamond DeShields", "image": r"D:\ChicagoSky\DiamondDeShields.jpg"},
        {"name": "Rachel Banham", "image": r"D:\ChicagoSky\RachelBanham.jpg"},
        {"name": "Michaela Onyenwere", "image": r"D:\ChicagoSky\MichaelaOnyenwere.jpg"}
     

    ]

    for player in players:
        insert_image(player["name"], player["image"])
