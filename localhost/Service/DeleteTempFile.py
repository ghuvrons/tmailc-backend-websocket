from PySan.Base.Service import Service
import datetime, os

class DeleteTempFile(Service):
    def __init__(self):
        Service.__init__(self)
        self.queueFile = []
        self.rentan = datetime.timedelta(seconds = 10)
    def delete(self, f):
        self.queueFile.append((f, datetime.datetime.now(), ))
    def run(self):
        while not self.isClose.wait(5):
            while len(self.queueFile) > 0:
                try:
                    now = datetime.datetime.now()
                    f, deleted_at = self.queueFile[0]
                    if now - deleted_at > self.rentan:
                        os.unlink(f)
                        self.queueFile.pop(0)
                except:
                    pass