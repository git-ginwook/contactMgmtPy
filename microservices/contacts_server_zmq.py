import zmq
import contactsMS


def contacts_server():
    while True:
        # set zmq server socket to localhost:5554
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5554")
        print("waiting for a request from contacts microservice client...")

        while True:
            # receive request details from contacts client
            message = socket.recv()
            message = message.decode()
            message = int(message)

            # call contacts microservice with three parameters
            contacts_dict: dict or bool = contactsMS.contacts_ms(message)

            # reply to contacts client with the result
            if contacts_dict is False:
                contacts_dict = {'contacts': 'False'}

            socket.send_json(contacts_dict)

            # end contacts server once completed a contacts client request
            if contacts_dict:
                print("completed the request from contacts client.\n")
                break


if __name__ == '__main__':
    # TODO: need to have the zmq server running on a separate terminal
    print("zmq server for handshake microservice")
    contacts_server()
