import zmq
import json
import time


def handshake_client(r_user_id: int, c_username: str, c_password: str) -> bool:
    # set zmq client socket to localhost:5555
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    print("connecting to a local zmq server...")

    # collect and convert three inputs to JSON
    request: object = json.loads(json.dumps({
        'request': {
            'r_user_id': r_user_id,
            'c_username': c_username,
            'c_password': c_password
        }
    }))

    # send request to zmq server socket
    print("sending request to handshake microservice...")
    socket.send_json(request)

    # give enough time to process the handshake client request
    time.sleep(5)

    # receive result from the handshake server
    result = socket.recv()
    result = result.decode()

    # convert string to boolean
    if result == '1':
        result = True
    else:
        result = False

    # end the handshake client by returning `result`
    return result


if __name__ == '__main__':
    print("zmq client for handshake microservice")
