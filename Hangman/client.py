import sys
import socket


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

    welcome = client.recv(2048)
    print(welcome.decode("utf-8"))

    player_type = client.recv(2048)
    player_type = player_type.decode("utf-8")
    print("---------" + player_type)

    if player_type == "side player":
        
        word = input("Enter the word: ")
        client.send(str.encode(word))
        description = input("Enter the description: ")
        client.send(str.encode(description))
        
        # the side player only receives messages from know
        while True:
            data = client.recv(2048)
            if data.decode("utf-8") == "end of game":
                break

            print(data.decode("utf-8"))
           
            

    else:

        # the quess player receives and sends messages to server
        while True:
            # receive data
            data = client.recv(2048)
            print(data.decode("utf-8"))

            # send data
            msg = input("Enter a message: ")

            if msg == "exit":
                break

            client.send(str.encode(msg))

    # close connection to server
    client.close()
    



if __name__ == "__main__":
    main()
