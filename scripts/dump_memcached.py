# The majority of this code was taken from http://pastebin.com/JZWZqzMr
# and modified slightly to fit the project's needs
import utils.djangoenv
import memcache
import re
from django.conf import settings
from datetime import datetime
from django.core.cache import cache
 
loc_parts = settings.CACHES['default']['LOCATION'].split(':')
host = loc_parts[0]
port = loc_parts[1]
mc = memcache.Client((':'.join(loc_parts),))

mc_server = mc.servers[0]
mc_server.connect()
slabs = []
mc_server.send_cmd('stats items')

while 1:
        line = mc_server.readline()
        if not line or line.strip() == 'END': break

        #gets the list of item details
        item = line.split(' ', 2)
        #print(item[1])

        slab = item[1].split(':', 2)
        slab_id = slab[1]

        if slab_id not in slabs:
                slabs.append(slab_id)

for slab_item in slabs:
        mc_server.send_cmd('stats cachedump %s 0' % slab_item)
        while 1:
                line = mc_server.readline()
                if not line or line.strip() == 'END': break

                item_details = line.split(' ')
                value = cache.get(re.search(r'^:\d+:(.*)', str(item_details[1])).groups(1)[0])

                print("\033[93m[%s]\033[0m \n\
        \033[94mkey: %s\033[0m \n\
        \033[95mlength: %s\033[0m \n\
        \033[91mexpires: %s\033[0m \n\
        value: %s\n"  % (slab_item, item_details[1], item_details[2][1:], datetime.fromtimestamp(int(item_details[4])).strftime("%Y-%m-%d %H:%M:%S"), value))