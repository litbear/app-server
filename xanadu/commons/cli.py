from xanadu import db
from xanadu.models.user import User
import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from sqlalchemy import MetaData

@click.command('init-db')
@with_appcontext
def init_db_command():
    User.__table__.create(db.get_engine())
    admin = User(username='admin', password=generate_password_hash('123456'))
    db.session.add(admin)
    db.session.commit()
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)