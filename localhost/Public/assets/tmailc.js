"use strict";
class TMAILC {
  _events = {
    "onRetrieveLoading": function (n){},
    "onRetrieveFinish": function (data){}
  };
  constructor(base_url = null) {
    this.base_url = base_url;
    this.configRouter = {};
    this.pySan = new PySan(this.base_url);
    this.result = [];
    var _this = this;
    this.pySan.on("retrieve_loading", function (data) {
      _this._events.onRetrieveLoading(data);
    });
    this.pySan.on("retrieve_words", function (data) {
      _this._events.onRetrieveFinish(_this.result);
    });
    this.pySan.on("retrieve_data_part", function (data) {
      console.log(data);
      _this.result.push(data)
    });
  };
  retrievehWords(data){
    this.result = []
    this.pySan.emit("retrieve_words", data);
  }
  on(event, callback){
    this._events[event] = callback;
  }
  close(){
    this.result = []
    this.pySan.close()
  }
}