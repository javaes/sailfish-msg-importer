import unittest
from sail_sms import SMSImporter, SMSParser


class SMSImporterTest(unittest.TestCase):

    def setUp(self):
        parser = SMSParser("assets/samples.xml")
        self.sms_list = parser.get_all_sms_in_sf_format()
        self.importer = SMSImporter("assets/test_commhistory.db")

    def tearDown(self):
        self.importer.remove_all_groups_and_msgs()

    def test_import_received_sms(self):
        self.importer.import_sms(self.sms_list[1])
        self.assertEqual(self.importer.get_msg_count(), 1)
        self.assertEqual(self.importer.get_group_count(), 1)
    
    def test_import_sent_sms(self):
        self.importer.import_sms(self.sms_list[0])
        self.assertEqual(self.importer.get_msg_count(), 1)
        self.assertEqual(self.importer.get_group_count(), 1)
    
    def test_import_sms_from_two_different_remote_uids(self):
        for sms in self.sms_list:
            self.importer.import_sms(sms)
        self.assertEqual(self.importer.get_msg_count(), len(self.sms_list))
        self.assertEqual(self.importer.get_group_count(), 2)
        
    def test_remove_all_groups_and_msgs(self):
        for sms in self.sms_list:
            self.importer.import_sms(sms)
        self.importer.remove_all_groups_and_msgs()
        self.assertEqual(self.importer.get_msg_count(), 0)
        self.assertEqual(self.importer.get_group_count(), 0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()