from PySan.Base.Controller import Controller
class site(Controller):
    def index(self, req, session):
        return "Hello World"
    def copy(self, req, session):
        self.Services["gDriveApi"].join_in(req)
        self.Services["gDriveApi"].copy()

    def tes(self, req, session):
        self.Services["tes"].addStreamer(req)
    def boom(self):
        self.Services["tes"].emit("boom", None)