
// If you're not here from bonk.io, don't worry about this. I'm not running any JS on my website.

let frame = document.getElementById("maingameframe").contentWindow.document

function get_index(num_of_maps)
{
	let i

	// User error
	if (num_of_maps < 2)
	{
		alert("You need to have a map selection loaded. Exit and click MAP.")
		return i
	}

	// Different index determination operations depending on what's selected
	switch(type.value)
	{
		case "no_duplicates":
			i = Math.floor(Math.random() * num_of_maps)
			while (i == prev_index)
			{
				i = Math.floor(Math.random() * num_of_maps)
			}

			break

		case "random":
			i = Math.floor(Math.random() * num_of_maps)
			break

		case "order":
			i = prev_index + 1
			break
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

		let corrected_index = i % num_of_maps
		frame.getElementById("maploadwindowmapscontainer").children[corrected_index].click()
		frame.getElementById("newbonklobby_startbutton").click()

		frame.getElementById("ingamewinner").style["visibility"] = "hidden"
	}
}

// Init interval variable so it's global
let qp_interval

// HTML UI ==================================================

let menu = document.getElementById("descriptioninner")
while (menu.children.length > 0)
{
	menu.children[0].remove()
}

let h1 = document.createElement("h1")
h1.innerHTML = "Bootleg Quick Play v2.3.6"
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

let p
p = document.createElement("p")
p.innerHTML = "Pick a rotation type:"
menu.appendChild(p)

let type = document.createElement("select")
let option

option = document.createElement("option")
option.value = "no_duplicates"
option.innerHTML = "Random, but no duplicates"
option.selected = true
type.appendChild(option)

option = document.createElement("option")
option.value = "random"
option.innerHTML = "Random, with occasional duplicates"
type.appendChild(option)

option = document.createElement("option")
option.value = "order"
option.innerHTML = "In order (not random)"
type.appendChild(option)

menu.appendChild(type)

menu.appendChild(document.createElement("hr"))

p = document.createElement("p")
p.innerHTML = "I did not write the original script, but I have made improvements (in my opinion)."
menu.appendChild(p)

let ul
let li

ul = document.createElement("ul")
li = document.createElement("li")
li.innerHTML = "I added a UI for selecting a rotation mode"
ul.appendChild(li)
li = document.createElement("li")
li.innerHTML = "I implemented 'Random, but no duplicates' mode and 'In order (not random)' mode"
ul.appendChild(li)
li = document.createElement("li")
li.innerHTML = "I added a UI for start/stop of the script"
ul.appendChild(li)
li = document.createElement("li")
li.innerHTML = "I cleaned up the codebase"
ul.appendChild(li)
li = document.createElement("li")
li.innerHTML = "I fixed a bug that rendered the script unusable (which was present in the original script, not caused by me)"
ul.appendChild(li)
menu.appendChild(ul)

menu.appendChild(document.createElement("hr"))

p = document.createElement("p")
p.innerHTML = "Credit"
menu.appendChild(p)

ul = document.createElement("ul")
li = document.createElement("li")
li.innerHTML = "msk (me) - the changes described above"
ul.appendChild(li)
li = document.createElement("li")
li.innerHTML = "MaeIstrom - giving me the original script"
ul.appendChild(li)
li = document.createElement("li")
li.innerHTML = "GudStrat - implementing 'Random, with occasional duplicates' mode"
ul.appendChild(li)
li = document.createElement("li")
li.innerHTML = "Original creator (I don't know their name) - creating the original script"
ul.appendChild(li)
menu.appendChild(ul)
