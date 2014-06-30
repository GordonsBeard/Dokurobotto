Dokurobotto
===========

Dokurobotto ([Doc Robot](http://megaman.wikia.com/wiki/Doc_Robot)) is an IRC bot that is used on GameSurge to do some unobtrusive robot stuff.

* * *

### Features / Plugins
#### YouTube
##### Identifying YouTube URLs
```
< medic_hp_u> http://youtu.be/7lTOnPc9h-c
      < DR-X> *** YouTube: MGS Peace Walker - Heavens Divide - HD+Lyrics (315")
```

##### Logging YouTube URLs
If enabled, DR will tell you how many times we've all seen your dumb video.
When in a private message, identifying a URL will not increase the post count.
```
< Tele-Viper> http://www.youtube.com/watch?v=xZ1C5klmkTU
      < DR-X> *** YouTube: It's not spam (56") (post 77)
```

##### Searching YouTube
Allows users to search YouTube via keyword, one result.
Multiple-word queries need to be wrapped in "quotation marks"
```
 < Detective> !yt "impossible soul"
      < DR-X> http://youtu.be/8R_3mXZBsuU
      < DR-X> *** YouTube: Sufjan Stevens- Impossible Soul (1535")

       < doc> so you can do things like !yt "clark future daniel" now and not have to worry
      < DR-X> http://youtu.be/vazBxk_avxc
      < DR-X> *** YouTube: Clark - Future Daniel (249") (post 2)
```

* * *
### History
```
DR-1:   YouTube module added.
   1.0:     Identify YouTube links.
   1.1:     Stores links in database.
   1.2:     Responds to privmsg commands.
   1.3:     Searching via !yt added.

DR-0:   Joins channels. Not much else.
```
