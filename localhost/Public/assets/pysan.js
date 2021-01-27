"use strict";
class PySan {
  _events = {};
  _emit_queue = [];
  constructor(base_url = null) {
    this.base_url = base_url;
    this.ws = null;
    this.isConnected = false;
    this.reconnecting = null;
    this.connect();
  }
  connect(){
    try{   
      console.info("connecting");
      this.ws = new WebSocket(this.base_url);
      let pySan = this;
      this.ws.addEventListener('open', function (event) {
        while (pySan._emit_queue.length > 0) {
          this.send(pySan._emit_queue.shift())
        }
        pySan.onConnected();
      });
      this.ws.addEventListener('close', function (event) {
        this.isConnected = false;
        pySan.connect();
      });

      // Listen for messages
      this.ws.addEventListener('message', function (event) {
        pySan.onEvent(event.data);
      });
      this.isConnected = true;
    } catch (err){
      console.error(err);
      setTimeout(this.connect(), 1000);
    }
  }
  onConnected(){}
  onEvent(msg){
    let _msg = JSON.parse(msg);
    if(_msg.status != 200){
      console.warn(_msg.status, _msg.data);
      return;
    }
    if(this._events[_msg.respond] != undefined){
      this._events[_msg.respond](_msg.data)
    }
  }
  on(event, _func){
    this._events[event] = _func
  }
  emit(event, data){
    if(this.isConnected)
      this.ws.send(JSON.stringify({
        request: event,
        data: data
      }))
    else
      this._emit_queue.push(JSON.stringify({
        request: event,
        data: data
      }))
  }
  close(){
    _events = {};
    _emit_queue = [];
    if(this.ws != null)
      this.ws.close();
  }
}