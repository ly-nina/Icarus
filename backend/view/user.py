from slim.support.peewee import PeeweeView
from model.user import User
from view import route


@route('user')
class UserView(PeeweeView):
    model = User