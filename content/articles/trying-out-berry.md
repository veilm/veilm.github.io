---
title: "Trying Out berry"
date: 2021-08-15T10:38:12-04:00
---

#### Introduction

Recently, I found out about [berry](https://github.com/JLErvin/berry), which
describes itself as "[a] healthy, byte-sized window manager". As of the time I'm
writing this, I have used berry for around one day. In this post, I would like
to share my first impressions.

#### Philosophy

The main thing that drew me to berry in the first place was its philosophy.
[dwm](https://dwm.suckless.org), which I was using before trying berry, does not
follow the UNIX philosophy as well as I would like. In particular, dwm ships
with a statusbar and a hotkey daemon (the latter is not a precise description,
but I'm not sure what would be a better name; if you use dwm, you know what I'm
referring to). Neither of these are parts of berry. Additionally, berry has no
built-in tiling. Instead, you can use berryc to create your own layout.

#### Statusbar

If berry doesn't come with its own statusbar, which one did I choose? On dwm, my
usage of its statusbar consisted of a cron job, running ``xsetroot -name``
calls. This was enough for me. I didn't need (and still don't need) fancy
modules or anything like that.

With this in mind, I went with the statusbar that berry's website recomended:
[lemonbar](https://github.com/LemonBoy/bar), which I am quite satisfied with.
Lemonbar has all of the features I would want in a statusbar without going too
far over.

The main annoyance is that, from what I understand, it is incompatible with
fontconfig and TTF fonts. After realizing this, I installed
[lemonbar-xft](https://gitlab.com/protesilaos/lemonbar-xft), a fork with fonts
working the way I would expect.

Another thing that caught me a bit off guard was the usage. I assumed you would
run ``bard`` or something similar and then call xsetroot as I was used to.
Instead, lemonbar uses standard input. For example, you could run ``echo test |
lemonbar -p`` to set the bar to the word "test". Here's what I came up with for
replicating my xsetroot workflow:

```sh
# Init
rm -f $XDG_DATA_HOME/statusbar
touch $XDG_DATA_HOME/statusbar
tail -f $XDG_DATA_HOME/statusbar | lemonbar -g x25+0+0 -f "Noto Sans JP Medium" -p &
```

Then, inside cron, my battery script runs
``echo "%{c}$(date)%{c}" >> $XDG_DATA_HOME/statusbar``.

This isn't literally how it works, because I don't just want the date in
BusyBox's default format, but you get the idea. The ``%{c}``s are used to center
the text, which I prefer to dwm's bar, where the placement is the right side of
the bar. (Yes, I know that there's probably a way to change that, but it's more
annoying than searching "center" in ``man lemonbar``, especially since dwm's bar
additionally shows the title of the window and draws workspaces, neither of
which I require.)

Now that I think about it, it's probably easier to simply use ``killall lemonbar
; echo "%{c}$(date)%{c}" | lemonbar -p``. I might give that a go later; it will
likely perform better over what I just described, the use of a "statusbar" file.

#### berryc

Another significant "change" a dwm user would experience is the new reliance on
berryc, which is berry's client.

First, berryc has "settings", which I set in berry's autostart file. I copied
the default autostart (from the "examples" directory), my main change being that
I removed all borders/window decorations.

Second, and more importantly, berryc gives you control over the management of
windows. Instead of setting WM-related bindings in a config.h file, you need
some kind of hotkey daemon that can map keys to berryc commands. I chose to use
[sxhkd](https://github.com/baskerville/sxhkd), which I would say is one of my
favourite projects of all time. sxhkd is such a pleasure to use that I even
ported my bindings to [fsignal](https://dwm.suckless.org/patches/fsignal/) when
I was on dwm. As an example,
[here](https://gist.github.com/michaelskyba/94d2ba318750cc5e5ab5b76d4ffadc6f) is
my current configuration for berry. I have a separate, WM-agnostic configuration
that includes everything else (e.g. launching my terminal, running dmenu
scripts).

Now, seeing this simple config file, combined with the knowledge that berry has
no built-in tiling, you may be wondering whether managing windows is a huge pain
(compared to dwm). My personal answer is no. So far, this basic setup of
Super+(h|l|Space) for tiling windows is enough, and I've yet to feel a sudden
urge to switch back to dwm.

You should note that I was not a heavy user of "complicated" tiling on dwm. I
mostly had a few windows in master-stack mode, occasionally popping into monocle
mode. My workflow with berry feels just as convenient. If, however, you are
frequently using something fancy
([this](https://dwm.suckless.org/patches/fibonacci/), for example), you will
need to write a few shell scripts to make berry act the way you like. This
should be totally possible, though. See their website if you're interested in
doing so.

#### Caveats

In this section, I will describe a few things that I'm unsatisfied with. I'm
pretty much nitpicking, though, so none of this should be taken very seriously.

First, neither resizing nor moving windows using (Super|Alt)+Mouse is working
for me. This should be taken with a mountain of salt, though, because I'm 99%
sure that it's my fault. When I first tried berry (with the example
configuration), it was working fine. I'll fiddle around with it later.

Second, I'm not a fan of [their website](https://berrywm.org).
Its design does not look simple, which, from what I can see, sends the opposite
message. Some examples of better-designed websites, in my opinion, are (the
current states of): my website, KISS Linux's website, and OpenBSD's website.

Even besides the design, some of the information on the website is inaccurate.
For instance, on their "Usage" page, they wrote ``window_*_relative`` instead of
``window_*_absolute``. See the man page if something mentioned on their website
isn't working the way you would expect.

Finally, judging from the GitHub issues, I can see that berry's philosophy is
not 100% aligned with mine. This is to be expected, of course; different people
have different opinions, but still. For an example, see [this
issue](https://github.com/JLErvin/berry/issues/127). In my eyes, this should be
left for the user to script, which would not be difficult at all. JLErvin
doesn't explicitly agree that it should be added, but you get what I mean.

#### Conclusion

In conclusion, berry is a great window manager that, in my opinion, follows the
UNIX philosophy better than dwm does. Unless something overwhelmingly negative
and completely unexpected comes up, it is unlikely that I will switch back to
dwm.

If you don't care about anything else I have said so far, my only advice would
be to try berry out for yourself. At *worst*, you'll lose ~20 minutes of your
time and garner newfound respect for your current window manager.
