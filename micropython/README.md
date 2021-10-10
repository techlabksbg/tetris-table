# Warning
This is just a dump of files, mosterly work in progress. It desperately needs cleaning...


# Installation
 - Download the latest (stable) Micropython Firmware from here: https://micropython.org/download/esp32/
 - Install ampy:

    sudo pip3 install adafruit-ampy

 - Upload all python files:

    for a in *.py; do echo "uploading $a"; ampy -p /dev/ttyUSB0 put $a; echo "$a is done"; done


# Upload via Webserver
 - Modify config.py accordingly.
 - Start the Webserver (by pressing the 8th button), connect to the IP indicated (http, on port 80)
 - You can upload a single file via browser or via curl (adjust the IP address!)

   curl -F "file=@main.py" http://192.168.1.181 


# IDEs
I currently use vim to edit code, and ampy to upload it (or the web-uploader with curl). You may try the following:
 - https://lemariva.com/blog/2018/12/micropython-visual-studio-code-as-ide
 - https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/
 - https://blog.jetbrains.com/pycharm/2018/01/micropython-plugin-for-pycharm/

