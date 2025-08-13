---
title: "Block a Site Using /etc/hosts"
date: 2021-04-20T18:47:20-04:00
---

Simply add ``0.0.0.0 mysite`` to your /etc/hosts file.

For example, ``0.0.0.0 example.com``. Here, example.com will basically be an
alias for "0.0.0.0", which acts as a dummy address.

Note that this isn't completely reliable. If it's not working, try adding a
second entry with "www." and also try restarting your browser (in case, for
example, you're seeing a cached page).

[Here](https://github.com/StevenBlack/hosts) is a list of sites that you may
want to block.
