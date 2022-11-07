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

    def create_audit(self, audit):
        data_dict = dict(audit)
        self.db.audit.insert_one(data_dict)

    def list_audit(self):
        data = list(self.db.audit.find())
        data = parse_obj_as(list[AuditModel], data)
        return data

    def get_audit(self, _id):
        data = self.db.audit.find_one({"id": _id})
        data = parse_obj_as(AuditModel, data)
        return data


