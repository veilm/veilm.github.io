---
title: "Changing your Locked Google Classroom Profile Picture"
date: 2022-09-23T19:01:41-04:00
---

### Note to Google
If you (a software engineer, tester, etc.) are reading this and thinking "Lol
thanks, now I'll just patch it", please, please, please send me an email
([michaelskyba@net-c.com](mailto:michaelskyba@net-c.com) or
[michaelskyba1411@gmail.com](mailto:michaelskyba1411@gmail.com)) notifying me
about it. If you do, I (in exchange; as thanks) promise to work hard to find
exploits in the future but report them to you immediately instead of abusing
them for personal use or posting them as a lazy attempt at publicity.

### Introduction
I don't know how things are in the rest of the world, but the school board my
high school is a part of has decided that choosing a profile picture is a bit
too much responsibility for students. So, through some kind of admin panel
provided by Google, I suppose, they disabled changing.

Of course, I had no interest in being dictated so harshly through a medium as
basic as web interfaces, so I spent a significant amount of effort trying my
best to break out, and eventually, I was successful. In this article, which is
probably the closest one on my website to being useful to somebody, I will
document my findings.

The big disclaimer is that for it to work, you have to currently have a profile
picture set. If you have the default first letter of your name, there's probably
nothing you can do to change that. This is targeted at people who are bored
with their old profile picture and want a new one.

Another disclaimer is that I have an unnecessarily verbose writing style. If
you're actually interested in changing your profile picture and are capable of
reading written instructions, this shouldn't be a problem, but if you aren't,
this article will probably not help you. I'm writing with the assumption that
the reader is capable of mentally connecting dots. (The abundance of images is
solely for diversity in medium and is generally not intended to act as a support
in comprehension.)

### Demonstration of the lock
By default, you should see something like this when opening up your Google
Account picture popup:

![Default picture UI](/9-1.webp)

However, when your administrator has locked the changes, you experience this
disappointment instead:

![Locked picture UI](/9-2.webp)

Clicking on your icon on the main Google Account page says this (which isn't
true!):

![Locked Google Accounts page](/9-3.webp)

The settings page on Google Classroom says "Change", sparking hope:

![Google Classroom settings](/9-4.webp)

But if you press it, you get the same no-change-UI popup I showed in the first
screenshot. Another dead end...

However, as you've probably noticed, the setbacks I've mentioned so far are
enforced on the client-side. What if you create your own UI and make a request
to the Google servers, saying that you want to change your profile picture? If
you're not at all familiar with web development, that will sound confusing and
abstract, so here's a practical example.

1. Open a private window so that your profile data is reset to the default of
being signed out.
2. Sign into a non-school Google account.
3. Open the profile picture changing screen.
4. Upload a profile picture, crop it, etc. but **do not** submit it.
5. In a new tab, sign out of your non-school account and sign into your blocked
school account.
6. Go back to the first tab and submit the profile picture switch.

The idea is that the first tab would tell the server, "Set P as the profile
picture for the user that is currently signed in." The server would assume
that this request would never take place if the user is on a blocked account
because the user shouldn't have a submit button on a blocked account. Because of
this (supposed) lapse in the judgement of the system designers, it would
complete the change. This will surely work, right?

Well, don't bother trying it, because this was my first idea, and it doesn't
work. Instead of setting the picture, it tells you that something went wrong and
that you should try again. Of course, trying again doesn't change anything, and
you're left with little hope at the sight of yet another dead end. 

This doesn't mean that it's impossible. You just have to be a bit more clever in
the way you approach the problem.

### Past profile pictures
First of all, there's a bit more than what meets the eye on the blocked profile
menu. If you press the kebab menu (three vertical dots), you will see the option
to view your past profile pictures:

![Past profile pictures option](/9-5.webp)

Clicking it takes you to some kind of album selection screen, where the only
option should be "Profile Photos", a collection of the profile photos you've set
in the past. If there are zero items in this list, you will not be able to
change your profile picture, as I mentioned in the introduction.

![Profile photos album selection](/9-6.webp)

If you enter the list, open an image, and press the kebab menu, you will see an
option to delete the photo:

![Delete picture option](/9-7.webp)

>Why should I care? I want to change my profile picture, not delete random past
ones.

Well, the important detail is this: deleting your active profile picture will
change it to a different item in your Profile photos list. The selection pattern
was inconsistent in my testing, so if you want a certain picture from your list,
delete every picture except for that one. Make sure to keep at least one
remaining at all times unless you want to (permanently) have no profile picture.

