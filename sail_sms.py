from xml.dom import minidom
import datetime
import uuid
import sqlite3
import logging
from shutil import copyfile
import time

class SMSParser(object):
    """
    This class parses a SMS Backup & Restore file and converts its entries to
    Sailfish OS messages which can be imported by using the SMSImporter class.
    """

    def __init__(self, xml_file):
        """
        Initializes the parser with an XML file to parse
        
        Parameters:
            xml_file    -       Path to SMS Backup & Restore file which will be
                                parsed
        """
        self.xml_file = xml_file

    def get_all_sms_in_sf_format(self):
        """
        Parses a SMS Backup & Restore XML File and convert its elements to a
        list of dictionaries with all mandatory Sailfish OS message fields.
        """
        xmldom = minidom.parse(self.xml_file)
        sms_list = xmldom.getElementsByTagName("sms")
        logging.info("Found %d SMS", len(sms_list))
        sailfish_sms_list = list()
        for sms in sms_list:
            if sms.attributes["protocol"].value == "0" or sms.attributes["protocol"].value == "193":
                sailfish_sms_list.append(self._convert_to_sailfish(sms))
        logging.info("Converted %d SMS", len(sailfish_sms_list))
        return sailfish_sms_list
    
    def _convert_to_sailfish(self, sms):
        entry = dict()
        entry["type"] = 2
        entry["startTime"] = entry["endTime"] = sms.attributes["date"].value[:-3]
        entry["isDraft"] = 0
        entry["isRead"] = 1
        entry["isMissedCall"] = 0
        entry["isEmergencyCall"] = 0
        entry["bytesReceived"] = 0
        entry["localUid"] = "/org/freedesktop/Telepathy/Account/ring/tel/account0"
        entry["remoteUid"] = sms.attributes["address"].value
        entry["parentId"] = None
        entry["subject"] = sms.attributes["subject"].value
        if entry["subject"] == "null":
            entry["subject"] = None
        entry["freeText"] = sms.attributes["body"].value
        entry["groupId"] = None
        entry["vCardFileName"] = None
        entry["vCardLabel"] = None
        entry["isDeleted"] = None
        entry["reportDelivery"] = 0
        entry["validityPeriod"] = 0
        entry["contentLocation"] = None
        entry["messageParts"] = None
        entry["headers"] = None
        entry["readStatus"] = 0
        entry["reportRead"] = 0
        entry["reportedReadRequested"] = 0
        entry["mmsId"] = None
        entry["isAction"] = 0
        entry["hasExtraProperties"] = 0
        entry["hasMessageParts"] = 0
        entry["messageToken"] = str(uuid.uuid4())
        if sms.attributes["type"].value == str(1):
            # received sms
            entry["direction"] = 1
            entry["status"] = 0            
            entry["lastModified"] = "1970-01-01T01:00:00.000"
        elif sms.attributes["type"].value == str(2):
            # sent sms
            entry["direction"] = 2
            entry["status"] = 2
            mod_date = datetime.datetime.fromtimestamp(int(sms.attributes["date"].value) / 1000)          
            entry["lastModified"] = mod_date.strftime("%Y-%m-%dT%H:%M:%S.%f")
        return entry
    
    def _group_by_remote_uid(self, sms_list):
        unique_remote_uids = set([sms["remoteUid"] for sms in sms_list])
        group_mapping = dict()
        for remote_uid in enumerate(unique_remote_uids, start=1):
            group_mapping[remote_uid[1]] = remote_uid[0]            
        for sms in sms_list:
            sms["groupId"] = group_mapping[sms["remoteUid"]]
            
    
