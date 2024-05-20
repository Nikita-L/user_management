from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from user_management.settings import settings

engine = create_engine(str(settings.db_url_sync))
session_factory = sessionmaker(engine)
Session = scoped_session(session_factory)
