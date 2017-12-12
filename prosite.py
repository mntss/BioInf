def parseParam(paramString):
    st = paramString.index('(') + 1
    end = paramString.index(')')
    params = paramString[st:end].split(',')
    atMin = int(params[0])
    if len(params) == 1:
        return atMin, atMin
    else:
        atMax = int(params[1])
        return atMin, atMax


def parsePattern(lt):
    if lt == 'x':
        return lambda x: True
    elif lt.startswith('[') and lt.endswith(']'):
        return lambda x: x in lt[1:-1]
    elif lt.startswith('{') and lt.endswith('}'):
        return lambda x: x not in lt[1:-1]
    else:
        return lambda x: x == lt


def createMatcher(pattern):
    try:
        patternEnd = pattern.index('(')
        matcherPattern = pattern[:patternEnd]
        matcherParams = parseParam(pattern[patternEnd:])

    except ValueError:
        matcherPattern = pattern
        matcherParams = (1, 1)
    return Matcher(parsePattern(matcherPattern), *matcherParams)


class Matcher:
    def __init__(self, matchFunction, minMatches, maxMatches):
        self.matchFn = matchFunction
        self.next = None
        if minMatches is None:
            self.minMatches = 1
        else:
            self.minMatches = minMatches

        if maxMatches is None:
            self.maxMatches = self.minMatches
        else:
            self.maxMatches = maxMatches

    def setNext(self, nextMatcher):
        self.next = nextMatcher

    def getNext(self):
        if self.next is None:
            return LastMatcher()
        return self.next.copy()

    def copy(self):
        m = Matcher(self.matchFn, self.minMatches, self.maxMatches)
        m.setNext(self.next)
        return m

    def deepCopy(self):
        m = Matcher(self.matchFn, self.minMatches, self.maxMatches)
        if self.next is not None:
            m.setNext(self.next.deepCopy())
        return m

    def decMatches(self):
        self.minMatches = max(self.minMatches - 1, 0)
        self.maxMatches = max(self.maxMatches - 1, 0)

    def match(self, string, i=0):
        # print(string)
        if string == '':
            return []

        if not self.matchFn(string[0]):
            return []

        self.decMatches()

        if self.minMatches > 0:
            return self.match(string[1:], i + 1)

        if self.maxMatches > 0:
            return self.match(string[1:], i + 1) + self.getNext().match(string[1:], i + 1)
        else:
            return self.getNext().match(string[1:], i + 1)


class LastMatcher:
    def match(self, string, i):
        return [i]


pt = 'x(1,3)'

links = [createMatcher(p) for p in pt.split('-')]

for i in range(len(links) - 1):
    links[i].setNext(links[i + 1])

s = 'AAA'

result = []
for i in range(len(s)):
    matchPos = links[0].deepCopy().match(s[i:])
    result += [(i, m + i) for m in set(matchPos)]

print(result)
for a, b in result:
    print(s[a:b])

