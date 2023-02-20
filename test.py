import reminders_middleware as middleware

if __name__ == '__main__':
    data = {"email": "test@gmail.com", "password": "123456", "c_user_id": 0}
    r = middleware.handshake(data["email"], data["password"], data["c_user_id"])
    print(r)
    r2 = middleware.getreminders(data["c_user_id"])
    print(r2)