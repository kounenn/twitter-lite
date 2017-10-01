from datetime import date, datetime

from peewee import *
from playhouse.flask_utils import FlaskDB
from werkzeug.security import generate_password_hash, check_password_hash

flask_db = FlaskDB()


class BaseModel(flask_db.Model):
    id = PrimaryKeyField()


class User(BaseModel):
    email = CharField(max_length=64, unique=True)
    username = CharField(max_length=64, unique=True)
    password_hash = CharField(max_length=128)
    join_date = DateField(default=date.today)
    name = CharField(max_length=64, null=True)
    location = CharField(max_length=64, null=True)
    about_me = CharField(max_length=1024, null=True)

    class Meta:
        order_by = ('username',)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def following(self):
        return User.select().join(
            Relationship, on=Relationship.to_user, ).where(
            Relationship.from_user == self
        )

    def followers(self):
        return User.select().join(
            Relationship, on=Relationship.from_user, ).where(
            Relationship.to_user == self
        )

    def is_following(self, user):
        return Relationship.select().where(
            (Relationship.from_user == self) &
            (Relationship.to_user == user)
        ).count() > 0

    def follow(self, user):
        if self == user:
            return False
        if self.is_following(user):
            return False
        with flask_db.database.atomic():
            try:
                Relationship.create(from_user=self, to_user=user)
            except IntegrityError:
                flask_db.database.rollback()
                return False
        return True

    def unfollow(self, user):
        if self == user:
            return False
        if not self.is_following(user):
            return False
        with flask_db.database.atomic():
            try:
                Relationship.delete().where(
                    (Relationship.from_user == self) & (Relationship.to_user == user)
                ).execute()
            except IntegrityError:
                flask_db.database.rollback()
                return False
        return True

    @staticmethod
    def gen_fake(count=100):
        from peewee import IntegrityError
        from random import seed
        import forgery_py
        seed()
        for i in range(count):
            with flask_db.database.atomic():
                try:
                    User.create(email=forgery_py.internet.email_address(),
                                username=forgery_py.internet.user_name(),
                                password=forgery_py.lorem_ipsum.word(),
                                join_data=forgery_py.date.datetime(True),
                                name=forgery_py.name.full_name(),
                                location=forgery_py.address.city(),
                                about_me=forgery_py.lorem_ipsum.sentence())
                except IntegrityError:
                    flask_db.database.rollback()


class Relationship(flask_db.Model):
    from_user = ForeignKeyField(User, related_name='from_user')
    to_user = ForeignKeyField(User, related_name='to_user')

    class Meta:
        indexes = (
            (('from_user', 'to_user'), True),
        )

    @staticmethod
    def gen_fake(count=1000):
        from random import seed, randint
        from peewee import IntegrityError

        seed()
        user_count = User.select().count()
        for i in range(count):
            f = User.select().offset(randint(1, user_count - 1))[0]
            t = User.select().offset(randint(1, user_count - 1))[0]
            with flask_db.database.atomic():
                try:
                    Relationship.create(from_user=f, to_user=t)
                except IntegrityError:
                    flask_db.database.rollback()


class Post(BaseModel):
    content = TextField()
    timestamp = DateTimeField(index=True, default=datetime.utcnow)
    author = ForeignKeyField(User, related_name='posts')

    class Meta:
        order_by = ('-timestamp',)

    @staticmethod
    def gen_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.select().count()
        for i in range(count):
            u = User.select().offset(randint(1, user_count - 1))[0]
            Post.create(content=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                        timestamp=forgery_py.date.datetime(True),
                        author=u)
