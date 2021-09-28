# Warning
This is just a dump of files, mosterly work in progress. It desperately needs cleaning...


# Installation
 - Download the latest (stable) Micropython Firmware from here: https://micropython.org/download/esp32/
 - Install ampy:

    sudo pip3 install adafruit-ampy

 - Upload all python files:

    for a in *.py; do echo "uploading $a"; ampy -p /dev/ttyUSB0 put $a; echo "$a is done"; done


