import sys
import logging
from sail_sms import SMSParser, SMSImporter

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "SMS Backup & Restore Importer for Sailfish OS"
        print "Usage: python sms_import.py [xml-file]"
        sys.exit()
    parser = SMSParser(sys.argv[1])
    importer = SMSImporter("/home/nemo/.local/share/commhistory/commhistory.db")
    sms_list = parser.get_all_sms_in_sf_format()
    for sms in sms_list:
        importer.import_sms(sms)
    logging.info("Imported %d SMS", len(sms_list))