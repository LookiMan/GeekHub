"""
Сайт для виконання завдання: https://jsonplaceholder.typicode.com
Написати програму, яка буде робити наступне:
1. Робить запрос на https://jsonplaceholder.typicode.com/users і вертає коротку інформацію про користувачів (ID, ім'я, нікнейм)
2. Запропонувати обрати користувача (ввести ID)
3. Розробити наступну менюшку (із вкладеними пунктами):
   1. Повна інформація про користувача
   2. Пости:
      - перелік постів користувача (ID та заголовок)
      - інформація про конкретний пост (ID, заголовок, текст, кількість коментарів + перелік їхніх ID)
   3. ТУДУшка:
      - список невиконаних задач
      - список виконаних задач
   4. Вивести URL рандомної картинки

"""

from typing import Optional

import utils


_SESSION = {}


def set_user_id_form_session(user_id) -> None:
    _SESSION["user_id"] = user_id


def get_user_id_form_session() -> Optional[int]:
    return _SESSION.get("user_id")


def draw_screen(items) -> range:
    print(utils.Fore.YELLOW + "[>] ================")

    for index, item in enumerate(items, 1):
        print(utils.Fore.YELLOW + f"[{index}] {item}")

    return range(1, index + 1)


def menu(menu_items):
    items_range = draw_screen([item[0] for item in menu_items])

    menu_index = utils.safe_input(
        "[<] Insert number",
        validator=lambda inp: int(inp) in items_range,
        post_processor=int,
    )

    handler = menu_items[menu_index - 1][1]()


def user_info_screen():
    user_id = get_user_id_form_session()
    user = utils.get_user_by_id(user_id)

    for key, value in user.items():
        print(utils.Fore.CYAN + f"[>] {key}:   \t\t {value}")

    menu_items = (
        ("Back", main_screen),
        ("Exit", close_session),
    )

    menu(menu_items)


def all_posts():
    user_id = get_user_id_form_session()
    user_posts = utils.get_user_posts(user_id)

    print(utils.Fore.CYAN + "[>] User posts:")

    for post in user_posts:
        task_id = post.get("id")
        title = post.get("title")
        print(utils.Fore.CYAN + f"[>] id: {task_id} \t title: {title}")

    menu_items = (
        ("Back", posts_screen),
        ("Exit", close_session),
    )

    menu(menu_items)


def post_info():
    user_id = get_user_id_form_session()
    user_posts = utils.get_user_posts(user_id)

    all_users_posts_id = [post["id"] for post in user_posts]

    post_id = utils.safe_input(
        "[>] Insert post ID",
        validator=lambda inp: int(inp) in all_users_posts_id,
        post_processor=int,
    )

    print(utils.Fore.CYAN + f"[>] Info about posts with ID {post_id}")

    post = utils.get_user_post_by_id(user_id, post_id)
    comments = utils.get_comments_by_post_id(post_id)

    post_id = post.get("id")
    post_title = post.get("title")
    post_body = post.get("body")
    amount_comments = len(comments)
    comments_id = [str(comment["id"]) for comment in comments]

    print(utils.Fore.CYAN + f"[>] id: {post_id}")
    print(utils.Fore.CYAN + f"[>] title: {post_title}")
    print(utils.Fore.CYAN + f"[>] body: {post_body}")
    print(utils.Fore.CYAN + f"[>] amount comments: {amount_comments}")
    print(
        utils.Fore.CYAN + f"[>] comments ID:", utils.Fore.CYAN + ", ".join(comments_id)
    )

    menu_items = (
        ("Back", posts_screen),
        ("Exit", close_session),
    )

    menu(menu_items)


def posts_screen():
    menu_items = (
        ("All posts", all_posts),
        ("Info about post", post_info),
        ("Back", posts_screen),
    )

    menu(menu_items)


def completed_tasks():
    user_id = get_user_id_form_session()
    tasks = [
        task for task in utils.get_user_todos(user_id) if task.get("completed") == True
    ]

    print(utils.Fore.CYAN + "[>] Completed tasks:")

    for task in tasks:
        task_id = task.get("id")
        title = task.get("title")
        print(utils.Fore.CYAN + f"[>] id: {task_id} \t title: {title}")

    menu_items = (
        ("Back", todos_screen),
        ("Exit", close_session),
    )

    menu(menu_items)


def uncompleted_tasks():
    user_id = get_user_id_form_session()
    tasks = [
        task for task in utils.get_user_todos(user_id) if task.get("completed") == False
    ]

    print(utils.Fore.CYAN + "[>] Uncompleted tasks:")

    for task in tasks:
        task_id = task.get("id")
        title = task.get("title")
        print(utils.Fore.CYAN + f"[>] id: {task_id} \t title: {title}")

    menu_items = (
        ("Back", todos_screen),
        ("Exit", close_session),
    )

    menu(menu_items)


def todos_screen():
    menu_items = (
        ("completed tasks", completed_tasks),
        ("uncompleted tasks", uncompleted_tasks),
        ("Back", main_screen),
    )

    menu(menu_items)


def image_screen():
    photo = utils.get_random_image()
    print(utils.Fore.CYAN + "[>] ================")
    print(utils.Fore.CYAN + f"[>] url: {photo.get('url')}")

    menu_items = (
        ("Back", main_screen),
        ("Exit", close_session),
    )

    menu(menu_items)


def close_session() -> None:
    print("[>] Bye!")
    exit(0)


def main_screen():
    menu_items = (
        ("User info", user_info_screen),
        ("Posts", posts_screen),
        ("Todos", todos_screen),
        ("Random image", image_screen),
        ("Exit", close_session),
    )

    menu(menu_items)


def main():
    users = utils.get_users()

    users_id = [str(user["id"]) for user in users]

    print(utils.Fore.GREEN + "[>] Users ID:", utils.Fore.GREEN + ", ".join(users_id))
    user_id = utils.safe_input(
        "[<] Insert user ID",
        validator=lambda uid: uid in users_id,
        post_processor=int,
    )

    set_user_id_form_session(user_id)

    main_screen()


if __name__ == "__main__":
    main()
