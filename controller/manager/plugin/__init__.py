algorithm = None


def load_algorithm(name):
    global algorithm
    if name == "SimpleNearestApAlgorithm":
        import simple
        algorithm = simple.SimpleNearestApAlgorithm()
    elif name == "TrafficThresholdNearestApAlgorithm":
        import traffic
        algorithm = traffic.TrafficThresholdNearestApAlgorithm()
    else:
        algorithm = None
