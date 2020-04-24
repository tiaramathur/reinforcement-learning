# Tiara Mathur and Perry Healy
import random as random
import copy as copy


def main():
    environment = {}

    testfile = open("assignment2test.txt")        # read input file
    lines = testfile.read().splitlines()

    for line in lines:
        linesArr = line.split('/')				  # split input lines and store info
        s = linesArr[0]
        a = linesArr[1]
        newS = linesArr[2]
        p = linesArr[3]
        d = float(p)

        if (s not in environment):                # set up
            environment[s] = {}
            environment[s][a] = {}
        else:
            if (a not in environment[s]):
                environment[s][a] = {}

        environment[s][a][newS] = d

    # reward values
    # to be honest I do not know much about golf so
    # this is under the assumption that the following are in worst -> best position in order
    # and that same, over, and left are very similar
    rewards = {"Fairway": 0.1, "Ravine": 0.3, "Same": 0.5,
               "Over": 0.6, "Left": 0.7, "Close": 0.9, "In": 1.0}

    callFuncs(environment, rewards)

def callFuncs(environment, rewards):
    print("Model-Free Learning:")  # Model-Free Learning
    modelFree = mfFunc(environment, rewards)
    for s in modelFree:
        print("We are in state " + s + " and we can either:")
        for a in modelFree[s]:
            print("Aim " + a + ", for which the utility is: " +
                  str(round(modelFree[s][a], 2)))

    print("Model-Based Learning:")  # Model-Based Learning
    modelBased = mbFunc(environment, rewards)
    for s in modelBased:
        print("We are in state " + s + " and we can either:")
        for a in modelBased[s]:
            print("Aim " + a + ", for which the utility is " +
                  str(round(modelFree[s][a], 2)))


def randnummf(x):  # random values for model free
    rand_val = random.random()
    total = 0
    for a, b in x.items():
        total += b
        if (rand_val <= total):
            return a


def randnummb(x):  # random values for model based
    tSum = 0
    for a, b in x.items():
        tSum += b
    rand_val = random.random()*(float(tSum))
    tSum = 0

    for a, b in x.items():
        tSum += b
        if (rand_val <= tSum):
            return a


def mfFunc(environment, reward):
    q = {}
    for s in environment:                                            # set up
        if (s not in q):
            q[s] = {}
        for action in environment[s]:
            q[s][action] = 0

    for n in range(0, 1000):
        currS = random.choice(list(q.keys()))						 # random starting state

        while (currS != "In"):
            a = ""
            if (random.uniform(0, 1) < 0.5):							 # determine if random action is needed
                a = random.choice((list(environment[currS].keys()))) # assign random action
            else:
                currMax = -1						                # find action with maximum value
                for pa in q[currS]:
                    if (q[currS][pa] > currMax):
                        a = pa
                        currMax = q[currS][a]

            newS = randnummf(environment[currS][a])            # new state
            print("We decide to " + a + " and are now " + newS + ".")

            if (newS == "In"):
                currS = newS
                break

            if (currS == "In"):
                break
            else:
                max_q = -1

                for a in q[newS]:
                    if (q[newS][qa] > max_q):
                        max_q = q[newS][qa]

                q[currS][a] = q[currS][a] + 0.5 * \
                    (reward[newS] + 0.8 * max_q - q[currS][a]
                     )                    # results of action
                currS = newS

    return q  							# return value


def mbFunc(environment, reward):
    pastS = []                              # past states and actions
    pastA = {}
    t = copy.deepcopy(environment)			# copy so we do not alter the original
    q = {}
    r = {}

    for s in t:                             # set up
        for a in t[s]:
            for newS in t[s][a]:
                t[s][a][newS] = 0.00001
    for s in environment:
        r[s] = {}
        for a in environment[s]:
            r[s][a] = 0

    for s in environment:
        if s not in q:
            q[s] = {}
        for a in environment[s]:
            q[s][a] = 0

    for n in range(0, 1000):
        currS = random.choice(list(q.keys()))						# random starting state
        while (currS != "In"):
            a = ""
            if (random.uniform(0, 1) < 0.5):							 # determine if random action is needed
                a = random.choice((list(environment[currS].keys()))) # assign random action
            else:
                currMax = -1            						    # find action with maximum value
                for pa in q[currS]:	      				              # if we find a larger value, swap
                    if (q[currS][pa] > currMax):
                        a = pa
                        currMax = q[currS][a]

            newS = randnummf(environment[currS][a])       		     # new state

            if (newS == "In"):
                t[currS][a][newS] += 1
                currS = newS
                break

            if (currS == "In"):                                            # if we are in the hole
                break
            else:
                max_q = -1
                for qa in q[newS]:
                    if (q[newS][qa] > max_q):
                        max_q = q[newS][qa]

                r[currS][a] = ((0.5 * r[currS][a]) + (0.5*reward[newS])) # results of action
                q[currS][a] = (q[currS][a] + 0.5 *
                               (reward[newS] + 0.8*max_q - q[currS][a]))
                t[currS][a][newS] += 1

                for n in range(0, 200):
                    if (currS not in pastA):
                        pastA[currS] = []
                    pastA[currS].append(a)
                    pastS.append(currS)

                    randS = random.choice(pastS)						 # random state and random action
                    randA = random.choice(pastA[randS])
                    newS2 = randnummb(t[randS][randA])					 # pick the new state based on probabilities given

                    if (newS2 == "In"):                                    # if (we are now in the hole
                        break

                    max_q2 = -1
                    for qaction in q[newS2]:
                        if (q[newS2][qaction] > max_q2):
                            max_q2 = q[newS2][qaction]

                    q[randS][randA] = (q[randS][randA] + 0.5 *
                                       (r[randS][randA] + 0.8*max_q2 - q[randS][randA]))
                currS = newS
    mbResult(s, t)									    # print the results
    return q

def mbResult(s, t):										# function to print the results
    for s in t:
        print("When in state " + s + ":")
        for a in t[s]:
            print("When we decided to aim for (" + a + "...")
            for newS in t[s][a]:
                print("We were " + newS + " " +
                      str(int(round(t[s][a][newS]))) + " times.")


main()
