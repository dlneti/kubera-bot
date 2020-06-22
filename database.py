from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
from models import Base as DbBase

engine = create_engine('postgresql://f:123@localhost:5432/kubera-bot')
Session = sessionmaker(bind=engine)

class DbManager(Base):
    def __init__(self):
        self.db = False

    def _perform_transaction(self):
        self.db.commit()
        self.db.close()

    def _get_session(self):
        if not self.db:
            self.db = Session()

    def _insert(self, obj):
        self.db.add(obj)

    def _save(self, obj):
        if isinstance(obj, list):
            for model in obj:
                self._save(model)
            return

        assert isinstance(obj, DbBase)
        self._insert(obj)

    def save(self, obj):
        self._get_session()             # session init
        self._save(obj)                 # perform transaction
        self._perform_transaction()     # session teardown
