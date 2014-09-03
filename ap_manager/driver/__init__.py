AP_DRIVER = None


def load(driver_name="dummy"):
    global AP_DRIVER
    if driver_name == "dummy":
        import dummy
        AP_DRIVER = dummy.ApDriver()
    elif driver_name == "upb":
        import upbtestbed
        AP_DRIVER = upbtestbed.ApDriver()
