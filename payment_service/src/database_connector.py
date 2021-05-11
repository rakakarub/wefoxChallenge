from pony import orm
import os
from datetime import datetime, date

class DatabaseConnector:
    def __init__(self):
        self.db = orm.Database()
        self.db_params = {
        'provider': 'postgres',
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
        'database': os.getenv('POSTGRES_DB')
    }
    def define_entities(self, db):
        class Accounts(db.Entity):
            _table_ = 'accounts'
            account_id = orm.PrimaryKey(int)
            name = orm.Optional(str)
            email = orm.Required(str)
            birthdate = orm.Optional(date)
            last_payment_date = orm.Optional(datetime)
            created_on = orm.Required(datetime, default=datetime.now())

        class Payments(db.Entity):
            _table_ = 'payments'
            payment_id = orm.PrimaryKey(str)
            account_id = orm.Required(int)
            payment_type = orm.Required(str)
            credit_card = orm.Optional(str)
            amount = orm.Required(float)
            created_on = orm.Required(datetime, default=datetime.now())



