
// If you're not here from bonk.io, don't worry about this. I'm not running any JS on my website.

function get_index(num_of_maps) {
	let i

	// User error
	if (num_of_maps < 2) {
		alert("You need to have a map selection loaded. Exit and click MAP.")
		return i
	}

	// Different index determination operations depending on what's selected
	switch(type.value) {
		case "no_duplicates":
			i = Math.floor(Math.random() * num_of_maps)
			while (i == prev_index) {
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

function new_map() {
	let num_of_maps = frame.getElementById("maploadwindowmapscontainer").children.length

	let i = get_index(num_of_maps)
	prev_index = i

	let corrected_index = i % num_of_maps
	// console.log(`${prev_index}, ${i}, ${corrected_index}, ${type.value}, ${num_of_maps}`)
	frame.getElementById("maploadwindowmapscontainer").children[corrected_index].click()
	frame.getElementById("newbonklobby_startbutton").click()

	frame.getElementById("ingamewinner").style["visibility"] = "hidden"
}

function timeout() {
	if (frame.getElementById("ingamewinner").style["visibility"] == "inherit") new_map()
}

// Quick play variable declaration

let prev_index = 0
let qp_interval
let frame = document.getElementById("maingameframe").contentWindow.document
let qp_running = false

// HTML UI ==================================================

// Clear old screen
let menu = document.getElementById("descriptioninner")
while (menu.children.length > 0) {
	menu.children[0].remove()
}

// Function definitions
function create_p(text) {
	let p = document.createElement("p")
	p.innerHTML = text
	return p
}

function create_button(value, onclick) {
	let button = document.createElement("input")
	button.type = "button"
	button.value = value
	button.style.color = "white"
	button.style.backgroundColor = "black"
	button.style.fontSize = "20px"
	button.onclick = onclick
	return button
}

function create_ul(items) {
	let ul = document.createElement("ul")
	items.forEach(function(value, index) {
		let li = document.createElement("li")
		li.innerHTML = value
		ul.appendChild(li)
	})
	return ul
}

// Actual insertion
let h1 = document.createElement("h1")
h1.innerHTML = "Bootleg Quick Play v2.3.8"
menu.appendChild(h1)

// Start, Stop, and Skip buttons
menu.appendChild(create_button("Start", function() {
	clearInterval(qp_interval)
	qp_interval = setInterval(timeout, 100)
	qp_running = true
}))
menu.appendChild(create_button("Stop", function() {
	clearInterval(qp_interval)
	qp_running = false
}))
menu.appendChild(create_button("Skip", function() {
	if (qp_running) new_map()
	else alert("No quick play rotation running.")
}))

menu.appendChild(create_p("Pick a rotation type:"))

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

menu.appendChild(create_p("I did not write the original script, but I have made improvements (in my opinion)."))

menu.appendChild(create_ul([
	"I added a UI for skipping maps - e.g. you run into a Grapple parkour map which is impossible to complete in Arrows, the mode you're using",
	"I added a UI for selecting a rotation mode",
	"I implemented 'Random, but no duplicates' mode and 'In order (not random)' mode",
	"I added a UI for start/stop of the script",
	"I cleaned up the codebase",
	"I fixed a bug that rendered the script unusable (which was present in the original script, not caused by me)"
]))

menu.appendChild(document.createElement("hr"))

menu.appendChild(create_p("Credit"))

menu.appendChild(create_ul([
	"msk (me) - the changes described above",
	"MaeIstrom - giving me the original script",
	"GudStrat - implementing 'Random, with occasional duplicates' mode",
	"Original creator (I don't know their name) - creating the original script"
]))
