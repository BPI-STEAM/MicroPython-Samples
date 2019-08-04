import gc
import ubinascii
import os
statvfs_fields = ['bsize', 'frsize', 'blocks',
                  'bfree', 'bavail', 'files', 'ffree', ]
info = dict(zip(statvfs_fields, os.statvfs('/flash')))
print(info)
# {'files': 0, 'ffree': 0, 'bsize': 4096, 'bfree': 175, 'frsize': 4096, 'bavail': 175, 'blocks': 513}
print(info['bsize'] * info['bfree'])


print(gc.mem_free())
gc.collect()
print(gc.mem_free())
