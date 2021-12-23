from collections.abc import Callable
from typing import Optional
import random

from colorama import init, Fore

import requests


init(autoreset=True)


def safe_input(
    prompt: str, *, validator: Callable, post_processor: Optional[Callable] = None
) -> str:
    quit_commands = ("q", "quit", "-q", "--quit")

    print(Fore.GREEN + "[>] ================")
    while True:
        raw_input = input(Fore.GREEN + f"{prompt}: ").strip()

        if raw_input.strip().lower() in quit_commands:
            raise BaseException

        try:
            if not validator(raw_input):
                raise Exception()
        except:
            print(Fore.RED + "[!] Insert correct value")
        else:

            if post_processor:
                return post_processor(raw_input)
            else:
                return raw_input


def make_request(url, params: dict = None) -> list:
    try:
        response = requests.get(url, params)
    except:
        return list()
    else:
        return response.json()


def get_users() -> list:
    return make_request("https://jsonplaceholder.typicode.com/users")


def get_user_by_id(user_id: int) -> Optional[dict]:
    for user in get_users():
        if user["id"] == user_id:
            return user


def get_user_posts(user_id: int) -> list:
    url = f"https://jsonplaceholder.typicode.com/posts"

    return make_request(url, {"userId": user_id})


def get_user_post_by_id(user_id: int, post_id: int) -> Optional[dict]:
    for post in get_user_posts(user_id):
        if post["id"] == post_id:
            return post


def get_random_image() -> dict:
    url = "https://jsonplaceholder.typicode.com/photos"
    photos = make_request(url)

    if photos:
        return random.choice(photos)
    else:
        return dict()


def get_user_todos(user_id: int) -> list:
    url = f"https://jsonplaceholder.typicode.com/todos"

    return make_request(url, {"userId": user_id})


def get_comments_by_post_id(post_id: int) -> list:
    url = f"https://jsonplaceholder.typicode.com/comments"

    return make_request(url, {"postId": post_id})
