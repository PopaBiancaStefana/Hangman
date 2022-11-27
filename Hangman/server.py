import socket
from _thread import *
import time

max_clients = 2
nr_of_clients = 0                                                                                            
welcome_text = "█░█ ▄▀█ █▄░█ █▀▀ █▀▄▀█ ▄▀█ █▄░█\n█▀█ █▀█ █░▀█ █▄█ █░▀░█ █▀█ █░▀█"

side_player = -1
guess_player = -1
word = ""
description = ""
game_running = False
limit = 5
display = ""
already_guessed = []


def main():
    global max_clients
    global nr_of_clients
    global side_player

    # setup server
    ip = '127.0.0.1'
    port = 2020
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Server running on port: " + str(port))
    
    try:
        server.bind((ip, port))
    except socket.error as e:
        print(str(e))

    server.listen(max_clients)
    print("Waiting for a connection...")

    # setup clients
    # waiting for two clients to connect
 
    while True:
        if nr_of_clients < max_clients:
            client, addr = server.accept()
            print("Connected to: " + addr[0] + ":  " + str(addr[1]))
            nr_of_clients += 1
            start_new_thread(threaded_client, (client, ))


def threaded_client(client):
    global player_type
    global nr_of_clients
    global side_player
    global guess_player

    if (nr_of_clients == 1 or side_player == -1):
        side_player = client
        player_type = "side"
    else:
        guess_player = client
        player_type = "guess"

    if player_type == "side":
        handle_side_player(client)
    else:
        handle_guess_player(client)


def handle_side_player(client):
    global nr_of_clients
    global side_player
    global guess_player
    global word
    global description
    global game_running

    client.send(str.encode("Welcome to the \n\n" + welcome_text + "   game\n\nYou are the side player.\nPlease enter a word and a short description.. "))
    client.send(str.encode("side player"))

    # if game_running:
    #     client.send(str.encode("Game is already running.\n"))

    data = client.recv(2048)
    if data:
        
        if not word:
            word = data.decode("utf-8")
        print("Word: " + word)

        description = client.recv(2048)
        if description:
            description = description.decode("utf-8")
            print("Description: " + description)
        
        
        if guess_player == -1:
            reply = "You have to wait for the guess player to guess the word"
            client.sendall(str.encode(reply))
            while guess_player == -1:
                time.sleep(1)
         

        # disconect when guess player disconnects or game is over
        while guess_player != -1:
            time.sleep(1)

    side_player = -1
    nr_of_clients -= 1
    print("Client disconnected")
    client.close()
    



def handle_guess_player(client):
    global nr_of_clients
    global guess_player
    global game_running
    global limit
    global word
    global description
    global display

    game_running = True
    client.send(str.encode("\nWelcome to the \n\n" + welcome_text + "   game\n\nYou are the guess player.\nYou have to guess the word.\nYou have 5 lives.\n\nIf you get stuck, type 'hint' to get a short definition.\n\nYou may have to wait for the side player to give you a word."))
    client.send(str.encode("guess player"))

    # wait for side player to give a word
    while not word or not description:
        time.sleep(1)

    display = "_" * len(word)
    client.send(str.encode("You can now guess the word: " + display + " " + str(limit) + " lives left"))
  
    while True:
        data = client.recv(2048)

        # guess player disconnected 
        if not data:
            side_player.sendall(str.encode("Guess player is out"))
            side_player.sendall(str.encode("end of game"))
            game_running = False
            break
        
        # guess player wants a hint
        if data.decode("utf-8") == "hint":
            reply = "Hint: " + description

        else:
            reply = evaluate_guess(data.decode("utf-8"))
            # the side player watches the game
            side_player.sendall(str.encode(reply))
            
        print(reply)
        client.sendall(str.encode(reply))

        if game_running == False:
            break

    limit = 5
    display = ""
    word = ""
    description = ""
    guess_player = -1
    nr_of_clients -= 1
    print("Client disconnected")
    client.close()



def evaluate_guess(guess):
    global word
    global game_running
    global display
    global limit

    if len(guess.strip()) == 0 or len(guess.strip()) >= 2 or guess <= "9":
        return "\nInvalid Input, Try a letter\n" + display + " " + str(limit) + " lives left"

    if guess in already_guessed:
        return "\nLetter already guessed.\n " + display + " " + str(limit) + " lives left"

    elif guess in word:
        already_guessed.extend([guess])
        for index in range(len(word)):
            if word[index] == guess:
                display = display[:index] + guess + display[index + 1:]

        if "_" not in display:
            game_running = False
            return "\nWinner! The word is: " + display + "\nend of game"

        return "\n" + display + " " + str(limit) + " lives left"

    else:
        already_guessed.extend([guess])
        limit -= 1
        if limit == 0:
            game_running = False
            return "\nLoser! The word was: " + word + "\nend of game"

        return "\n" + display + " " + str(limit) + " lives left"




if __name__ == "__main__":
    main()
