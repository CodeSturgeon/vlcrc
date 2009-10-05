# Python VLC RemoteControl interface bridge
_An easy wat to get VLC and Python talking._

## VLC Setup
Have VLC setup it's RC interface on local TCP port 4222. Either by config or using the following command line options:

    --extraintf=rc --rc-host=127.0.0.1:4222

## Python Setup

    python setup.py install
No dependancies, just python and included batteries.

## Tool usage
  
    $vlcrc-easygui
Uses a small EasyGUI tool to group filepaths of videos. Good for sorting videos out of folders of random junk. Dumps the file paths of all the grouped items.  
  
## Class usage

    from vlcrc import VLCRemote
    vlc = VLCRemote(hostname, port_no)
    now_playing = vlc.get_filename()
    while 1:
        if now_playing.find('wiggles')>=0:
            vlc.next()
