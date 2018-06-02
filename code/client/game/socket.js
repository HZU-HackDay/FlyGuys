var ws;
function init() {
    ws = new WebSocket("ws://127.0.0.1:9001/");
    ws.onopen = function() {
        console.log("=> onopen");
    };

    ws.onmessage = function(e) {
        output("=> onmessage: " + e.data);
        data = JSON.parse(e.data);
        var z = $.Event('keydown');

        if (data["type"] == "server") {
            switch (data["data"]) {
                case "left": z.keyCode = 37;
                case "right": z.keyCode = 39;
                default: z.keyCode = 38;
            }
            $(window).trigger(z);
            console.log("onmessage", z);
        }
    };

    ws.onclose = function() {
        output("=> onclose");
    };
    ws.onerror = function(e) {
        output("=> onerror");
        console.log(e);
    };
}

function onSubmit() {
    var input = document.getElementById("input");
    ws.send(input.value);
    output("=> send: " + input.value);
    input.value = "";
    input.focus();
}

function onCloseClick() {
    ws.close();
}

function output(str) {
  console.log(str);
  /*
  var log = document.getElementById("log");
  var escaped = str.replace(/&/, "&amp;").replace(/</, "&lt;").
    replace(/>/, "&gt;").replace(/"/, "&quot;"); // "
  log.innerHTML = escaped + "<br>" + log.innerHTML;
  */
}

init();