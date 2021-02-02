from PySan.Base.Controller import Controller
from PySan.Database.MySQL import Query 
import datetime, traceback
from .PDFRetrieval.PDFData import PDFData
from .PDFRetrieval import PDFRetrieval
from PySan.ErrorHandler import HTTPError

class pdfData(Controller):
    def _init_(self):
        self.pdfRetrieval = PDFRetrieval(self.Databases['db2']['companies_data'])
        PDFData.mongo_collect = self.Databases['db2']['companies_data']['pdf_report']

    def getList(self, req):
        page = 1
        if req.data:
            page = int(req.data.getvalue("page"))
        data = PDFData.find(page = page)
        return {
            "count": data['count'],
            "data": [d.dict_data for d in data['data']]
        }
    
    def detail(self, req):
        _id = req.data['id']
        pdf = PDFData.find_one(_id)
        return pdf.dict_data if pdf else None

    def insert(self, req):
        ticker = req.data.getvalue("ticker")
        year = int(req.data.getvalue("year"))
        sic = int(req.data.getvalue("sic"))
        category = req.data.getvalue("category")
        ext = req.data["pdf"].filename.split(".")[-1]
        pdfPath = "/pdf/{}/{}_{}.{}".format(year, category, ticker, ext)
        self.saveFile(req.data["pdf"].file, base_path = ".", path="pdfPath")
        self.pdfRetrieval.uploadPDF(ticker, year, pdfPath, category, sic)
        return _id
    
    def update(self, req):
        _id = req.data.getvalue("id")
        pdf = PDFData.find_one(_id)
        if pdf:
            pdf = pdf.dict_data
            ticker = pdf['ticker']
            year = pdf['year']
            category = req.data.getvalue("category")
        else:
            raise HTTPError(404, 'not found')
        ext = req.data["pdf"].filename.split(".")[-1]
        pdfPath = "/pdf/{}/{}_{}.{}".format(year, category, ticker, ext)
        self.saveFile(req.data["pdf"].file, base_path = ".", path="pdfPath")
        self.pdfRetrieval.uploadPDF(ticker, year, pdfPath, category)
        return "ok"

    def saveFile(self, _f, base_path = ".", path = "/tmp.tmp"):
        b = _f.read(2048)
        _f_save = open(base_path+path, 'wb')
        while b:
            _f_save.write(b)
            b = _f.read(2048)
        _f_save.close()
        return