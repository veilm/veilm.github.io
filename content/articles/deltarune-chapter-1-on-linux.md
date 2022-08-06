---
title: "Deltarune Chapter 1 on Linux"
date: 2021-09-17T10:53:42-04:00
---

With the release of Deltarune Chapter 2 today, I thought I would share how I was
able to get Chapter 1 working on Linux. I will assume you're running Arch.

#### 1. Download the .exe
This would be from [Deltarune's website](https://deltarune.com/).

#### 2. Install Wine and libstrangle
```sh
su -c "pacman -S wine"
git clone https://aur.archlinux.org/libstrangle-git.git
cd libstrangle-git
makepkg -sirc
```

#### 3. Install Deltarune as if you were on Windows using Wine
```sh
wine SURVEY_PROGRAM_WINDOWS_ENGLISH.exe
```
For me, it stopped writing new text after a couple of minutes, at which point I
killed it with ^C. I guess it finishes installing but doesn't quit Wine?

#### 4. Run Deltarune using strangle:
```sh
cd "$HOME/.wine/drive_c/Program Files (x86)/SURVEY_PROGRAM"
strangle 30 wine DELTARUNE.exe
```

That's it, it should work now. Using Wine on its own without libstrangle won't
work (extreme framerate issues). Feel free to try it if you don't believe me.

### Update: 2021-09-17-20-50

A few hours after I posted the article, and with the reveal of Chapter 2,
Deltarune (the "demo", at least) was released on Steam. So, you can now simply
play it through Proton instead of installing Wine and everything.

I'll leave this article up in case someone wants to avoid Steam. From my limited
testing, the itch.io download for Chapters 1&2 also worked fine under Wine.
