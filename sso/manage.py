""" скрипт для выполнения миграций """

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from init import app, db
from models import *

manager = Manager(app)

if __name__ == '__main__':
    application = app
    migrate = Migrate(app, db)

    manager.add_command('db', MigrateCommand)
    manager.run()