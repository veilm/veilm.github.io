
// If you're not here from bonk.io, don't worry about this. I'm not running any JS on my website.

let frame = document.getElementById("maingameframe").contentWindow.document

function map(e)
{
    frame.getElementById("maploadwindowmapscontainer").children[e].click()
    frame.getElementById("newbonklobby_startbutton").click()
}

function get_index(num_of_maps)
{
    // Don't let i be the same value twice in a row
    let i = Math.floor(Math.random() * num_of_maps)
    while (i == prev_index)
    {
        i = Math.floor(Math.random() * num_of_maps)
    }

    return i
}

let prev_index
function timeout()
{
        if (frame.getElementById("ingamewinner").style["visibility"] == "inherit")
        {
			let num_of_maps = frame.getElementById("maploadwindowmapscontainer").children.length

	        let i = get_index(num_of_maps)
	        prev_index = i

            map(i % num_of_maps)
            frame.getElementById("ingamewinner").style["visibility"] = "hidden"
        }
}

// Set up GUI
let menu = document.getElementById("descriptioninner")
while (menu.children.length > 0)
{
	menu.children[0].remove()
}

let h1 = document.createElement("h1")
h1.innerHTML = "Bootleg Quick Play v2.3"
menu.appendChild(h1)

let start = document.createElement("input")
start.type = "button"
start.value = "Start"
start.style.color = "white"
start.style.backgroundColor = "black"
start.style.fontSize = "20px"
start.onclick = function()
{
	clearInterval(qp_interval)
	qp_interval = setInterval(timeout, 100)
}
menu.appendChild(start)

let stop = document.createElement("input")
stop.type = "button"
stop.value = "Stop"
stop.style.color = "white"
stop.style.backgroundColor = "black"
stop.style.fontSize = "20px"
stop.onclick = function()
{
	clearInterval(qp_interval)
}
menu.appendChild(stop)

let p = document.createElement("p")
p.innerHTML = "I did not write the original script, but I have made improvements (in my opinion)."
menu.appendChild(p)

let ul = document.createElement("ul")
let li
li = document.createElement("li")
li.innerHTML = "I added a UI"
ul.appendChild(li)
li = document.createElement("li")
li.innerHTML = "I cleaned up the codebase"
ul.appendChild(li)
li = document.createElement("li")
li.innerHTML = "I fixed a bug that rendered the script unusable"
ul.appendChild(li)
menu.appendChild(ul)

// Init interval variable so it's global
let qp_interval
