class MyEncoder(JSONEncoder):
    def default(self, obj_pdf_data):
        return obj_pdf_data.dict_data

class PDFData:
    mongo_collect = None
    def __init__(self, _id, data = None):
        self._id = _id
        self.dict_data = data
    
    def update(self, newData):
        PDFData.mongo_collect.update({"_id": self._id},
            {"$set":newData}
        )
    
    def delete(Self):
        pass

    @staticmethod
    def find(**arg):
        _condition = PDFData.default_condition(arg)
        cur = PDFData.mongo_collect.find(_condition)
        paging = {
            'page' : None,
            'limit': 20
        }
        paging.update(arg)
        if paging['page'] is not None:
            _skip = (paging['page'] - 1)*limit
            cur.skip(_skip).limit(paging['limit'])
        result = [PDFData(d._id, _d) for d in cur]
        return result
    
    @staticmethod
    def default_condition(**arg):
        data = {
            'ticker': [],
            'year_start': None,
            'year_end': None,
            'sic': [],
            'path_tag': None,
        }
        data.update(arg)
        
        _condition = {}
        if len(data['ticker']) > 0:
            ticker = []
            for c in data['ticker']:
                ticker.append(c.upper())
            _condition["ticker"] = {"$in": data['ticker']}
        
        result = []
        if data['year_start']:
            _condition["year"] = {"$gte": data['year_start']}
        if data['year_end']:
            if 'year' in _condition:
                _condition["year"]["$lte"] = data['year_end']
            else:
                _condition["year"] = {"$lte": data['year_end']}
        if len(data['sic']) > 0:
            _sic = []
            for s in data['sic']:
                try:
                    _sic.append(int(s))
                except ValueError:
                    pass
            if len(_sic) > 0:
                _condition["sic"] = { "$in": _sic}

        if data['part_tag']:
            _condition["path."+data['path_tag']] = {"$exists": True}

        return _condition