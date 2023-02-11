import handshake_client_zmq

# call handshake microservice
r_user_id = int(input("Enter user id for Reminders app: "))
c_username = input("Enter username for Contacts app login: ")
c_password = input("Enter password for Contacts app login: ")
handshake_res: bool = handshake_client_zmq.handshake_client(r_user_id, c_username, c_password)

# call contacts microservice
