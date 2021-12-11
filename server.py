import json
import socket, time, pickle, random, pygame

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
players_data = {
    "1": {
        "x": 10,
        "y": 20
    },
    "2": {
        "x": 20,
        "y": 10
    }
}
# list of connections
connection = []
speed = 3


def process_positions(player_id, key_ids):
    # key 0 up
    # key 1 down
    # key 2 left
    # key 3 right

    global speed

    x = players_data[player_id]["x"]
    y = players_data[player_id]["y"]

    for key_id in key_ids:
        if key_id == 0:
            y -= speed
        elif key_id == 1:
            y += speed
        elif key_id == 2:
            x -= speed
        elif key_id == 3:
            x += speed

    players_data[player_id]["x"] = x
    players_data[player_id]["y"] = y



def waiting_for_connections():
    while len(connection) < 2:
        conn, addr = serversocket.accept()
        connection.append(conn)
        print(conn)
        print(connection)


def recieve_information():
    # TODO: получить информацию от второго пользователя
    recv_data = connection[0].recv(2048)
    player_1_info = json.loads(recv_data.decode("utf-8"))

    return player_1_info #, player_2_info


waiting_for_connections()
while True:
    raw = json.dumps(players_data, ensure_ascii=False).encode("utf-8")
    connection[0].send(raw)
    print(raw)
    #connection[1].send(data_arr)

    player1_data = recieve_information()
    # TODO: process position
    p_1_data = process_positions("1", player1_data["keys"])
