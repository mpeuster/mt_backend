algorithm = None


def load_algorithm(name):
    global algorithm
    if name == "SimpleNearestAp" or name == "SimpleNearestApAlgorithm":
        import simple
        algorithm = simple.SimpleNearestAp()
    elif name == "SimpleNearestApSwitchCooldown":
        import simple
        algorithm = simple.SimpleNearestApSwitchCooldown()
    elif name == "TrafficThresholdNearestAp":
        import traffic
        algorithm = traffic.TrafficThresholdNearestAp()
    elif name == "TrafficThresholdNearestApSwitchCooldown":
        import traffic
        algorithm = traffic.TrafficThresholdNearestApSwitchCooldown()
    elif name == "GreedyMinActiveApsFullCoverage":
        import bcgdemo
        algorithm = bcgdemo.GreedyMinActiveApsFullCoverage()
    else:
        algorithm = None
