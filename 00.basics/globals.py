
def var_create(var):
    if var not in globals():
        globals()[var] = 1

def var_remove(var):
    if var in globals():
        globals().pop(var)

start('global_var')

global_var = global_var + 1

print(global_var)

# It will be there until you turn it off (shutdown or restart)
# close()

print(global_var)
