import fabric.api as fab


def sudo(*args, **kwargs):
    with fab.quiet():
        return fab.sudo(*args, **kwargs)


def put(*args, **kwargs):
    with fab.quiet():
        return fab.put(*args, **kwargs)
