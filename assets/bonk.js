
// If you're not here from bonk.io, don't worry about this. I'm not running any JS on my website.

let frame = document.getElementById("maingameframe").contentWindow.document

function map(e) {
    frame.getElementById("maploadwindowmapscontainer").children[e].click();
    frame.getElementById("newbonklobby_startbutton").click();
}

function timeout() {
    setInterval(() => {
        if (frame.getElementById("ingamewinner").style["visibility"] == "inherit") {
            let i = Math.floor(Math.random()*frame.getElementById("maploadwindowmapscontainer").children.length)
            map(i % (frame.getElementById("maploadwindowmapscontainer").children.length));
            frame.getElementById("ingamewinner").style["visibility"] = "hidden";
        }
    }, 100);
}

timeout();
