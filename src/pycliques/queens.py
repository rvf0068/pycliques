def flatten(nested):
    try:
        for sublist in nested:
            for element in flatten(sublist):
                yield element
    except TypeError:
        yield nested


def conflict(state, nextX):
    nextY = len(state)
    for i in range(nextY):
        if abs(state[i] - nextX) in (0, nextY - i):
            return True
    return False


def queens(num=8, state=()):
    for pos in range(num):
        print("Trying {}".format(pos))
        if not conflict(state, pos):
            print("State: {}, pos: {}".format(state, pos))
            if len(state) == num-1:
                print("Hello! State: {}. Yielding: {}".format(state, (pos,)))
                yield (pos,)
            else:
                for result in queens(num, state + (pos,)):
                    print("yielding {}".format((pos,)+result))
                    yield (pos,) + result
