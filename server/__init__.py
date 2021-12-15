import json
import socket, time, pickle, random, pygame
from server.db import connections, speed, data

# create socket and initalize connection type
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# get hostname of Network server is on
hostname = socket.gethostname()
print(hostname)

# use hostname to get ipaddress
ip_address = socket.gethostbyname(hostname)
# bind socket to port and ip address
serversocket.bind((ip_address, 5555))
print(ip_address)

# listen for connections
serversocket.listen()


# Create list of postions to be sent to client


def process_positions(player_id, key_ids):
    # key 0 up
    # key 1 down
    # key 2 left
    # key 3 right

    global speed

    x = data['players_data'][player_id]["x"]
    y = data['players_data'][player_id]["y"]

    for key_id in key_ids:
        if key_id == 0:
            y -= speed
        elif key_id == 1:
            y +=speed
        elif key_id == 2:
            x -= speed
        elif key_id == 3:
            x += speed

    if x >= 800:
        x = 800
    if y >= 600:
        y = 600
    if x < 0:
        x = 0
    if y < 0:
        y = 0



    data['players_data'][player_id]["x"] = x
    data['players_data'][player_id]["y"] = y


def waiting_for_connections():
    while len(connections) < 2:
        conn, addr = serversocket.accept()
        connections.append(conn)
        print('', conn)
    data['game'] = True


def recieve_information():
    recv_data = connections[0].recv(2048)
    player_1_info = json.loads(recv_data.decode("utf-8"))

    recv_data = connections[1].recv(2048)
    player_2_info = json.loads(recv_data.decode("utf-8"))

    return {
        player_1_info['id']: player_1_info['keys'],
        player_2_info['id']: player_2_info['keys'],
    }


def main():
    waiting_for_connections()
    while True:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        connections[0].send(raw)
        connections[1].send(raw)
        players_keys = recieve_information()
        for player_id in players_keys.keys():
            process_positions(player_id, players_keys[player_id])
