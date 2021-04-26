from app import login_manager
from .users import UserModel

# catch an Exception and specify it instead of catching every exception
@login_manager.user_loader
def load_user(user_id):
    try:
        return UserModel.query.get(user_id)
    except Exception as e:
        print(e)
