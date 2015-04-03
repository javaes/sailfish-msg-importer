# sailfish-msg-importer
This little script helps to import messages from other mobile OSs to Sailfish OS. The first version only supports Android SMS messages exported by SMS Backup &amp; Restoree.


Please use with caution, I wrote this script for personal use and the only test case was the import of my old messages from my Android phone.
# Usage

Copy both python files to the same directory on your Sailfish OS phone. The XML-File with the messages can be placed in a directory of your choice on your device.

Open a command shell on your device and navigate to the path were you put the script.

    [nemo@Jolla sms_importer]$ python sms_import [xml-file]

If no error message is printed the import was successful.
