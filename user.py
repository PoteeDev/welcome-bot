import json
from pathlib import Path


class User:
    def __init__(self, name: str = "",
                 group: str = "",
                 team: str = "",
                 status: int = -1,
                 chat_id: int = -1,
                 username: str = ""):
        self.name = name
        self.username = username
        self.group = group
        self.team = team
        self.status = status
        self.chat_id = chat_id

    def set_group(self, group):
        self.group = group


class Users:
    def __init__(self):
        self.path = Path("users.json")
        self.users = dict()
        self.load_users()

    def load_users(self):
        if self.path.exists():
            with self.path.open() as u:
                users = json.loads(u.read())['users']
                for key, value in users.items():
                    self.users[key] = User(**value)

    def save(self):
        with self.path.open("w") as u:
            users = {k: v.__dict__ for k, v in self.users.items()}
            u.write(json.dumps({"users": users}, indent=2))
