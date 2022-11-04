from datetime import datetime

from models.auditmodel import AuditModel
from models.settings import MongoSettings
from pymongo import MongoClient
from pydantic import parse_obj_as


class Storage:
    def __init__(self):
        settings = MongoSettings()
        client = MongoClient(settings.mongodb_uri)
        self.db = client["audit-trail"]

    def _create_audit(self):
        data = AuditModel(id=2, date_created=datetime.utcnow(), content="first audit")
        data_dict = dict(data)
        self.db.audit.insert_one(data_dict)
        return data

    def _list_audit(self):
        data = list(self.db.audit.find())
        data = parse_obj_as(list[AuditModel], data)
        return data

    def _get_audit(self, _id):
        data = self.db.audit.find_one({"id": _id})
        data = parse_obj_as(AuditModel, data)
        return data


