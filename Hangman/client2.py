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

 

    if player_type == "guess player":

        while True:
            # receive data
            data = client.recv(2048)
            print(data.decode("utf-8"))

            if data.decode("utf-8").endswith("end of game"):
                msg = input("Want to play again? (y/n): ")
                if(msg == "y"):
                    client.send(str.encode("y"))
                else:
                    client.send(str.encode("n"))
                    break
            else:
                # send data
                msg = input("\nEnter the quess: ")
                while(not msg):
                    msg = input("Enter the quess: ")

                if msg == "exit":
                    break
                else:
                    client.send(str.encode(msg))

    # close connection to server
    client.close()
    

if __name__ == "__main__":
    main()
