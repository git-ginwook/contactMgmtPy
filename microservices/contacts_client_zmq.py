import zmq
import json
import time


def contacts_client(r_user_id: int) -> dict or bool:
    # set zmq client socket to localhost:8888
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5554")
    print("connecting to a local zmq server...")

    # send request to zmq server socket
    print("sending request to contacts microservice...")

    # convert int to string
    r_user_id = str(r_user_id)
    socket.send(r_user_id.encode())

    # give enough time to process the handshake client request
    time.sleep(5)

    # receive result from the handshake server
    result = socket.recv_json()
    if result['contacts'] == 'False':
        result = False

    # end the handshake client by returning `result`
    return result


if __name__ == '__main__':
    print("zmq client for contacts microservice")
