---
title: "Becoming a PulseAudio user"
date: 2022-08-24T10:44:45-04:00
---

A few days ago, I decided to bite the bullet and install PulseAudio. I did so
through PipeWire, though, so by "PulseAudio", I'm going to be referring to the
``pipewire-pulse`` system.

## Background
While most Linux users either have it shipped with their distribution by
default, have it as a dependency of other software they rely on, or install it
themselves once they boot into their system for the first time, I was part of
the minority who decided to say "no".

Was it because ALSA is more convenient to work with? Because PulseAudio was
incompatible with the software I was intending to use? Because PulseAudio had
terrible performance and would slow down my computer?

No, it was never anything like that. Instead, I was willing to sacrifice
usability just so I could tell myself that I wasn't using PulseAudio. At that
time, this made a lot of sense, but as I grew older and started to have more
important things to spend time on, I gradually came to understand that making
myself less productive as a joke was not a great idea.

(Of course, I'm talking about general desktop use. In other cases, such as an
embedded system with only 100 MB of RAM, a server, etc. it usually wouldn't make
sense to have another layer on top of ALSA.)

## systemd

You might be quick to apply this logic to other topics, such as the systemd
debate:

>N-nooo! systemd is more convenient than other init systems! You're just
being a hipster for no reason!

However, in the case of systemd specifically,
from my experience with OpenRC on Gentoo, and from what I have heard about some
other init systems (e.g.
[s6](https://dudemanguy.github.io/blog/posts/2019-12-19-s6-love/s6-love.html)),
they're probably more usable rather than less usable. As software grows in
complexity, it generally becomes harder to extend.

With that reasoning, I'm becoming more and more inclined to try Artix again,
this time putting more thought into my usage. Even if systemd ends up being more
convenient, I'm sure it'd only be a slight difference. My point with ALSA was
that PulseAudio is significantly more convenient, my reasoning for which I'll
explain in the next section.

## Post-transition
These are the two broad "benefits" that I feel I've received with PulseAudio.

### 1. General audio convenience

First, there are the conveniences that are pretty easy to get on ALSA, like
having multiple programs playing audio at once, not starting muted,
automatically muting the speaker when you plug in headphones, etc.

But after that come the more sophisticated features. For instance, PulseAudio
remembers the volume you saved for each output device. So, if I have the volume
turned up to 100 on my speakers and then plug in my headphones, my ears aren't
going to melt. With ALSA, this happened several times before the computer's
Pavlovian conditioning sufficiently ingrained the habit of checking the volume
before playing sound. Another example is that each program is given its own
volume configuration, unlike ALSA where you can pretty much only modify the
master volume.

I'm sure there are obscure ways to reach the same functionality with ALSA, but
again, I don't see any benefit to taking the time to research that.

### 2. No more pain in recording
Finally, PulseAudio is significantly nicer to work with in ffmpeg. If you've
never done any recording and have no intention of doing it, this point doesn't
become particularly relevant. However, because I like to occasionally create
(low effort, like everything I end up doing) YouTube videos, it's quite
important to me.

Some things don't change much. For example, consider the recording of microphone
input along with the desktop video. With ALSA, you could use something like
```sh
ffmpeg -y -f x11grab -r 30 -s 1366x768 -i :0.0 -f alsa -i default ~/screen.mp4
```
and with PulseAudio, you could use something like
```sh
ffmpeg -y -f x11grab -r 30 -s 1366x768 -i :0.0 -f pulse -i default ~/screen.mp4
```

(The options I'm showing are adjusted to my system.) Not much stress, right? But
then, consider another scenario: capturing the screen like before, but this time
taking the desktop audio instead of the microphone input.

On PulseAudio, you spend thirty seconds reading the documentation and settle on
```sh
ffmpeg -y -s 1366x768 -f x11grab -i :0.0 -f pulse -i <monitor id> ~/screen.mp4
```
Just in case the monitor's ID changes, I decided to grep for it each time with
```sh
num=$(pactl list short sources | grep monitor)
num=${num%%	*}
```

Pretty sensible. What about ALSA? Judging from the [ffmpeg wiki
article](https://trac.ffmpeg.org/wiki/Capture/ALSA), the standard way to do this
would be

```sh
ssu modprobe snd-aloop pcm_substreams=1
echo 'pcm.!default { type plug slave.pcm "hw:Loopback,0,0" }' > ~/.asoundrc
ffmpeg -loglevel quiet -s 1366x768 -f x11grab -i :0.0 -f alsa -i hw:Loopback,1,0 ~/screen.mp4
rm ~/.asoundrc
```

Why does the user have to do that? Besides the shock, this solution stops all
playback to your original output device. Getting it to go to both takes an even
more complex asoundrc configuration. Additionally, you're now stuck with an
extra file that doesn't follow the XDG base directory specification.

### Wayland
A bonus point is that if I ever switch to Wayland in the future, for which I
believe PipeWire is required for screen sharing, I will have already gained
familiarity with the system. However, this is an extremely minor detail
considering the amazingly low likelihood that I would ever decide to use Wayland
seriously. From my short but atrocious experience using it, my understanding of
the architecture, and [explanations from people particularly knowledgeable about
it](https://dudemanguy.github.io/blog/posts/2022-06-10-wayland-xorg/wayland-xorg.html),
it doesn't sound like Wayland will ever be remotely suitable to my use cases.

## Conclusion
A while ago, I would hear about constant lag, bugs, and crashes in PulseAudio,
but that seems to have gone away, especially with the development of PipeWire. I
haven't had a single problem with it. Overall, this has been a significant
upgrade in usability for all things sound-related. I don't need to have
nightmares about ALSA breaking during a critical event and me not being able to
fix it anymore.

Hopefully, my mind can start to throw away the digital self-harm mindset and
start to become more adapted to meaningful productivity. If I really need to
spend time making things hard for myself, I should just go fight Malenia without
using summons again.
