algorithm = None


def load_algorithm(name):
    global algorithm
    if name == "SimpleNearestAp" or name == "SimpleNearestApAlgorithm":
        import simple
        algorithm = simple.SimpleNearestAp()
    elif name == "SimpleNearestApSwtichCooldown":
        import simple
        algorithm = simple.SimpleNearestApSwtichCooldown()
    elif name == "TrafficThresholdNearestAp":
        import traffic
        algorithm = traffic.TrafficThresholdNearestAp()
    elif name == "TrafficThresholdNearestApSwtichCooldown":
        import traffic
        algorithm = traffic.TrafficThresholdNearestApSwtichCooldown()
    else:
        algorithm = None
