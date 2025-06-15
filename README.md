# veilm.github.io
I'm not sure what kind of README is expected for something like this.

## crss
crss is a script I made for updating the RSS feed. Using a Hugo template seems
like it would be annoying, since I have pages outside of Hugo that I would want
to be included. Also, I wanted to practice using Kakoune in filter mode.

### Usage: ``crss [hugo md file]``
This will open a temporary file with some text for each RSS value. Edit it to
match your intended content of the form
```
<Update Title>
<Update URL>
<Update Date>
<Update Description>
```
, save the file, and close the editor to give control back to the script. If you
provided a Hugo markdown file, its filepath (./content/articles/foo-bar.md -->
base_url/articles/foo-bar/) and front matter will be used as default values.

Once you're done, the RSS item will be added below the ``<!-- crss-insert -->``
line in your rss xml file. If it's not present, crss will exit with an error.

## Credit
Credit to oxalorg for making [sakura.css](https://github.com/oxalorg/sakura),
which I use extensively here.

The SVG icons are from
[SuperTinyIcons](https://github.com/edent/SuperTinyIcons).
