from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
from models import Base as DbBase
from utils import setup_logging

engine = create_engine('postgresql://f:123@localhost:5432/kubera-bot')
Session = sessionmaker(bind=engine)
logger = setup_logging(__name__)

class DbManager(Base):
    def __init__(self):
        self.db = False
        self.logger = setup_logging(self, class_name=True, prefix_path=__name__)

    def _perform_transaction(self):
        self.db.commit()
        self.db.close()

    def _get_session(self):
        if not self.db:
            self.db = Session()

    def _insert(self, obj):
        self.logger.info(obj.json)
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
        self._save(obj)                 # save to db
        self._perform_transaction()     # session teardown
