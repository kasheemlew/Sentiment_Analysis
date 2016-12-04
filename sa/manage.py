# coding: utf-8
"""
project management
 -- database management
    -- python manage.py db init: create migrations folder
    -- python manage.py db migrate: database migrate
    -- python manage.py db upgrate: upgrade database
    -- python manage.py shell
       >> Role.insert_roles() : create user roles

 -- add administrator
    -- python manage.py admin
       \_admin username:
       \_admin email:
       \_admin password:

 -- add users
    -- python manage.py adduser
       \_username:
       \_password:
       \_email:
       \_[1:moderator 2:admin 3:user]:

 -- run project
    -- python manage.py runserver

 -- shell environment
    -- python manage.py shell

 -- run your unit tests
    -- python manage.py test

"""

import sys
import os
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import db, app
from app.models import User, Role, Comment

# 编码设置
reload(sys)
sys.setdefaultencoding('utf-8')


manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """自动加载环境"""
    return dict(
        app = app,
        db = db,
        User = User,
        Role = Role,
        Comment = Comment
    )


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """run your unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def admin():
    """add administrator"""
    from getpass import getpass
    username = raw_input("\_admin username: ")
    email = raw_input("\_admin email: ")
    password = getpass("\_admin password: ")
    u = User(
        email = email,
        username = username,
        password = password,
        role_id = 2
    )
    db.session.add(u)
    db.session.commit()
    print "<admin user %s add in database>" % username


@manager.command
def adduser():
    """add user"""
    from getpass import getpass
    username = raw_input("\_username: ")
    email = raw_input("\_email: ")
    role_id = raw_input("\_[1:moderator 2:admin 3:user]: ")
    password = getpass("\_password: ")
    u = User(
        email = email,
        username = username,
        password = password,
        role_id = role_id
    )
    db.session.add(u)
    db.session.commit()
    print "<user %s add in database>" % username


@manager.command
def crawler():
    """crawler"""
    print "Uncomment the utilities to start the crawler!"
    # from app.crawlers.taoke import taoke
    # taoke()

    # from app.crawlers.ixuanxiu import ixuanxiu
    # ixuanxiu()

    # from app.crawlers.xuanxiuke import xuanxiuke
    # xuanxiuke()


@manager.command
def parse():
    """parse the comments"""
    import jieba
    import jieba.posseg as pseg

    handled_count = 0

    # Load User's Dictionary
    path_list = os.getcwd().split('/')
    path_list.append("dict.txt")
    dict_path = '/'.join(path_list)
    jieba.load_userdict(dict_path)

    # Disimss These Flags
    dismiss = ['b', 'c', 'x', 'r', 'm', 'uj', 'u', 'p', 'q', 'ns', 'nr', 'nr1',
            'nr2', 'nsf', 'n', 'nz', 'uz', 't', 'ul', 'k', 'f', 'ud', 'ug', 'uv']

    comments = Comment.query.all()
    for comment in comments:
        word_list = []
        pseg_cut = pseg.cut(comment.body)
        for word, flag in pseg_cut:
            if flag not in dismiss:
                word_list.append(word)
        comment.parsed = '/'.join(word_list)
        handled_count += 1
        db.session.add(comment)
        print "Comment %04d Parsed!" % handled_count

    db.session.commit()
    print "ALL DONE!"


if __name__ == '__main__':
    manager.run()