If all you want is to set one of the profile pictures that you truly did use in
the past, then you're done! Note that it takes some time for Google's servers to
refresh your picture, so be prepared to wait 2-16 hours or so once you've
isolated the picture. If you're unfamiliar with your browser's picture caching
system, it could take even longer.

However, there's a solid chance that this isn't enough to satisfy you; you want
to set a new profile picture, not an old one. What then? Well, if deleting
unneeded profile pictures is the way you modify your selected one, then all we
have to do is add a new picture to the list and delete all the old ones. But
is that possible? It certainly is.

### Adding pictures to your Profile photos list
(This procedure is slightly more complicated and will therefore require some
more attention/thinking from the reader.)

As you can tell by looking at the album screen, there's no "+" button or
anything for adding new photos:

![No plus button](/9-8.webp)

This means that we will have to get creative again.

First, visit the main Google Photos site on your blocked school account and
create an album:

![Creating an album](/9-9.webp)

In here, you _will_ be given the option to upload photos from your computer.
Upload a random photo to finish the process. Once you're done, you should see
your new album with your uploaded photo:

![Created an album](/9-10.webp)

In the album UI you find on Google Photos, you can upload photos just fine:

![You can upload photos](/9-11.webp)

So, the problem now is to figure out how to open the Profile photos album inside
Google Photos. First, consider the UI from before (when I talked about deleting
profile photos). You were looking at the photos in the album, but it definitely
wasn't inside Google Photos, so what kind of view was that? Well, compare the
URLs of both views.

**Note that from this point on, I will be including ``/u/1/``s in my URLs,
because my school account is of index ``1`` in the set of Google accounts that
are saved in my browser. If your school account is the primary Google account
on your browser, you won't see /u/n (where n is the index) in Google Classroom,
Drive, and Photos URLs, so disregard them in my examples.**

In the Google Photos view that you can access on your newly-created album,
you'll see (probably from your browser's search/URL bar) a URL that looks like
```
https://photos.google.com/u/1/album/xxxxxxxxxxxxxxxxxxx
```
where the ``x``s comprise the album ID (a string of mixed-case letters) of the
album you created. (If your school account is the primary account, you'd see
``...com/album...`` and not ``...com/u/n/album...``. This is the last time I
will mention it.)

And what about the old Profile photos view? The URL should look like
```
https://get.google.com/u/1/albumarchive/yyyyyyyyyyyyyyyyyyy/album/zzzzzzzzzzzzzzzzzzz
```
where the ``y``s comprise a number (an ID of your student account? I'm not sure)
and the ``z``s comprise... the album ID! If you've been paying attention, you
should be excited. If we have the ID, why don't we just modify the Google Photos
URL? Simply direct your browser to
```
https://photos.google.com/u/1/album/zzzzzzzzzzzzzzzzzzz
```
and you'll see that it works! You can view the Profile photos album from Google
Photos just fine!

![Profile photos in Google Photos](/9-12.webp)

If we can access the album from Google Photos, we can add new photos to the album!

![New photos in Profile photos](/9-13.webp)

And if we can add new photos to the Profile photos album, we can set the profile
picture to anything we want. You should now know everything needed to change
your profile picture. Keep in mind my note from earlier about the update delay.

### Conclusion
In conclusion, once you've figured out how the system works, using it in a new
way isn't all that difficult. However, it's entirely possible that Google
patches this in the future (which I'm 100% fine with **IF** they email me). So,
if you followed the steps I outlined but are encountering a real (i.e. not due
to an inability to understand written instructions) issue, send me an email at
[michaelskyba@net-c.com](mailto:michaelskyba@net-c.com) and I'll try to help you
out. If it's clear that Google patched it and that it's not a user error, I'll
update this article to say that nothing written here works anymore.

###### Examples of "not real" problems
- Wait, you just jumped to the conclusion? I don't know what to do after adding
the picture to the album...
- I (literally) went to
``https://photos.google.com/u/1/album/zzzzzzzzzzzzzzzzzzz`` and I'm getting a
weird 404 error. What's going on?

###### Examples of (hypothetical) "real" problems
- I've waited seven days after setting the profile picture and it _still_ hasn't
been updated in any Google service. What's going on? And yes, I have a different
picture, not the default placeholder, set currently.
- When I visit the Profile photos album in Google Photos, I don't see the upload
button that you have in your screenshot... Was the UI updated?

I hope this article was helpful. Please give me credit if you're sharing these
instructions outside of the medium of this article, especially if you go to the
same school as me.
