AP_DRIVER = None


def load():
    global AP_DRIVER
    if True:  # TODO add to config file
        import dummy
        AP_DRIVER = dummy.ApDriver()
    elif False:
        import upbtestbed
        AP_DRIVER = upbtestbed.ApDriver()
