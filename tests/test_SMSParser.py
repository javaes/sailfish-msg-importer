import unittest
from sail_sms import SMSParser


class SMSParserTest(unittest.TestCase):


    def setUp(self):
        parser = SMSParser("assets/samples.xml")
        self.sms_list = parser.get_all_sms_in_sf_format()

    def assert_sms(self, sms):
        self.assertEqual(sms["type"], 2)
        self.assertEqual(sms["isDraft"], 0)
        self.assertEqual(sms["isRead"], 1)
        self.assertEqual(sms["isMissedCall"], 0)
        self.assertEqual(sms["isEmergencyCall"], 0)
        self.assertEqual(sms["bytesReceived"], 0)
        self.assertEqual(sms["localUid"], "/org/freedesktop/Telepathy/Account/ring/tel/account0")        
        self.assertEqual(sms["reportDelivery"], 0)
        self.assertEqual(sms["validityPeriod"], 0)
        self.assertEqual(sms["readStatus"], 0)
        self.assertEqual(sms["reportRead"], 0)
        self.assertEqual(sms["reportedReadRequested"], 0)
        self.assertEqual(sms["isAction"], 0)
        self.assertEqual(sms["hasExtraProperties"], 0)
        self.assertEqual(sms["hasMessageParts"], 0)
        
    def assert_received_sms(self, received_sms):
        self.assertEqual(received_sms["direction"], 1)
        self.assertEqual(received_sms["status"], 0)
        self.assertEqual(received_sms["lastModified"], "1970-01-01T01:00:00.000")
        
    def assert_sent_sms(self, sent_sms):
        self.assertEqual(sent_sms["direction"], 2)
        self.assertEqual(sent_sms["status"], 2)    
    
    def test_parse_received_sms(self):        
        received_sms = self.sms_list[1]
        self.assert_sms(received_sms)
        self.assert_received_sms(received_sms)
        self.assertEqual(received_sms["startTime"], "1341324992")
        self.assertEqual(received_sms["endTime"], "1341324992")
        self.assertEqual(received_sms["remoteUid"], "+4949494949499")
        self.assertEqual(received_sms["freeText"], "Bye Tester! :)")
    
    def test_parse_sent_sms(self):
        sent_sms = self.sms_list[0]
        self.assert_sms(sent_sms)
        self.assert_sent_sms(sent_sms)
        self.assertEqual(sent_sms["startTime"], "1341324666")
        self.assertEqual(sent_sms["endTime"], "1341324666")
        self.assertEqual(sent_sms["remoteUid"], "+4949494949499")
        self.assertEqual(sent_sms["freeText"], "Hi Test!")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()