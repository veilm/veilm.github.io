---
title: "RSS with a private Nitter instance"
date: 2024-02-19T20:30:00-04:00
---

### 2024-10-11 Update
A while ago now, some endpoints were disabled, and the Python script mentioned
in this article will no longer generate any credentials. I don't have time right
now to update this with new instructions. Sorry. Hopefully some part can still
be helpful for reference.

### Disclaimer
Depending on future updates to Twitter's authentication system and/or the Nitter
project, the information in this post may be inaccurate. I am only declaring my
faith in the context of the time I am writing this.

### Introduction
As you likely already know if you're reading this, the great and holy Mr. Musk
has finally killed off guest accounts, thus extinguishing the already-fading
light of public Nitter instances. Ah, the joys of the modern web...

Fortunately, it's still possible to use Nitter's RSS feature by hosting your own
private instance on your own computer, using a personal Twitter account. The
process is not complex, but sorting through the comments on the [Nitter GitHub
repository](https://github.com/zedeus/nitter/) is pretty annoying, so I have
compiled the basic steps here.

### Requirements
- You need an operating system compatible with Nitter. I'm using Arch Linux, but
would expect other distributions and probably macOS/BSD to also work. If you're
using Windoze, how did you find my website?
- You need a Twitter account, the authorization tokens of which will be used. I
would not recommend using your primary account, in case it gets locked.
- ``nim``
- ``libsass``, if you want working CSS
- ``libpcre`` (``pcre`` on Arch)
- ``redis``

There are other implied requirements such as basic reading comprehension and
digital literacy.

### Tutorial
Clone the Nitter repository and switch into the ``guest_accounts`` branch.

```sh
$ git clone https://github.com/zedeus/nitter
$ cd nitter
$ git checkout guest_accounts
```

Make a modification to the ``src/auth.nim`` file, commenting out line 205.
```diff
--- auth.nim
+++ auth2.nim
@@ -202,7 +202,7 @@
     quit 1

   let accountsPrePurge = accountPool.len
-  accountPool.keepItIf(not it.hasExpired)
+  # accountPool.keepItIf(not it.hasExpired)

   log "Successfully added ", accountPool.len, " valid accounts."
   if accountsPrePurge > accountPool.len:
```

Compile Nitter.

```sh
$ nimble build -d:release
$ nimble scss
$ nimble md
```

Copy the example configuration.

```sh
$ cp nitter.example.conf nitter.conf
```

Look through the file and make any desired changes. You may want to increase
``rssMinutes`` to decrease the likelihood of being rate limited, for example.

Then, generate the JSON for your authorization tokens using the following Python
script, written by 0o120 and csisoap. Modify the ``username`` and ``password``
variables to match the account you wish to use.

```py
import requests
import base64
import json

username = "XXXXXXXXXXXX"
password = "XXXXXXXXXXXX"

TW_CONSUMER_KEY = "3nVuSoBZnx6U4vzUxf5w"
TW_CONSUMER_SECRET = "Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys"
TW_ANDROID_BASIC_TOKEN = "Basic {token}".format(
    token=base64.b64encode(
        (TW_CONSUMER_KEY + ":" + TW_CONSUMER_SECRET).encode()
    ).decode()
)

authentication = None
bearer_token_req = requests.post(
    "https://api.twitter.com/oauth2/token",
    headers={
        "Authorization": TW_ANDROID_BASIC_TOKEN,
        "Content-Type": "application/x-www-form-urlencoded",
    },
    data="grant_type=client_credentials",
).json()
bearer_token = " ".join(str(x) for x in bearer_token_req.values())

guest_token = requests.post(
    "https://api.twitter.com/1.1/guest/activate.json",
    headers={
        "Authorization": bearer_token,
    },
).json()["guest_token"]

twitter_header = {
    "Authorization": bearer_token,
    "Content-Type": "application/json",
    "User-Agent": "TwitterAndroid/9.95.0-release.0 (29950000-r-0) ONEPLUS+A3010/9 (OnePlus;ONEPLUS+A3010;OnePlus;OnePlus3;0;;1;2016)",
    "X-Twitter-API-Version": "5",
    "X-Twitter-Client": "TwitterAndroid",
    "X-Twitter-Client-Version": "9.95.0-release.0",
    "OS-Version": "28",
    "System-User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ONEPLUS A3010 Build/PKQ1.181203.001)",
    "X-Twitter-Active-User": "yes",
    "X-Guest-Token": guest_token,
}

session = requests.Session()

task1 = session.post(
    "https://api.twitter.com/1.1/onboarding/task.json",
    params={
        "flow_name": "login",
        "api_version": "1",
        "known_device_token": "",
        "sim_country_code": "us",
    },
    json={
        "flow_token": None,
        "input_flow_data": {
            "country_code": None,
            "flow_context": {
                "referrer_context": {
                    "referral_details": "utm_source=google-play&utm_medium=organic",
                    "referrer_url": "",
                },
                "start_location": {"location": "deeplink"},
            },
            "requested_variant": None,
            "target_user_id": 0,
        },
    },
    headers=twitter_header,
)

session.headers["att"] = task1.headers.get("att")
task2 = session.post(
    "https://api.twitter.com/1.1/onboarding/task.json",
    json={
        "flow_token": task1.json().get("flow_token"),
        "subtask_inputs": [
            {
                "enter_text": {
                    "suggestion_id": None,
                    "text": username,
                    "link": "next_link",
                },
                "subtask_id": "LoginEnterUserIdentifier",
            }
        ],
    },
    headers=twitter_header,
)

task3 = session.post(
    "https://api.twitter.com/1.1/onboarding/task.json",
    json={
        "flow_token": task2.json().get("flow_token"),
        "subtask_inputs": [
            {
                "enter_password": {"password": password, "link": "next_link"},
                "subtask_id": "LoginEnterPassword",
            }
        ],
    },
    headers=twitter_header,
)

task4 = session.post(
    "https://api.twitter.com/1.1/onboarding/task.json",
    json={
        "flow_token": task3.json().get("flow_token"),
        "subtask_inputs": [
            {
                "check_logged_in_account": {"link": "AccountDuplicationCheck_false"},
                "subtask_id": "AccountDuplicationCheck",
            }
        ],
    },
    headers=twitter_header,
).json()

for t4_subtask in task4.get("subtasks", []):
    if "open_account" in t4_subtask:
        authentication = t4_subtask["open_account"]
        break

    elif "enter_text" in t4_subtask:
        response_text = t4_subtask["enter_text"]["hint_text"]
        code = input(f"Requesting {response_text}: ")

        task5 = session.post(
            "https://api.twitter.com/1.1/onboarding/task.json",
            json={
                "flow_token": task4.get("flow_token"),
                "subtask_inputs": [
                    {
                        "enter_text": {
                            "suggestion_id": None,
                            "text": code,
                            "link": "next_link",
                        },
                        "subtask_id": "LoginAcid",
                    }
                ],
            },
            headers=twitter_header,
        ).json()

        for t5_subtask in task5.get("subtasks", []):
            if "open_account" in t5_subtask:
                authentication = t5_subtask["open_account"]

print(json.dumps(authentication))
```

As far as I can tell, this script will only work for accounts with 2FA disabled
(which is the default). It's still possible to use Nitter with a 2FA-enabled
account, but it will require further intervention which I didn't bother to
investigate.

When you run the file, it will print JSON output containing your credentials.
Save these to a file called ``guest_accounts.jsonl`` in the root of your
``nitter`` source directory. Don't pretty-format the JSON; it's supposed to be
on one line.

Your ``guest_accounts.jsonl`` should end up structured like
```json
{"user": {"id": 1111111111111111111, "id_str": "1111111111111111111", "name": "XXXXXXXXXX", "screen_name": "XXXXXXXXXXXXXXX"}, "next_link": {"link_type": "subtask", "link_id": "next_link", "subtask_id": "SuccessExit"}, "oauth_token": "1111111111111111111-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "oauth_token_secret": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "known_device_token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "attribution_event": "login"}
```

I'm not sure how long your tokens can be active before you'll need to regenerate
them. I'd guess that it's around a few months at least, though.

Now, start Redis and run the Nitter binary.

```sh
$ systemctl start redis
$ ./nitter
```

By default,
- Redis runs on ``localhost:6379``, which is also what nitter.conf is set to use.
- Redis has no password, and nitter.conf doesn't provide a password.
- nitter.conf configures Nitter to run on ``0.0.0.0:8080``.

So, you should now be able to access your RSS feeds at that location. For
example, the following should work as expected.
```sh
$ curl 0.0.0.0:8080/nearcyan/rss
```

Of course, Nitter will be inaccessible if its service stops running, so you will
need to launch it on startup.

### Rate limits and banning
I only sat down and figured out how to do this today, so I haven't had much of a
chance to experience any possible reprecussions.

I didn't see much relevant information on GitHub either. Here is one anecdote:
> it's working for me but the account gets locked if you try to paginate more than
a couple of pages in search

I've also heard that Twitter blocks connections from known VPS IP addresses;
it's probably better to use your local machine.

In my nitter.conf, I set ``rssMinutes = 60``, and I have configured my RSS
client to only query my Nitter instance once per two minutes or so. I expect
this to stay under the rate limits, although I may experiment with more liberal
usage in the future. Ideally, I'd be able to fetch every feed once per minute or
so.

### Sources
- https://github.com/zedeus/nitter/tree/master?tab=readme-ov-file#installation
- https://github.com/zedeus/nitter/issues/983#issuecomment-1914616663
- https://github.com/zedeus/nitter/issues/1155#issuecomment-1917167072
- https://github.com/zedeus/nitter/issues/1155#issuecomment-1953290183
- https://github.com/zedeus/nitter/issues/1156#issuecomment-1922999620

### Conclusion
:(

O our great Elon, why must you punish us so? Is the will of the scrapers truly
so incompatible with yours? Would it harm you so much to simply provide Sam with
the training data he seeks, and leave the poor users in peace? I propose
focusing our engineering efforts on Neuralink instead...
