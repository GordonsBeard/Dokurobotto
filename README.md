Dokurobotto
===========

Dokurobotto (Doc Robot) is an IRC bot that is used on GameSurge to do some unobtrusive robot stuff.

## Setup
Edit `settings_template.ini` and rename to `settings.ini`
If docrobot.py is launched with `-d` this will enable DEBUG mode. More logging is included and it will join a seperate channel.

* * *

### Features / Plugins
#### YouTube
##### Identifying YouTube URLs
```
16:31 <@ docBeard> http://youtu.be/7lTOnPc9h-c
16:31 <      DR-X> *** YouTube: MGS Peace Walker - Heavens Divide - HD+Lyrics (315")
```

##### Tests
* Yes there are tests! `plugins/youtube/youtube_tests.py`
