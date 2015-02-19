import logging


algorithm_list = []
selected_algorithm = None


def load_algorithms(name_list, default_algorithm):
    global algorithm_list
    for name in name_list:
        if name == "SimpleNearestAp" or name == "SimpleNearestApAlgorithm":
            import simple
            algorithm_list.append(simple.SimpleNearestAp())
        elif name == "SimpleNearestApSwitchCooldown":
            import simple
            algorithm_list.append(simple.SimpleNearestApSwitchCooldown())
        elif name == "TrafficThresholdNearestAp":
            import traffic
            algorithm_list.append(traffic.TrafficThresholdNearestAp())
        elif name == "TrafficThresholdNearestApSwitchCooldown":
            import traffic
            algorithm_list.append(traffic.TrafficThresholdNearestApSwitchCooldown())
        elif name == "GreedyMinActiveApsFullCoverage":
            import bcgdemo
            algorithm_list.append(bcgdemo.GreedyMinActiveApsFullCoverage())
    switch_algorithm(default_algorithm)


def switch_algorithm(selected_name):
    global selected_algorithm
    selected_algorithm = selected_name
    logging.info("Selected algorithm: %s" % selected_name)
