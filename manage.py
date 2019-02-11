import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from mysite import app, db

from models import Post, Tags

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
