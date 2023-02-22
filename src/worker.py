import asyncio

from celery import Celery

from src.core.ner import NLP
from src.db.db_requests import DBCommands
from src.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


async def create_report(db_connection, name, user_id, bytes_doc, task_id):
    await db_connection.create_report(doc=bytes_doc, user_id=user_id, name=name, id_=task_id)


@celery.task(name="create_task", bind=True)
def process_text(self, name, user_id, text_data):
    conn = DBCommands()
    doc = NLP(text_data)
    bytes_doc = doc.to_bytes()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_report(conn, name, user_id, bytes_doc, self.request.id))
    return True
