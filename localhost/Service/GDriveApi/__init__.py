from PySan.Base.Service import Service
import datetime, os, threading
from .RCloneDrive import RCloneDrive

class GDriveApi(Service):
    def __init__(self):
        Service.__init__(self)
        self.clients = []
        token = """{"access_token":"ya29.a0AfH6SMCFHmqK31TCAPrQfIag5PCu3lqSqMBwtG6IVxd7my7BLM5T7Q32w41uEWUzPFlkfozsHaVbkVHd-TWzJr39GNKckU-M-mSyQks0ntfbaxm482NJCY4cXIOuRNoX-YHj2I3K1fTmJ9nuw8DnvXsW1wNUR4XD6r6oInSkLOg","token_type":"Bearer","refresh_token":"1//0gVahorUwA8iECgYIARAAGBASNwF-L9Irsh0aw-f9XKcSNDb9aBq3aD-IVqwZbggfjXuEub62ZuvZtZ-Y2ZUjkJJRYEPNDDW3MqM","expiry":"2021-02-03T00:12:07.278985254Z"}"""
        self.rCloneDrive = RCloneDrive(token)
        self.isRun = threading.Event()
        self.status = {
            "transfering": False
        }
        self.folder_id = ""
        self.rCloneDrive.onSizeTf = self.onSizeTf
        self.rCloneDrive.onNumTf = self.onNumTf
        self.rCloneDrive.onError = self.onError

    def onSizeTf(self, transferred, maxSized, progress):
        print("size",  transferred, maxSized, progress)
        self.broadcast("size", {
            "transferred": transferred,
            "maxSized": maxSized,
            "progress": progress
        })

    def onNumTf(self, transferred, maxSized, progress):
        print("num",  transferred, maxSized, progress)
        self.broadcast("num", {
            "transferred": transferred,
            "maxSized": maxSized,
            "progress": progress
        })

    def onError(self, message):
        print("error", message)
        self.broadcast("error", message)

    def copy(self, folder_id):
        self.folder_id = folder_id
        self.emit("copy")

    def on_copy(self):
        print("tranferring")
        result = self.rCloneDrive.copy( 
                self.folder_id, 
                "/root/cpebr_server/tmailc-backend-websocket/localhost/Service/tes"
        )
        print("tranferring done")