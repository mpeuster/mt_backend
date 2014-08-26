algorithm = None


def load_algorithm(name):
    global algorithm
    if name == "SimpleNearestApAlgorithm":
        import simple
        algorithm = simple.SimpleNearestApAlgorithm()
    else:
        algorithm = None
