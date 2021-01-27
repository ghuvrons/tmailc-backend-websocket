from .Retriever import Retriever
from .ExportExcel import ExportExcel
import subprocess
import re
import os, sys
import json, csv
from time import sleep

class PDFRetrieval:
    def __init__(self, mongo_db):
        #self.mysql = mysql
        self.Database = mongo_db
        self.document_category = {
            #parameter : (basepath on file, on mongo)
            "Annual Report": ("C:\\Users\\Asus\\Projects\\CPEBR", "annual_report", ),
            "Sustainability Report": ("/var/database/Sustainability Report", "sustainability_report", ),
            "MDnA.Indonesia": ("/var/database/MDnA", "MDnA.id", ),
            "MDnA.English": ("/var/database/MDnA", "MDnA.en", )
        }
        self.Retriever = Retriever()
        self.log_path = "log.log"
        self.events = {
            "retrieving": self.onRetrieving,
            "exportExcel": self.onExportExcel
        }

        ## get sic code
        sic_code = open(__path__[0]+'/sic_code.json')
        self.sic_code = json.load(sic_code)
        sic_code.close()

    def log(self, errorLog, pdf_path, ticker='-', year='-', pdf_path_on_db='-', description=''):
        with open(self.log_path, 'a') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows([[errorLog, pdf_path, pdf_path_on_db,ticker,year,description]])
        writeFile.close()
    def on(self, event_name):
        def decorator(f):
            self.events[event_name] = f
            return self.events[event_name]
        return decorator
    def onRetrieving(self, progress):
        pass
    def onExportExcel(self, progress):
        pass
    def exportExcel(self, data, callback = None):
        date_result = self.retrieve(data, sentencesLimit = -1, isExportExcel = True, callback = callback)
        return ExportExcel.createXlsx(date_result)
    def retrieve(self, data, sentencesLimit = 3, isExportExcel = False, callback = None):
        ### query create conditions
        empty_data = {
            'companies': [],
            'year_start': None,
            'year_end': None,
            'sic': [],
            'category': "Annual Report",
        }
        empty_data.update(data)
        data = empty_data
        
        words = data['words']
        _where = {}
        if len(data['companies']) > 0:
            companies = []
            for c in data['companies']:
                companies.append(c.upper())
            _where["ticker"] = {"$in": data['companies']}
        
        result = []
        if data['year_start']:
            _where["year"] = {"$gte": data['year_start']}
        if data['year_end']:
            if 'year' in _where:
                _where["year"]["$lte"] = data['year_end']
            else:
                _where["year"] = {"$lte": data['year_end']}
        if len(data['sic']) > 0:
            _sic = []
            for s in data['sic']:
                try:
                    _sic.append(int(s))
                except ValueError:
                    pass
            if len(_sic) > 0:
                _where["sic"] = { "$in": _sic}

        category = data['category']
        _where["path."+self.document_category[category][1]] = {"$exists": True}
        ### query get
        pdf = self.Database['pdf_report'].aggregate([
            {"$match":_where},
            {"$lookup":{
                "from":"companies_profile",
                "localField": "ticker",
                "foreignField": "_id",
                "as": "profile" }},
            {'$unwind': "$profile"}
        ])
        pdf = list(pdf)
        pdf_length = len(pdf)

        ### search word for each pdf
        i = 0
        progres_tmp = -1
        for p in pdf:
            i += 1
            if True:
                try:
                    progres_num = int(i*100/pdf_length)
                    if not progres_num == progres_tmp:
                        if isExportExcel:
                            if callback is None:
                                self.events['exportExcel'](progres_num)
                            else:
                                callback(progres_num)
                        else:
                            if callback is None:
                                self.events['retrieving'](progres_num)
                            else:
                                callback(progres_num)
                    progres_tmp = progres_num
                except:
                    break
            else:
                break
            txtPath = p["path"]
            pdfName = p["path"]
            for c_o in self.document_category[category][1].split("."):
                txtPath = txtPath[c_o]
                pdfName = pdfName[c_o]
            txtPath = txtPath["txt"]
            pdfPath = pdfName["pdf"] if "pdf" in pdfName else None
            pdfName = pdfPath.split('/')[-1] if pdfPath else None
            sens_tmp = []
            try:
                word_number, sens = self.getSentences(txtPath, words, sentencesLimit, True, category = category)
            except Exception as e:
                continue
            for sen in sens:
                sens_tmp.append(sen)
            isZero = False
            for w in words:
                if word_number[w.lower()] == 0:
                    isZero = True
            if isZero:
                continue
            num_of_words = [{"word": word, "total": word_number[word]} for word in word_number.keys()]
            r_tmp = {}
            r_tmp["id"] = p["_id"]
            r_tmp["ticker"] = p["ticker"]
            r_tmp["company_name"] = p["profile"]["name"]
            r_tmp["sic"] = p['sic'] if 'sic' in p else "-"
            r_tmp["pdf"] = pdfName
            r_tmp["year"] = p["year"]
            r_tmp["num_of_words"] = num_of_words
            r_tmp["sentences"] = sens_tmp
            r_tmp["pdfPath"] = pdfPath
            result.append(r_tmp)
        return result
    
    def onConverting(self, pdfPath):
        print("converting ", pdfPath)
    def pdfInfo(self, pdf):
        print(pdf)
        p1 = subprocess.Popen(['pdfinfo', pdf], stdout=subprocess.PIPE)
        output = p1.communicate()[0]
        info = {}
        for d in output.split("\n"):
            if not d.find(":") == -1:
                key, val = d.split(":", 1)
                while len(val) > 0:
                    if val[0] == " ":
                        val = val[1:]
                        continue
                    break
                info[key] = val
        return info
    def uploadPDF(self, pdfPath, ticker, year, txtDir = None, isForceReplace=False, category='Annual Report'):
        data = {}
        pdfFilename = pdfPath
        isExists = False
        isText = False
        if pdfPath.split(".")[-1] in ["txt", "TXT"]:
            isText = True
        if txtDir:
            txtFilename = txtDir + pdfPath.split("/")[-1] + ".txt"
        else:
            txtFilename = '/txt/'+str(year)+'/'+pdfPath.split("/")[-1]+ ".txt"
        if category[:4] == 'MD&A':
            lang = category.split('.')[-1]
            txtFilename = "/"+lang+txtFilename
        data["_id"] = ticker+str(year)
        data["path"] = {self.document_category[category][1]: {}}
        if not isText:
            data["path"][self.document_category[category][1]]["pdf"] = pdfFilename
        data["ticker"] = ticker
        data["year"] = year
        
        mypdf = self.Database['pdf_report'].find_one({'_id': data['_id']}, {"path."+self.document_category[category][1]: 1})
        
        if (mypdf 
          and 'path' in mypdf 
          and self.document_category[category][1] in mypdf['path'] 
          and 'path' in mypdf['path'][self.document_category[category][1]]):
            if isText:
                pass
            elif mypdf['path'][self.document_category[category][1]]['pdf'] == pdfPath:
                return
            elif isForceReplace:
                isExists = True
            else:
                self.log("double ticker", 
                    data["path"][self.document_category[category][1]]['pdf'], 
                    data["ticker"], 
                    data["year"], mypdf["path"][self.document_category[category][1]]['pdf'],
                    description=category
                )
                return
        elif mypdf:
            isExists = True
        
        # apt-get install poppler-utils
        
        self.onConverting(pdfPath.split("/")[-1])
        
        pdfjson = []
        if not isText:
            info = self.pdfInfo(self.document_category[category][0] + pdfFilename)
            if 'Pages' in info:
                for i in range(int(info['Pages'])):
                    p = str(i+1)
                    p1 = subprocess.Popen(['pdftotext', '-f', p, '-l', p, self.document_category[category][0] + pdfFilename, 'tmp'], stdout=subprocess.PIPE)
                    output = p1.communicate()[0]
                    sys.stdout.write('-')
                    sys.stdout.write(output)
                    sys.stdout.flush()
                    p1 = subprocess.Popen(['cat', 'tmp'], stdout=subprocess.PIPE)
                    output = p1.communicate()[0]
                    pdfjson.append(self.txtNormalisasi(output))
            else:
                self.log("cannot read pdf file", data["path"][self.document_category[category][1]]['pdf'], data["ticker"], data["year"], description=category)
        else:
            baseTextFile = open(self.document_category[category][0] + pdfFilename, "r") #make text file
            try:
                pdfjson = [unicode(baseTextFile.read(), "utf-8")]
            except:
                self.log("cannot read text file", pdfFilename, data["ticker"], data["year"], description=category)
            baseTextFile.close()
        txtDir_tmp = self.document_category[category][0]
        for part_of_path in txtFilename.split('/')[:-1]:
            if part_of_path == '': continue
            txtDir_tmp += '/'+part_of_path
            if not os.path.exists(txtDir_tmp):
                os.mkdir(txtDir_tmp)
        textFile = open(self.document_category[category][0] + txtFilename, "w") #make text file
        textFile.write(json.dumps(pdfjson)) #write text to text file
        textFile.close()
        data["path"][self.document_category[category][1]]['txt'] = txtFilename
        if isExists:
            newData = {}
            newData["path."+self.document_category[category][1]+".txt"] = txtFilename
            if not isText:
                newData["path."+self.document_category[category][1]+".pdf"] = pdfFilename
            self.Database['pdf_report'].update({"_id":data["_id"]},
                {"$set":newData}
            )
        else:
            path_obj = self.document_category[category][1].split(".")
            if len(path_obj) > 1:
                data["path"] = {}
                tmp_ob = data["path"]
                for p_o in path_obj:
                    tmp_ob[p_o] = {}
                    tmp_ob = tmp_ob[p_o]
                if not isText:                    
                    tmp_ob["pdf"] = pdfFilename
                tmp_ob["txt"] = txtFilename
            self.Database['pdf_report'].save(data)

    def txtNormalisasi(self, text):
        def repl(m):
            text = m.group(1)
            if text > 1:
                isNotStart = re.search(r'^[A-z0-9&][A-z0-9\s]', text)
                isEnd = re.search(r'[^A-z0-9,)]$', text)
                if isNotStart:
                    if isEnd:
                        text += "\n"
                    return " "+text
            return "\n"+text
        
        text = re.sub(r"\n(.*)(.*?)", repl, text)
        text = text.replace('\n ', '\n')
        text = text.replace('    ', ' ')
        text = text.replace('   ', ' ')
        text = text.replace('  ', ' ')
        return text
    
    def getWordNumber(self, textFilePath, word, category="Annual Report"):
        textFile = open(self.document_category[category][0] + textFilePath, "r")
        text = textFile.read()
        textFile.close()
        arrText = json.loads(text)
        text = ''
        for t in arrText:
            text += t+"\n"
        return len(self.Retriever.numWord(text, word))
        
    def getSentences(self, txtPath, word, limit = -1, isGetWordNum = False, category="Annual Report"):
        textFile = open(self.document_category[category][0] + txtPath, "r")
        arrText = json.loads(textFile.read())
        textFile.close()
        return self.Retriever.listSentence(arrText, word, limit, isGetWordNum)