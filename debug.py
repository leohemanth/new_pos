def nothing():
    pass

try:
    from IPython.Shell import IPShellEmbed
    ipython = IPShellEmbed()
except:
    ipython = nothing

try:
    import ipdb
    idebug = ipdb.set_trace
except:
    idebug = nothing