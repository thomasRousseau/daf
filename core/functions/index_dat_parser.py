import pymsiecf
import common
from datetime import datetime, timedelta

def parse_index_dat(filepath):
    msiecf_file = pymsiecf.file()
    msiecf_file.open(filepath)
    #try:
    #  msiecf_file.open_file_object(filepath)
    #except IOError as exception:
    #  print(u'unable to open file with error: {0:s}'.format(exception))
    #  return

    format_version = msiecf_file.format_version
    cache_directories = []
    for cache_directory_name in msiecf_file.cache_directories:
      cache_directories.append(cache_directory_name)

    for item_index in range(0, msiecf_file.number_of_items):
        try:
            msiecf_item = msiecf_file.get_item(item_index)
            if isinstance(msiecf_item, pymsiecf.leak):
                pass

            elif isinstance(msiecf_item, pymsiecf.redirected):
                pass

            elif isinstance(msiecf_item, pymsiecf.url):
                timestamps = parse_url(format_version, cache_directories, msiecf_item)
                print "Type: Url"
                print "Primary timestamp: " + timestamps[0]
                print "Secondary timestamp: " + timestamps[1]
                print "Http headers: " + timestamps[2]
                print "---------------------------------------------\n"

        except IOError as exception:
            print(u'Unable to parse item: {0:d} with error: {1:s}'.format(item_index, exception))

    for item_index in range(0, msiecf_file.number_of_recovered_items):
        try:
            msiecf_item = msiecf_file.get_item(item_index)
            if isinstance(msiecf_item, pymsiecf.leak):
                pass

            elif isinstance(msiecf_item, pymsiecf.redirected):
                pass

            elif isinstance(msiecf_item, pymsiecf.url):
                timestamps = parse_url(format_version, cache_directories, msiecf_item, True)
                print "Type: Url (recovered)"
                print "Primary timestamp: " + timestamps[0]
                print "Secondary timestamp: " + timestamps[1]
                print "Http headers: " + timestamps[2]
                print "---------------------------------------------\n"

        except IOError as exception:
            print(u'Unable to parse item: {0:d} with error: {1:s}'.format(item_index, exception))

    msiecf_file.close()


def parse_url(format_version, cache_directories, msiecf_item, recovered=False):
    primary_timestamp = convert_timestamp(msiecf_item.get_primary_time_as_integer())
    secondary_timestamp = convert_timestamp(msiecf_item.get_secondary_time_as_integer())

    if msiecf_item.type:
      if msiecf_item.type == u'cache':
        primary_timestamp = "Last access time: " + primary_timestamp
        secondary_timestamp = "Content modification time: " + secondary_timestamp

      elif msiecf_item.type == u'cookie':
        primary_timestamp = "Last access time: " + primary_timestamp
        secondary_timestamp = "Content modification time: " + secondary_timestamp

      elif msiecf_item.type == u'history':
        primary_timestamp = "Last visited time: " + primary_timestamp
        secondary_timestamp = "Last visited time: " + secondary_timestamp

      elif msiecf_item.type == u'history-daily':
        primary_timestamp = "Last visited time: " + primary_timestamp
        secondary_timestamp = "Last visited time (Localtime): " + secondary_timestamp

      elif msiecf_item.type == u'history-weekly':
        primary_timestamp = "Creation time: " + primary_timestamp
        secondary_timestamp = "Last visited time (Localtime): " + secondary_timestamp

    
    http_headers = u''
    if msiecf_item.type and msiecf_item.data:
      if msiecf_item.type == u'cache':
        if msiecf_item.data[:4] == b'HTTP':
          try:
            http_headers = msiecf_item.data[:-1].decode(u'ascii')
          except UnicodeDecodeError:
            http_headers = msiecf_item.data[:-1].decode(
                u'ascii', errors=u'replace')
    return [primary_timestamp, secondary_timestamp, http_headers]

def convert_timestamp(timestamp):
    epoch_start = datetime(year=1601, month=1,day=1)
    seconds_since_epoch = timestamp/10**7
    date = epoch_start + timedelta(seconds=seconds_since_epoch)
    return '%s/%s/%s' % (date.month, date.day, date.year)

print "History"
filepath = "/media/daudau/ce551a8e-94b5-4b2c-889c-51f906c103a5/disk2/Users/IEUser/AppData/Local/Microsoft/Windows/History/History.IE5/index.dat"
parse_index_dat(filepath)

print "-----------------------------------------------------------------------\n\n"
print "Cache"
filepath = "/media/daudau/ce551a8e-94b5-4b2c-889c-51f906c103a5/disk2/Users/IEUser/AppData/Local/Microsoft/Windows/Temporary Internet Files/Content.IE5/index.dat"
parse_index_dat(filepath)

print "-----------------------------------------------------------------------\n\n"
print "Cookies"
filepath = "/media/daudau/ce551a8e-94b5-4b2c-889c-51f906c103a5/disk2/Users/IEUser/AppData/Roaming/Microsoft/Windows/Cookies/index.dat"
parse_index_dat(filepath)
