import os

import peewee

from app import create_app
from app.models import *

DB = 'twitter_lite.db'
app = create_app()

if __name__ == '__main__':
    if os.path.exists(DB):
        os.remove(DB)

    peewee.create_model_tables([User, Post, Relationship])

    with app.app_context():
        User.gen_fake()
        Post.gen_fake()
        Relationship.gen_fake()
