import sys
import logging
from sail_sms import SMSParser, SMSImporter, SMSBackup
import os

if __name__ == '__main__':
    commhistory_path = "/home/nemo/.local/share/commhistory/commhistory.db"
    backup_tool = SMSBackup(commhistory_path, "backup/")
    if len(sys.argv) >= 3:
        if sys.argv[1] == "--import" and os.path.isfile(sys.argv[2]):
            parser = SMSParser(sys.argv[2])
            importer = SMSImporter(commhistory_path)
            sms_list = parser.get_all_sms_in_sf_format()
            backup_tool.create_backup()
            for sms in sms_list:
                importer.import_sms(sms)
            logging.info("Imported %d SMS", len(sms_list))
        elif sys.argv[1] == "--restore" and os.path.isfile(sys.argv[2]):
            backup_tool.restore_backup(sys.argv[2])
    elif len(sys.argv) == 2:
        if sys.argv[1] == "--backup":
            backup_tool.create_backup()
    else:
        print("SMS Backup & Restore Importer for Sailfish OS")
        print("Import a XML-File:")
        print("\tpython sms_import.py --import [xml-file]")
        print("Create a backup:")
        print("\tpython sms_import.py --backup")
        print("Import a commhistory.db Backup:")
        print("\tpython sms_import.py --restore [backup-file]")
        sys.exit()