class SMSImporter(object):
    """
    This class imports messages in in the Sailfish OS format to the Sailfish OS
    database. The messages are provided by a parsing class.
    """
    
    def __init__(self, db_path):
        """
        Initializes the database connection for the parser
        
        Parameters:
            db_path    -    Path to the sqlite3 database
        """
        self.db_path = db_path
        self.db = sqlite3.connect(db_path)
        self.c = self.db.cursor()
        
    def reload_db(self):
        """
        Reloads the database
        """
        self.db = sqlite3.connect(self.db_path)
        self.c = self.db.cursor()
        
    def import_sms(self, sf_sms):
        """
        Imports a message to the database.
        
        Parameters:
            sf_sms    -     Dictionary which provides all mandatory fields for a
                            Sailfish OS message
        """
        group_id = self._get_group(sf_sms["remoteUid"])
        if group_id is None:
            self._add_new_group(sf_sms["remoteUid"], 0)
            group_id = self._get_group(sf_sms["remoteUid"])
            logging.debug("Added new group with ID %d", group_id)
        self.c.execute("INSERT INTO Events(vCardLabel,\
                                            reportRead,\
                                            hasExtraProperties,\
                                            hasMessageParts,\
                                            readStatus,\
                                            messageParts,\
                                            reportDelivery,\
                                            messageToken,\
                                            vCardFileName,\
                                            isDeleted,\
                                            status,\
                                            headers,\
                                            localUid,\
                                            isDraft,\
                                            isEmergencyCall,\
                                            reportedReadRequested,\
                                            isMissedCall,\
                                            freeText,\
                                            lastModified,\
                                            remoteUid,\
                                            type,\
                                            isRead,\
                                            endTime,\
                                            mmsId,\
                                            parentId,\
                                            contentLocation,\
                                            startTime,\
                                            direction,\
                                            subject,\
                                            bytesReceived,\
                                            isAction,\
                                            validityPeriod,\
                                            groupId) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                            (sf_sms["vCardLabel"],
                                            sf_sms["reportRead"],
                                            sf_sms["hasExtraProperties"],
                                            sf_sms["hasMessageParts"],
                                            sf_sms["readStatus"],
                                            sf_sms["messageParts"],
                                            sf_sms["reportDelivery"],
                                            sf_sms["messageToken"],
                                            sf_sms["vCardFileName"],
                                            sf_sms["isDeleted"],
                                            sf_sms["status"],
                                            sf_sms["headers"],
                                            sf_sms["localUid"],
                                            sf_sms["isDraft"],
                                            sf_sms["isEmergencyCall"],
                                            sf_sms["reportedReadRequested"],
                                            sf_sms["isMissedCall"],
                                            sf_sms["freeText"],
                                            sf_sms["lastModified"],
                                            sf_sms["remoteUid"],
                                            sf_sms["type"],
                                            sf_sms["isRead"],
                                            sf_sms["endTime"],
                                            sf_sms["mmsId"],
                                            sf_sms["parentId"],
                                            sf_sms["contentLocation"],
                                            sf_sms["startTime"],
                                            sf_sms["direction"],
                                            sf_sms["subject"],
                                            sf_sms["bytesReceived"],
                                            sf_sms["isAction"],
                                            sf_sms["validityPeriod"],
                                            group_id))
        self.db.commit()
        logging.info("Imported SMS to Group %d", group_id)
    
    def _add_new_group(self, remote_uid, type=0):
        query = "INSERT INTO Groups(localUid, remoteUids, type, lastModified)\
                            VALUES('/org/freedesktop/Telepathy/Account/ring/tel/account0',?,?,0)"
        self.c.execute(query, (remote_uid, type))
        self.db.commit()
        
    def _get_group(self, remote_uid):
        query = "SELECT id FROM Groups WHERE remoteUids = '%s';" % remote_uid
        self.c.execute(query)
        result = self.c.fetchone()
        if result is not None:
            return result[0]
        return None
    
    def get_group_count(self):
        query = "SELECT * FROM Groups;"
        self.c.execute(query)
        return len(self.c.fetchall())
    
    def get_msg_count(self):
        query = "SELECT * FROM Events;"
        self.c.execute(query)
        return len(self.c.fetchall())
    
    def remove_all_groups_and_msgs(self):
        """
        Removes all messages and their groups from the database
        """
        query = "DELETE FROM Events WHERE 1 = 1;"
        self.c.execute(query)
        query = "DELETE FROM Groups WHERE 1 = 1;"
        self.c.execute(query)
        self.db.commit()
        
class SMSBackup(object):
    """
    This class creates and imports simple one-to-one database backups
    """
    
    def __init__(self, db_file, backup_path):
        """
        Parameters:
            db_file        -    Path to the sqlite3 database which should be saved
            backup_path    -    Path where new backups should be stored
        """
        self.db_file = db_file
        self.backup_path = backup_path
        
    def create_backup(self, timestamp=None):
        """
        Creates a copy of the database at the specified path named with a timestamp.
        
        Parameters:
            timestamp   -   optional, if you want to declare your own timestamp
                            or the backup.
        """
        if timestamp is None:
            timestamp = int(time.time())
        copyfile(self.db_file, self.backup_path + "commhistory-" + str(timestamp) + ".db")
        logging.info("Saved copy of %s to %s", self.db_file, self.backup_path + "commhistory-" + str(timestamp) + ".db")
    
    def restore_backup(self, backup_file):
        """
        Copies a backup to the database location. All connections with the database
        have to be reloaded, otherwise changes will be written to the old copy.
        
        Parameters:
            backup_file    -    Path to the sqlite3 Database which will replace
                                the current commhistory.db
        """
        copyfile(backup_file, self.db_file)
        logging.info("Restored backup from %s to %s", backup_file, self.db_file)