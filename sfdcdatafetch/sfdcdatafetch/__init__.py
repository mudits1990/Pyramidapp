from pyramid.config import Configurator
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy.orm import sessionmaker
from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = create_engine('mysql+mysqldb://root:admin@localhost/mydb1')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('sObjects', '/sObjects')
    config.add_route('getTable','/getTable')
    config.scan()
    return config.make_wsgi_app()
