
class JSONHandler
{

constructor(address="/api")
{
	this.address = address;
}

post(data=null)
{
    return fetch(this.address, {
          method: 'post',
          headers: {
              "Content-Type": "application/json",
              'Accept':'application/json'
          },
          body: JSON.stringify(data),
    });
}


}


class WebSocketHandler
{

constructor(address="ws://localhost:5000/ws")
{
	this.address = address;
    this.uuid=null;
	this.ws = new WebSocket("ws://localhost:5000/chat/ws");

    this.ws.addEventListener("close", (event) => {
      this.websocket_close(event);
    });

    this.ws.addEventListener("open", (event) => {
        this.sendEvent("open");
    });

    this.ws.addEventListener("message",  (event) => {
      this.listener_message(event);
    });

}

listener_message(event)
{
    try {
        var data = JSON.parse(event.data);
        if( data.event && data.event == "new_uuid")
        {
            this.uuid=data.uuid;
            console.log("uuid: "+ data.uuid);
        }else if(data.event){
            this.websocket_message(data);
        }
    } catch (error) {
        alert("Message from server "+ event.data);
    }
}

websocket_message(data)
{

}

sendEvent(event_name,data=null)
{
    this.ws.send(JSON.stringify({"event":event_name,"data":data}));
}
websocket_close(event){
    console.log("WebSocket Closed");
}

}
