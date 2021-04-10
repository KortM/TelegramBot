from vedis import Vedis

def set_step(user_id, step) -> bool:
    try:
        with Vedis('user_state.db') as db:
            db[user_id] = step
    except Exception:
        return False

def get_last_step(user_id) -> str or bool:
    try:
        with Vedis('user_state.db') as db:
            return db[user_id].decode()
            
    except Exception:
        return False
