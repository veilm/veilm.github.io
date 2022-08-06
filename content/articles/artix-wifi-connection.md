---
title: "Get a Working Wi-Fi Connection in an Artix Installation"
date: 2021-04-20T21:43:53-04:00
---

While Arch and Gentoo have had internet working mostly out-of-the-box, Artix has
not. I thought it could be beneficial if I compiled a list of steps:

##### 1. Become root: ``su``
##### 2. Make an initial wpa_supplicant configuration
Create ``/etc/wpa_supplicant/wpa_supplicant.conf`` with the following lines:
```
ctrl_interface=/run/wpa_supplicant
update_config=1
```

##### 3. Make sure rfkill isn't active
```
rfkill unblock wifi
```

##### 4. Start wpa_supplicant
```
wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
```
My device name was 'wlan0', but you should edit the command if yours is different.

##### 5. Run wpa_cli
```
wpa_cli
scan
scan_results
add_network
set_network 0 ssid "<the name of your wifi network>"
set_network 0 psk "<the password of your wifi network>"
enable_network 0
save_config
quit
```

Of course, this could be significantly more complicated depending on what kind
of security your network is using.

##### 6. Start dhcpcd: ``dhcpcd``

You should be done. I've done two Artix installs and both of them have succeeded
with this procedure. Note that for both I have used the base-runit installation;
it's possible that using a different init system (openrc and s6 are available
currently) will require different steps.

### Rambling

>You thought it could be beneficial? But how could that be if nobody is going to
read this?

That same logic can be applied to every "article" I make, though. It makes more
sense to assume that somebody *is* reading, even if that assumption is
unfounded.
