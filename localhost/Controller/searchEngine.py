from PySan.Base.Controller import Controller
from PySan.Database.MySQL import Query 
import datetime, traceback
from .PDFRetrieval import PDFRetrieval
from .PDFRetrieval import ExportExcel


class searchEngine(Controller):
    def _init_(self):
        self.urlExcel = '/excel'
        self.pdfRetrieval = PDFRetrieval(self.Databases['db2']['companies_data'])
        ExportExcel.directory = self.appPath+'/Public'+self.urlExcel
    
    def listSIC(self):
        return {
            "status": 200,
            "data": self.pdfRetrieval.sic_code
        }

    def retrieve(self, requestHeandler):
        def progress(p):
            requestHeandler.ws.sendRespond("retrieve_loading", 200, p)
        data = self.pdfRetrieval.retrieve(requestHeandler.data, callback=progress)
        l_data = len(data)
        i = 0
        while i < l_data:
            requestHeandler.ws.sendRespond("retrieve_data_part", 200, data[i:(i+10)])
            i += 10
        return True

    def exportExcel(self, requestHeandler):
        def progress(p):
            requestHeandler.ws.sendRespond("retrieve_loading", 200, p)
        data = self.pdfRetrieval.exportExcel(requestHeandler.data, callback=progress)
        return self.urlExcel+'/'+data

    def excelFile(self, requestHeandler):
        self.Services['deleteTempFile'].delete(ExportExcel.directory + requestHeandler.data)
