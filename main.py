from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
import logging

from models.auditmodel import AuditModel
from storage.storage import Storage

load_dotenv()
app = FastAPI()
router = InferringRouter()


@cbv(router)
class AuditController:
    def __init__(self):
        self.storage = Storage()

    @router.get("/")
    def read_root(self):
        return {"Hello": "World"}


    @router.get("/audit/{audit_id}")
    def read_audit(self,audit_id: int):
        try:
            return self.storage.get_audit(audit_id)
        except Exception as err:
            logging.error(err)
            return None


    @router.get("/audit/")
    def read_all_audit(self):
        return self.storage.list_audit()


    @router.post("/audit/")
    def create_audit(self, audit: AuditModel):
        self.storage.create_audit(audit)
        return audit

app.include_router(router)