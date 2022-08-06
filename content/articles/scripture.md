---
title: "Scripture"
date: 2021-09-22T10:59:07-04:00
---

This article is about
[scripture](https://github.com/michaelskyba/scripture), an SM-2 implementation
that I made. This will not be a rewrite of the README but instead notes on why I
made it, my workflow with it, etc.

## SM-2

SM-2 is an application of
[spaced repetition](https://en.wikipedia.org/wiki/Spaced_repetition). The idea
is to be able to retain information in your long-term memory while spending as
little total time as possible reviewing it. SM-2 is a popular algorithm due to
it proving to be effective.

SuperMemo has made many algorithms after SM-2, and I presume that they are even
more efficient. I don't think there are any non-SuperMemo uses of them, perhaps
because they're significantly more complicated to implement? Take a look at
[SuperMemo's wiki](https://supermemo.guru/wiki/SuperMemo_Guru) if you're
interested in reading about them, or other topics that they seem to have
available.

## Anki

Anki is easily the most popular SM-2 implementation, although the developers
slightly tweaked the algorithm. Anki is what I have used for a long time before,
and all in all, it's a quality piece of software. Anki is infinitely better than
not using spaced repetition and I have recommended it to many people (in real
life) in the past.

However, Anki has problems, ignorable in many other eyes, but not mine. To cut
to the chase, Anki ignores the UNIX philosophy. It has a Qt (I think) GUI, a
built-in extension manager, built-in synchronization, an SQL database, etc. None
of these would exist if Anki followed the UNIX philosophy.

Again, for 99% of people, what I just described is great, and I would not want
Anki to actually adopt the ideas I have, because it's obviously not their goal.

## Other CLI Flashcard Programs

After I decided that I wanted to stop using Anki, I kept my eye out for any
other implementations that I thought could be suitable for my use cases. The
closest I found was [vocage](https://github.com/proycon/vocage), but I didn't
end up using it seriously. Vocage does not use any SuperMemo algorithm, from
what I understand, so my retention rate would significantly decrease from what
it was on Anki.

It wasn't clear to me how to extend it with shell scripts.
[This issue](https://github.com/proycon/vocage/issues/7) might be relevant, but
it doesn't seem like it will be solved any time soon. I am not familiar with and
have no interest in Rust, the language vocage was written in, so there's no
possibility of me looking through the source code or contributing.

Around this time, I had the idea of making my own implementation of SM-2. I
found out that Wikipedia had a really nifty pseudocode description of it on
their SuperMemo article that I could base it on, which probably sparked the
thought.

## Scripture's Language

At the time, my "go-to" programming language was Python (yes), but wanting to
become more familiar with shell scripting, I decided to write it in Shell. In
hindsight, this was a great decision. Not only have I gained valuable experience
in Shell, but Python is also the wrong language for this kind of project. I
maybe could have used Go, which I currently have used for two small CLI
projects, but from writing those (with my very limited Go knowledge), I think Go
would have been more of a hassle.

I also decided to avoid bashisms, because I wanted greater portability, and also
because I wanted to remove bash from my computer. Shellcheck says that scripture
does not use any bashisms, which is great, but it definitely uses non-POSIX
flags on certain tools (``sed`` and ``date`` are what I can think of off the top
of my head). Currently, I'm not particularly interested in trying to remove the
usage of those flags, because that would be a lot of work.

## Scripture following the UNIX Philosophy

As it stands, I think scripture follows the UNIX philosophy well enough. The
SCRIPTURE_HOOK system, I feel, is very extensible. I have been able to implement
every "personal" feature that I wanted to through its use without polluting the
main scripture codebase.

The fact that scripture doesn't have a built-in deck editor is also a huge plus
in terms of extensibility. Something like creating a new card when you receive
an email is trivial to do with scripture but a huge pain with Anki, if that's
even possible there.

The main shortcoming is the fact that scripture is interactive. Instead of
running commands like ``scripture mark <card> <score>``, you only
call scripture once on your deck file and then provide input through scripture's
``read < /dev/tty`` calls.

From a convenience standpoint, this is totally fine: it works well and is not
annoying to type. However, I don't know of an easy way to send input into an
interactive program like scripture from a separate shell instance. This means
that something like creating a GUI on top of scripture is going to be more
difficult than it needs to be.

You can say that scripture wouldn't benefit from a GUI, which I would agree
with, but that's beside the point. Interactivity reduces opportunities. No
matter what those are, it's unideal.

One possible solution is to have the base scripture program take on the model of
``scripture <command>`` as I mentioned before. Then, the scripture repository
would also come with a default interactive wrapper that most people would use.
The few that want to create an alternative UI would ignore the provided wrapper
(which, again, is a separate script from the main "scripture" script). This is
similar to how sfeed works, with its optional ncurses wrapper.

If I was smart, I probably would have created this structure from the start.
Switching to it now would not be *too* significant of a pivot, considering that
scripture has only around 200 total lines of code, but it would still be
annoying nonetheless, especially since it doesn't provide any current benefit to
me. If I happen to need a custom UI in the future, or if someone else really
needs one, I can implement the more UNIX-y model, but for now, I'm going to
leave it the way it is.

This is also better than the SCRIPTURE_HOOK system because, despite it having
good, clear documentation (in my opinion), it's still something you have to
learn/read about before you can use it. Ideally, simply having shell scripting
knowledge should be enough.

#### 2022 Update
I have since made a new SRS program called
[tunnel](https://github.com/michaelskyba/tunnel) which uses this non-interactive
CLI system. It might warrant its own article later.

## Personal Extensions

##### Reviewing Cards in Random Order

I'm not sure what SM-2's official advice is, but I like reviewing cards in
random order. I do not want to impose this opinion on every scripture user, so
in my hook script, I simply run ``shuf -o <deck file>`` before the review
starts.

##### Images

Image support, of course, is not built into scripture by default. Fortunately,
it can be very easily implemented through SCRIPTURE_HOOK. See the README on an
example implementation. The example deck uses them for pictures of flags, which
is one of the ways I use them personally.

##### Easy-to-read Text via Imagemagick

One of the things I use scripture for is remembering hiragana (initially; once
it clicked once, normal reading is enough to keep it in memory, obviously).
However, having normal cards for it is troublesome in two ways.

First off, to be able to properly each character, I need to have a
larger-than-normal font size. So, I would have to increase the font size in my
terminal every time I have due reviews for my hiragana deck, which is annoying.

The second and bigger problem is that st, the terminal emulator I use, is having
issues with dual-width characters for me. I'm pretty sure this is some kind of
problem on my end, because [its homepage](https://st.suckless.org) lists "wide
characters" as a supported feature, and I remember it working on a different
distribution.

Anyway, to kill two birds with one stone, I created a script called
"msk_display" that uses Imagemagick to write text onto a generate imaged, then
launches sxiv on that temporary image.
([Here](https://gist.github.com/michaelskyba/700366b6649f4dc6fa6cba6c264d3da2)
is the actual script in case you're interested.) In my scripture hook, it will
display cards with a "jp:" prefix with msk_display.

##### Spelling Deck

Although I "consider" English my native language, there are still some spellings
that I occasionally get confused about. To remember those, I can use scripture,
but what's the right way to do it? I obviously can't have the front of the card
"How do you spell 'x'?" because that gives away the spelling right there and
then.

One way is to record yourself saying each word so that the front of the card
will be an audio file of you speaking and the back will be the correct spelling.
Here, you would need to use a front_show hook to launch mpv or something on your
chosen audio file. I don't like this solution because I think it requires too
much maintenance, and also because I will quickly get annoyed with hearing my
own voice.

Instead, I decided to use Text-to-Speech (TTS)! My scripture hook looks for
"speak:" and runs TTS software to pronounce it. To make sure I heard it
properly, I have it repeat the word three times, with ``sleep 1`` in between
repetitions.

Now, the question of the hour is, of course, "What TTS implementation did you
choose?" I went with [espeak-ng](https://github.com/espeak-ng/espeak-ng), which
I am somewhat satisfied with. The good part of espeak-ng is that its usage is
simple and convenient. You don't need to have a speech database or machine
learning software installed. You don't need to create text or audio files
(although I'm sure you can if you wanted to). You can simply run ``espeak-ng
"<word>"``, and it will play the sound right away.

That sounds good, but what's wrong, if I'm only "somewhat satisfied"? Well, the
speech doesn't sound natural. Inherently, that's not a particularly big deal,
but the issue is that it can make it hard to determine which word is being
spoken. Sometimes, I have to synthesize fake spellings (or an entire sentence)
to make it easier for me to guess what word I'm being tested on spelling.

From taking a glance at their GitHub repository, which I looked up so I knew
where to link to, it seems like there are quite a lot of options, so maybe I can
read the documentation later and tweak it to sound more natural to me. Still, if
you know of a more easily decipherable engine, let me know.

The last thing I want to note in regards to this spelling deck is a script I
made called
["spell_add"](https://gist.github.com/michaelskyba/a0dacf6f07bcf6b6d4f83015569bae01)
(a very creative name). This script makes it more convenient to add a new word
to the spelling deck. It's another example of something easy to do when your
deck files are in plaintext rather than a complicated format.

## File Organization

I like to keep a separate directory for each deck, which can contain any other
files that the deck might use (usually images):

```sh
~/decks $ pwd
/home/michael/decks
~/decks $ tree
.
|-- flags
|   |-- australia.png
|   |-- canada.png
|   `-- deck
|-- hook
|-- japanese-hiragana
|   `-- deck
`-- japanese-katakana
`-- deck

3 directories, 6 files
```

- I have a "decks" directory
- Each deck has its own directory inside "decks"
- I use hyphens as a convention for subcategories
- Each deck directory uses a file called "deck" as the deck
- My scripture hook is not in a deck directory, but instead the master "decks" directory

(This isn't 100% what I use, because I have more decks and my decks
directory isn't in $HOME, but it's close enough for demonstration purposes.)

Then, I have a script called
[msk_scripture](https://gist.github.com/michaelskyba/b4de15a3bf8c4be719c7a8191e67c446)
which saves me time ``cd``ing into directories and typing "scripture" over and
over. It just goes through each deck and runs scripture on it. Once a day, I
type "msk_scripture" into the terminal and complete any due reviews.

## Conclusion

That's the end of this article. Hopefully, if you read all of it, you have a
good idea of whether or not scripture will satisfy your needs. I don't think
this kind of information belongs in the README, but my website is a fine place
to put it.

I may make another article in a similar style but about
[budgetpass](https://github.com/michaelskyba/budgetpass).
