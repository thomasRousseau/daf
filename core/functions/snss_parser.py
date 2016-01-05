import os
import sys
import struct
import StringIO

SNSS_HEADER = 0x53534E53

TYPE_ID_DICT = {'0': "CommandSetTabWindow",
                 '1': "CommandSetWindowBounds", #Obsolete
                 '2': "CommandSetTabIndexInWindow",
                 '3': "CommandTabClosedObsolete", #Obsolete
                 '4': "CommandWindowClosedObsolete", #Obsolete
                 '5': "CommandTabNavigationPathPrunedFromBack",
                 '6': "CommandUpdateTabNavigation",
                 '7': "CommandSetSelectedNavigationIndex",
                 '8': "CommandSetSelectedTabInIndex",
                 '9': "CommandSetWindowType",
                 '10': "CommandSetWindowBounds2", #Obsolete
                 '11': "CommandTabNavigationPathPrunedFromFront",
                 '12': "CommandSetPinnedState",
                 '13': "CommandSetExtensionAppID",
                 '14': "CommandSetWindowBounds3",
                 '15': "CommandSetWindowAppName",
                 '16': "CommandTabClosed",
                 '17': "CommandWindowClosed",
                 '18': "CommandSetTabUserAgentOverride",
                 '19': "CommandSessionStorageAssociated",
                 '20': "CommandSetActiveWindow"}


def ssns_parser(file_path):
    """
    Parses a SNSS file and returns a list of dictionnaries
    containing the commands information.
    """
    ssns_content = []

    f = open(file_path, 'rb')
    f.seek(0, os.SEEK_END)
    end = f.tell()
    f.seek(0, os.SEEK_SET)
    header = struct.unpack('I', f.read(4))[0] # uint32
    if header != SNSS_HEADER:
        raise Exception("Invalid file format!")
    version = struct.unpack('i', f.read(4))[0] # int32

    while (end - f.tell()) > 0:
        # Each command start with it size in a uint16 format
        command_size = struct.unpack('H', f.read(2))[0] # uint16
        if command_size == 0:
            raise Exception("Corrupted File!")
        # Then there is the id of the command as an uint8
        command_type_id = struct.unpack('B', f.read(1))[0] # uint8

        # Then the actual datas of the command whuch depend of the id
        content = f.read(command_size - 1)
        if TYPE_ID_DICT.has_key(str(command_type_id)):
            content = StringIO.StringIO(content)
            command_dict = {'Id': str(command_type_id),
                            'Type': TYPE_ID_DICT[str(command_type_id)]}
            command_dict.update(getattr(sys.modules[__name__],
                "get" + TYPE_ID_DICT[str(command_type_id)])(content))
            ssns_content.append(command_dict)

    f.close()
    return ssns_content


def getCommandSetTabWindow(content):
    windows_id = readInt(content)
    tab_id = readInt(content)
    return {'Windows ID': windows_id, 'Tab ID': tab_id}


def getCommandSetWindowBounds(content):
    return {}


def getCommandSetTabIndexInWindow(content):
    tab_id = readInt(content)
    index = readInt(content)
    return {'Tab ID': tab_id, 'Index': index}


def getCommandTabClosedObsolete(content):
    tab_id = readInt(content)
    close_time = struct.unpack('q', content.read(8))[0] # int64
    #TODO: transform time into datetime and determine timezone
    return {'Tab ID': tab_id, 'Close time': close_time}


def getCommandWindowClosedObsolete(content):
    windows_id = struct.unpack('B', content.read(1))[0] # uint8
    close_time = struct.unpack('q', content.read(8))[0] # int64
    #TODO: transform time into datetime and determine timezone
    return {'Windows ID': windows_id, 'Close time': close_time}


def getCommandTabNavigationPathPrunedFromBack(content):
    tab_id = readInt(content)
    index = readInt(content)
    return {'Tab ID': tab_id, 'Index': index}


def getCommandUpdateTabNavigation(content):
    """
    TODO: Correct the strange behavior
    """
    content.seek(0, os.SEEK_END)
    content_size = content.tell()
    content.seek(0, os.SEEK_SET)

    payload_size = readInt(content)
    
    tab_id = readInt(content)
    index = readInt(content)
    url = readStringFromPickle(content, content_size)
    title = readString16FromPickle(content, content_size)
    page_state = readStringFromPickle(content, content_size)
    transition_type = readInt(content)
    type_mask = readInt(content)
    referrer = readStringFromPickle(content, content_size)
    referrer_policy = readInt(content)
    original_request_url = readStringFromPickle(content, content_size)
    is_overriding_user_agent = bool(readInt(content))
    timestamp = struct.unpack('q', content.read(8))[0] # int64
    #TODO: transform timestamp to datetime
    search_terms = readString16FromPickle(content, content_size)
    http_status_code = readInt(content)

    return {'Tab ID': tab_id,
            'Index': index,
            'Url': url,
            'Title': title,
            'Page state (encoded)': page_state,
            'Transition type': transition_type,
            'Type mask (has_post_data)': type_mask,
            'Referrer': referrer,
            'Referrer policy': referrer_policy,
            'Original request url': original_request_url,
            'Is overidding user agent': is_overriding_user_agent,
            'Timestamp': timestamp,
            'Search terms': search_terms,
            'Http status code': http_status_code}


def getCommandSetSelectedNavigationIndex(content):
    return {}


def getCommandSetSelectedTabInIndex(content):
    return {}


def getCommandSetWindowType(content):
    return {}


def getCommandSetWindowBounds2(content):
    return {}


def getCommandTabNavigationPathPrunedFromFront(content):
    return {}


def getCommandSetPinnedState(content):
    return {}


def getCommandSetExtensionAppID(content):
    return {}


def getCommandSetWindowBounds3(content):
    return {}


def getCommandSetWindowAppName(content):
    return {}


def getCommandTabClosed(content):
    return {}


def getCommandWindowClosed(content):
    return {}


def getCommandSetTabUserAgentOverride(content):
    return {}


def getCommandSessionStorageAssociated(content):
    return {}


def getCommandSetActiveWindow(content):
    return {}


def readInt(content):
    return struct.unpack('I', content.read(4))[0] # uint32    


def readStringFromPickle(content, content_size):
    string_length = struct.unpack('I', content.read(4))[0] # uint32
    if string_length > content_size - content.tell():
        return None #content.read(8).decode('utf-8', 'ignore')
    else:
        return content.read(string_length).decode('utf-8', 'ignore')    


def readString16FromPickle(content, content_size):
    string_length = struct.unpack('I', content.read(4))[0] # uint32
    if string_length*2 > content_size - content.tell():
        return None #content.read(16).decode('utf-16', 'ignore')
    else:
        return content.read(string_length*2).decode('utf-16', 'ignore')
    

print ssns_parser("/mnt/441EDCA81EDC93F0/Data/Linux/Documents/Eurecom/Project/Samples/disk_mounted/disk4/Users/IEUser/AppData/Local/Google/Chrome/User Data/Default/Current Session")

