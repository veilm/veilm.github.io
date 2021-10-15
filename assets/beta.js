
// If you're not here from bonk.io, don't worry about this. I'm not running any JS on my website.

let frame = document.getElementById("maingameframe").contentWindow.document

function map(e)
{
    frame.getElementById("maploadwindowmapscontainer").children[e].click()
    frame.getElementById("newbonklobby_startbutton").click()
}

function timeout()
{
        if (frame.getElementById("ingamewinner").style["visibility"] == "inherit")
        {
            let i = Math.floor(Math.random()*frame.getElementById("maploadwindowmapscontainer").children.length)
            map(i % (frame.getElementById("maploadwindowmapscontainer").children.length))
            frame.getElementById("ingamewinner").style["visibility"] = "hidden"
        }
}

// Set up GUI
let menu = document.getElementById("descriptioninner")
while (menu.children.length > 0)
{
	menu.children[0].remove()
}

let p = document.createElement("p")
p.innerHTML = "Bootleg Quickplay v2.2"
menu.appendChild(p)

let start = document.createElement("input")
start.type = "button"
start.value = "Start"
start.onclick = function()
{
	clearInterval(qp_interval)
	qp_interval = setInterval(timeout, 100)
}
menu.appendChild(start)

let stop = document.createElement("stop")
stop.type = "button"
stop.value = "Stop"
stop.onclick = function()
{
	clearInterval(qp_interval)
}
menu.appendChild(stop)

// Init interval variable so it's global
let qp_interval
