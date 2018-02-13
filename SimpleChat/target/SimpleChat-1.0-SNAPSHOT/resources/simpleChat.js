var websocket;

window.onload = function () {
    invokeConnection();
}

function invokeConnection() {
    websocket = new WebSocket(obtainUri());
    websocket.onerror = function (evt) {
        onError(evt)
    };
    websocket.onmessage = function (evt) {
        onMessage(evt)
    };
    return true;
}

function obtainUri() {
    return "ws://localhost:8877/ws";
}

function onError(evt) {
    writeToScreen('<span style="color: red;">ERROR:</span> ' + evt.data);
}

function onMessage(evt) {
    element = document.getElementById("mensajes");
    if (element.value.length === 0) {
        element.value = evt.data + "\n";
    } else {
        oldTexts = element.value.split("\n").slice(-19);
        element.value = oldTexts.join("\n") + evt.data;
        element.scrollTop = element.scrollHeight;
    }
    return;
}

function acceptValue(element) {
    websocket.send(element.value);
    element.value = "";
    return true;
}


