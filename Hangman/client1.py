import sys
import socket
import re


def main():
    if len(sys.argv) < 3:
        print("Please enter the IP and PORT number ")
        sys.exit()

    ip = str(sys.argv[1])
    port = int(sys.argv[2])

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server
    try:
        client.connect((ip, port))
    except socket.error as e:
        print(str(e))
        sys.exit()

    player_type = client.recv(2048)
    player_type = player_type.decode("utf-8")
 
    if player_type == "side player":
        
        while(True):

            data = client.recv(2048)     
            print(data.decode("utf-8"))

            if(data.decode("utf-8").startswith("End of game")):
                break

            word, description = get_word_description()
            client.send(str.encode(word))
            client.send(str.encode(description))

    # close connection to server
    client.close()
    

def get_word_description():
     # get word
    word = input("Enter the word: ")
    while(not word.isalpha()):
        word = input("Enter the word: ")
          
    # get description
    description = input("Enter the description: ")
    while(not description):
        description = input("Enter the description: ")
    
    return word, description


if __name__ == "__main__":
    main()
