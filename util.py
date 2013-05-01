from functools import wraps


def memoized(f):
    d = {}
    @wraps(f)
    def deco(*args):
        try:
            return d[args]
        except KeyError:
            ret = d[args] = f(*args)
            return ret
    return deco

def split_jid(jid):
    return jid.split('/', 1)

def userid_from_jid(jid):
    return split_jid(jid)[0]

def resource_from_jid(jid):
    return split_jid(jid)[1]
