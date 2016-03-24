def testEqual(actual, expected, feedback = ""):
    print "--",
    if type(expected) != type(actual):
        print "Failed test: %s\n\ttype of expected and actual don't match" % (feedback)
        return False
    if type(expected) == type(1):
        # they're integers, so check if exactly the same
        if actual == expected:
            print'Pass test: %s'  % (feedback)
            return True
    elif type(expected) == type(1.11):
        # a float is expected, so just check if it's very close, to allow for
        # rounding errors
        if abs(actual-expected) < 0.00001:
            print'Pass test: %s'  % (feedback)
            return True
    elif type(expected) == type([]):
        if len (expected) != len(actual):
            print "Failed test: %s\n\tLengths don't match" % (feedback)
            return False
        else:
            for (x, y) in zip(expected, actual):
                if x != y:
                    print "Failed test: %s\n\titems in expected and actual do not match" % (feedback)
                    return False
            print'Pass test: %s'  % (feedback)
            return True
    else:
        # check if they are equal
        if actual == expected:
            print'Pass test: %s'  % (feedback)
            return True
    print 'Failed test: %s\n\texpected:\t%s\n\tgot:\t\t%s' % (feedback, expected, actual)
    return False