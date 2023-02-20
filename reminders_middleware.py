import requests


def handshake(email: str, password: str, c_user_id: int) -> str:
    data = {"email": email, "password": password, "c_user_id": c_user_id}
    r = requests.post("http://localhost:8001/handshake", json=data)
    if r.status_code != 500:
        return r.json()["message"]
    else:
        return "Server error"


def getreminders(c_user_id: int):
    data = {"c_user_id": c_user_id}
    r = requests.get("http://localhost:8001/getreminders", json=data)
    print(r)
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 404:
        return r.json()["message"]
    else:
        return "Server error"
