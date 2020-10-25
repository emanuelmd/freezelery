import random

from celery import Celery, group

# Configuration

broker = 'redis://localhost:6379'
backend = 'redis://localhost:6379'

app = Celery('freezelery', broker=broker, backend=backend)

celery_app = app

# Task logic

names = ['Joshua', 'John', 'Alice', 'Billie', 'Mary', 'Chacalon', 'Guido', 'Sanic']

# Setting this to False will prevent exceptions
should_ban_users = True

class BannedUser(Exception):
    pass

@app.task
def fetch_user():
    name = random.choice(names)
    return {'name': name}

@app.task
def fetch_details_for_user(d):
    d['age'] = random.randint(18, 71)

    is_user_banned = random.randint(0, 1) == 1

    if is_user_banned and should_ban_users:
        raise BannedUser()

    return d

@app.task
def send_welcome_email(d):
    name = d['name']
    print(f'Sending email to user: {name}')
    return d

@app.task
def print_user_to_file(d):
    name = d['name']
    age = d['age']
    print(f'Name: {name}, Age: {age}')
    return d

def build_task(n):

    def workflow():
        return (
            fetch_user.s() |
            fetch_details_for_user.s() |
            group(send_welcome_email.s(), print_user_to_file.s()))

    # The following composition works,
    # it propagates the Exception correctly
    # although it's slightly different

    # def correct_workflow():
    #     return (
    #         fetch_user.s() |
    #         fetch_details_for_user.s() |
    #         send_welcome_email.s() |
    #         print_user_to_file.s()
    #     )

    return group([workflow() for _ in range(0, n)])
        
# Exports

__all__ = ('celery_app', )

