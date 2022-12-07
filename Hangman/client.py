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

    welcome = client.recv(2048)
    print(welcome.decode("utf-8"))

 

    if player_type == "side player":
        
        if( not welcome.decode("utf-8").endswith("Please come back later.")):

            # get word
            word = input("Enter the word: ")
            while(not word.isalpha()):
                word = input("Enter the word: ")
            client.send(str.encode(word))

            # get description
            description = input("Enter the description: ")
            while(not description):
                description = input("Enter the description: ")
            client.send(str.encode(description))
        
            data = client.recv(2048)     
            print(data.decode("utf-8"))     

    else:

        while True:
            # receive data
            data = client.recv(2048)
            print(data.decode("utf-8"))

            if data.decode("utf-8").endswith("end of game"):
                break

            # send data
            msg = input("\nEnter the quess: ")
            while(not msg):
                msg = input("Enter the quess: ")

            if msg == "exit":
                break

            client.send(str.encode(msg))

    # close connection to server
    client.close()
    

if __name__ == "__main__":
    main()
