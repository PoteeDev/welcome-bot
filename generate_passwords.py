import json
import random
from string import ascii_letters
from user import Users
from collections import defaultdict
from pathlib import Path


class Credentials:
    def __init__(self, team: str,
                 password: str,
                 members: list):
        self.team = team
        self.password = password
        self.members = members


def generate_passwords(n=24):
    return ''.join([random.choice(ascii_letters) for _ in range(n)])


class Generator(Users):
    def __init__(self):
        super().__init__()
        self.filename = Path("teams.json")
        self.teams = defaultdict(Credentials)
        self.read()

    def generate(self):
        for user in self.users.values():
            if self.teams.get(user.chat_id):
                self.teams[user.team.lower()].members.append(user.username)
            else:
                self.teams[user.team.lower()] = Credentials(team=user.team,
                                                            password=generate_passwords(),
                                                            members=[user.username])

    def read(self):
        if self.filename.exists():
            with self.filename.open() as t:
                teams = json.loads(t.read())
                self.teams = {x: Credentials(**y) for x, y in teams.items()}
        else:
            self.generate()
            self.save()

    def save(self):
        with self.filename.open("w") as t:
            t.write(json.dumps(self.teams, default=lambda x: x.__dict__))


if __name__ == '__main__':
    g = Generator()
    g.generate()
    g.save()
    g.read()
    print(g.teams)
