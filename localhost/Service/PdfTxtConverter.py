from PySan.Base.Service import Service
import datetime, os, subprocess, traceback

class PdfTxtConverter(Service):
    def __init__(self):
        Service.__init__(self)
        self.queueFile = []
        self.rentan = datetime.timedelta(seconds = 10)
        self.timeout = None
        self.pdfRetrieval = self.Models['pdfRetrieval']()
        self.pdfRetrieval.log = self.r_log

    def r_log(self, msg):
        self.broadcast("pdf_txt_converter", msg)

    def stopConverting(self):
        self.pdfRetrieval.isConverterStop = True
        self.pdfRetrieval.log("Terminating....")
        return True

    def on_convert(self, data):
        self.Log.info("converting {}".format(data))
        category = data['category']
        years = data['years']
        try:
            self.pdfRetrieval.multiplePdfToTxt(category, years)
        except Exception:
            e = traceback.format_exc()
            self.r_log(e)