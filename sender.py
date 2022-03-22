import random
from pathlib import Path
from bot_logging import logger
from user import Users
from generate_passwords import Generator
from main import bot


def send_message():
    db = Users()
    data = Generator()
    for user in db.users.values():
        if user.status == 10:
            logger.info(f"send message to {user.chat_id}:{user.username}")
            teams_password = data.teams[user.team.lower()].password
            bot.send_message(int(user.chat_id), f"Привет, держи креды.\nЛогин: {user.team}\nПароль: {teams_password}")
        else:
            logger.info(f"can't send message to {user.chat_id}:{user.username}. reason: user not complete registration")
        break


if __name__ == '__main__':
    send_message()
