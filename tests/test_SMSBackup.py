import unittest
from sail_sms import SMSBackup, SMSImporter, SMSParser
import time
import os

class SMSBackupTest(unittest.TestCase):


    def setUp(self):
        self.backup_tool = SMSBackup("assets/test_commhistory.db", "assets/")
        parser = SMSParser("assets/samples.xml")
        self.sms_list = parser.get_all_sms_in_sf_format()
        self.importer = SMSImporter("assets/test_commhistory.db")
        self.empty_backup = None
        self.non_empty_backup = None

    def tearDown(self):
        self.importer.reload_db()
        self.importer.remove_all_groups_and_msgs()
        if self.empty_backup is not None:
            if os.path.isfile(self.empty_backup):
                os.remove(self.empty_backup)
        if self.non_empty_backup is not None:
            if os.path.isfile(self.non_empty_backup):
                os.remove(self.non_empty_backup)
        if os.path.isdir("backup_folder/"):
            os.rmdir("backup_folder/")

    def test_create_and_restore_backup(self):
        timestamp = int(time.time())
        self.backup_tool.create_backup(timestamp)
        self.empty_backup = "assets/commhistory-" + str(timestamp) + ".db"
        self.assertTrue(os.path.isfile(self.empty_backup))
        self.importer.import_sms(self.sms_list[0])
        self.importer.reload_db()
        time.sleep(1)
        timestamp = int(time.time())
        self.backup_tool.create_backup(timestamp)
        self.non_empty_backup = "assets/commhistory-" + str(timestamp) + ".db"
        self.assertTrue(os.path.isfile(self.non_empty_backup))
        self.backup_tool.restore_backup(self.empty_backup)
        self.importer.reload_db()  
        self.assertEqual(self.importer.get_msg_count(), 0)
        self.assertEqual(self.importer.get_group_count(), 0)
        self.backup_tool.restore_backup(self.non_empty_backup)
        self.importer.reload_db()
        self.assertEqual(self.importer.get_msg_count(), 1)
        self.assertEqual(self.importer.get_group_count(), 1)
        
    def test_should_create_backup_folder(self):
        bt = SMSBackup("assets/test_commhistory.db", "backup_folder/")
        timestamp = int(time.time())
        self.empty_backup = "backup_folder/commhistory-" + str(timestamp) + ".db"
        bt.create_backup(timestamp)
        self.assertTrue(os.path.isfile(self.empty_backup))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()