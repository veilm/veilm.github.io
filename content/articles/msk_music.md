---
title: "msk_music"
date: 2021-07-23T22:12:54-04:00
---

I have decided to put this to use for sharing scripts I write, in hopes that one
or two of them could be of use to somebody.

[msk_music GitHub Gist](https://gist.github.com/michaelskyba/2e04107265d4255671bb597581afd76a)

``msk_music`` is a simple and featureless way of listening to music. It uses the
equivalent of "random" and "consume" modes on mpd (which it aims to replace).
For my use cases, which I believe are fairly standard, it does so successfully.

Instead of having a vast number of configuration options, additional features
can be implemented by changing the source code, which, due to being written in
shell, is completely transparent. For instance,
[this patch](https://gist.github.com/michaelskyba/697a06b1f53f3f8a14e94bd9ccf4de3e)
will have ``msk_music`` only run on .mp4 files.

``msk_music`` depends on mpv and a set of coreutils that support sed's "-i"
flag. ``msk_music`` is around 20 LOC, and was written in about 10 minutes.

***

### 2022-08-06: Rambling

>So, it uses local files?

Yes. You could modify it to create the track list from a user-generated track
list that contains web URLs, but that would be weird.

Playing music locally instead of through a streaming service offers a few
advantages:
- You can listen to your music even when you're offline.
- You can listen to music without the use of online streaming platforms, which
often have required payments, advertisements, bloated, slow, resource-hogging
user interfaces, etc.
- You can listen to the same music in any client that you like, of which there
are many on Linux.
- Since it's your filesystem, you can perform your own automation for
organization, renaming, etc.

I don't care how you listen to your music or if you listen to music at all; I'm
just explaining my motivation for using this system instead of e.g. Spotify.

>But how am I supposed to get the local audio?

This is only a problem if you lack basic digital literacy, in which case you
definitely wouldn't be interested in some random shell script on the internet.
That said, I usually save any new music I like to a YouTube playlist and then
download the playlist with [yt-dlp](https://github.com/yt-dlp/yt-dlp) once it
starts filling up. I don't understand why people bother with torrenting when
this seems so much easier.
