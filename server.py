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


def process_positions(player_id, key_ids, position):
    # key 0 up
    # key 1 down
    # key 2 left
    # key 3 right

    global speed

    x = position["x"]
    y = position["y"]

    for key_id in key_ids:
        if key_id == 0:
            y -= speed
        elif key_id == 1:
            y += speed
        elif key_id == 2:
            x -= speed
        elif key_id == 3:
            x += speed

    return {
        player_id: {
            "x": x,
            "y": y
        }
    }


def waiting_for_connections():
    while len(connection) < 2:
        conn, addr = serversocket.accept()
        connection.append(conn)
        print(conn)
        print(connection)


def recieve_information():
    player_1_info = pickle.loads(connection[0].recv(1024))
    player_2_info = pickle.loads(connection[1].recv(1024))

    return player_1_info, player_2_info


while True:
    waiting_for_connections()

    data_arr = pickle.dumps(players_data)
    print(data_arr)
    connection[0].send(data_arr)
    connection[1].send(data_arr)

    player1, player2 = recieve_information()
    p_1_data =  process_positions("", player2)
