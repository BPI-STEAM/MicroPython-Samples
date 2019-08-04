
import ubinascii
import os
import gc

statvfs_fields = ['bsize', 'frsize', 'blocks',
                  'bfree', 'bavail', 'files', 'ffree', ]
info = dict(zip(statvfs_fields, os.statvfs('/flash')))
# print(info)
print('ffs flash: ' + str(info['bsize'] * info['bfree'] / 1024) + ' kb')

print('mpy ram: ' + str(gc.mem_free()) + ' bit')
gc.collect()
print('mpy ram: ' + str(gc.mem_free()) + ' bit')
