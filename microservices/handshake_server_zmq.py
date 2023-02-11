import zmq
import json
import handshakeMS


def handshake_server():
    # set zmq server socket to localhost:5555
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("waiting for a request from handshake microservice client...")

    while True:

        # receive request details from handshake client
        message = socket.recv_json()

        # call handshake microservice with three parameters
        message = json.loads(json.dumps(message))
        is_synced: bool = handshakeMS.handshake_ms(message["request"]['r_user_id'],
                                                   message['request']['c_username'],
                                                   message['request']['c_password'])

        # convert boolean to string
        if is_synced:
            result = '1'
        else:
            result = '0'

        # reply to handshake client with the result
        socket.send(result.encode())

        # end handshake server once completed a handshake client request
        if message:
            print("completed the request from handshake client.\n")
            break


if __name__ == '__main__':
    # TODO: need to have the zmq server running on a separate terminal
    print("zmq server for handshake microservice")
    handshake_server()
