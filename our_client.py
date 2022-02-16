from socket import socket, AF_INET, SOCK_STREAM
from struct import pack, unpack
from xmlrpc.client import boolean

PORT = 0x2BAD
SERVER = "127.0.0.1"

if __name__ == '__main__':
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((SERVER, PORT))
        num = unpack('!i', sock.recv(4))[0]
        print(f"You're player {num}")
        isReady = False
        while (not isReady):
                print("Veuillez appuyer sur R pour confirmer")
                content = input().lower()
                if(content == "r"):
                    isReady = True
                    sock.send(pack('?', isReady))
        while True:
            first_letter = sock.recv(4096).decode('utf-8')
            wordIsCorrect = False
            while (not wordIsCorrect):
                content = input(f"Veuillez rentrer un mot commençant par {first_letter} \n").lower()
                sock.send(content.encode())
                wordCode = unpack('!i', sock.recv(4))[0]  #Reception code associé au mot
                score = unpack('!i', sock.recv(4))[0]
                if(wordCode == 0):
                    print("Mot correct")
                    wordIsCorrect = True
                elif(wordCode == 1):
                    print("Mauvaise première lettre")
                elif(wordCode == 2):
                    print("Le mot n'existe pas, il ne fallait pas sécher les cours de français au collège en classe de 6ème B (la classe basket).")
                elif(wordCode == 3):
                    print("Vous avez gagner la partie !")
                    sock.close()

                print("--------------------------")
                print(f"Votre score est de {score}")
            # elif content in ['h', 't']:
            #     sock.send(pack('?', content == 'h'))
            #     is_head = unpack('?', sock.recv(1))[0]
            #     score_num = unpack('!i', sock.recv(4))[0]
            #     print(f"It was {'HEAD' if is_head else 'TAIL'}, here are the scores :")
            #     for i in range(1, score_num+1):
            #         score = unpack('!i', sock.recv(4))[0]
            #         print(f"- Player {i}{' (you)' if i == num else ''} : {score if score>=0 else '-'}")