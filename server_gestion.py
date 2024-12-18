from utils import on_quit
from my_struct import info
from my_struct import HOST, PORT
from my_struct import json, socket

def connect_to_server():
    try:
        info.client.connect((HOST, PORT))
        print("Connexion au serveur réussie.")
    except socket.error as e:
        print(f"Erreur de connexion au serveur: {e}")
        on_quit()

def receive_messages():
    connect_to_server()
    while not info.stop_event_client.is_set():
        try:
            info.response = info.client.recv(1024).decode('utf-8')
            message = json.loads(info.response)
            if not info.response:
                print("Le serveur a fermé la connexion.")
                break
            for _gamertag in message['GAMERTAGS']:
                info.gamertags_list.append(_gamertag)
        except Exception as e:
            print(f"Erreur de réception du message: {e}")
            break