from vedis import Vedis

def get_last_step(user_id):
    with Vedis('vedis/users.db') as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return None

def register_next_step(user_id, value):
    with Vedis('vedis/users.db') as db:
        try:
            db[user_id] = value
            return True
        except:
            return False

