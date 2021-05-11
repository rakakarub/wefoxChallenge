from pony.orm import db_session, core
from datetime import datetime
from requests import exceptions

from database_connector import DatabaseConnector
import kafka_consumer_service
import rest_client_service
import json

db_con = DatabaseConnector()
db_con.define_entities(db_con.db)
db = db_con.db
db.bind(db_con.db_params)
db.generate_mapping(create_tables=True)

REST_CLIENT_SERVICE = rest_client_service.RestClientService()

def process_payment(payment_data, type):
    try:
        if type == 'online':
            response = REST_CLIENT_SERVICE.check_payment(payment_data)
            if response == 200:
                save_payment_data(payment_data)
        elif type == 'offline':
            save_payment_data(payment_data)
        else:
            print('Incorrect payment type. Should be Offline or Online! : ' + str(type))
    except core.TransactionIntegrityError as e:
        REST_CLIENT_SERVICE.log_error(payment_data['payment_id'], 'database', str(e))
    except exceptions.HTTPError as httpError:
        REST_CLIENT_SERVICE.log_error(payment_data['payment_id'], 'network', str(httpError))
    except Exception as exc:
        REST_CLIENT_SERVICE.log_error(payment_data['payment_id'], 'other', str(exc))



@db_session
def save_payment_data(payment_data):

    db.Payments(
        payment_id=payment_data['payment_id'],
        account_id=payment_data['account_id'],
        payment_type=payment_data['payment_type'],
        credit_card=payment_data['credit_card'],
        amount=payment_data['amount']
    )
    db.Accounts[payment_data['account_id']].last_payment_date = datetime.now()

consumer = kafka_consumer_service.KafkaConsumerService().consumer
consumer.subscribe(['online', 'offline'])

while True:
    msg_pack = consumer.poll(timeout_ms=500)

    for tp, messages in msg_pack.items():
        for message in messages:
            if message is None:
                continue
            value = message.value
            topic = message.topic
            data = json.loads(value)
            process_payment(data, topic)