def parseParam(paramString):    # odczyt minimalnej i maksymalnej liczby dopasowań - e(i,j), e(i) jest rozumiane jako e(i,i)
    st = paramString.index('(') + 1
    end = paramString.index(')')
    params = paramString[st:end].split(',')
    atMin = int(params[0])
    if len(params) == 1:
        return atMin, atMin
    else:
        atMax = int(params[1])
        return atMin, atMax


def parsePattern(lt):   # przetłumaczenie części wzoru np. [SAD], zwracamy funkcję która posłuży do sprawdzenia czy dopasowanie jest legalne
    if lt == 'x':
        return lambda x: True
    elif lt.startswith('[') and lt.endswith(']'):
        return lambda x: x in lt[1:-1]
    elif lt.startswith('{') and lt.endswith('}'):
        return lambda x: x not in lt[1:-1]
    else:
        return lambda x: x == lt


def createMatcher(pattern): # stworzenie pojedynczego matchera np. dla {RTK}(2)
    try:
        patternEnd = pattern.index('(')
        matcherPattern = pattern[:patternEnd]
        matcherParams = parseParam(pattern[patternEnd:])

    except ValueError:
        matcherPattern = pattern
        matcherParams = (1, 1)      # brak nawiasów okrągłych, przyjmujemy wartości domyślne
    return Matcher(parsePattern(matcherPattern), *matcherParams)


class Matcher:
    def __init__(self, matchFunction, minMatches, maxMatches):
        self.matchFn = matchFunction
        self.next = None
        self.minMatches = minMatches
        self.maxMatches = maxMatches

    def setNext(self, nextMatcher):
        self.next = nextMatcher

    def getNext(self):
        if self.next is None: # jeżeli obecny Matcher jest ostatni to jako kolejny zwracamy specjalny obiekt
            return LastMatcher()
        return self.next.copy() # kopiujemy następny matcher żeby kolejne ścieżki nie wpływały na siebie nawzajem

    def copy(self):
        m = Matcher(self.matchFn, self.minMatches, self.maxMatches)
        m.setNext(self.next)
        return m

    def deepCopy(self): # kopia całego łańcucha
        m = Matcher(self.matchFn, self.minMatches, self.maxMatches)
        if self.next is not None:
            m.setNext(self.next.deepCopy())
        return m

    def decMatches(self):
        self.minMatches = max(self.minMatches - 1, 0)
        self.maxMatches = max(self.maxMatches - 1, 0)

    def match(self, string, i=0):
        if string == '':    # nie ma dopasowania dla pustej sekwencji
            return []

        if not self.matchFn(string[0]): # jeżeli element nie pasuje do wzoru to wychodzimy z funkcji
            return []

        self.decMatches() # zmniejszamy liczbę wymaganych dopasowań dla obecnego matchera

        if self.minMatches > 0:                     # jeżeli nie dopasowaliśmy jeszcze minimalnej liczby elementów dla 
            return self.match(string[1:], i + 1)    # matchera to powtarzamy krok dla następnego elementu w sekwencji
            

        if self.maxMatches > 0:     #rozwidlenie, sumujemy dopasowania z uwzględnieniem opcjonalnego elementu z dopasowaniem bez niego
            return self.match(string[1:], i + 1) + self.getNext().match(string[1:], i + 1)
        else:
            return self.getNext().match(string[1:], i + 1)  # przejście do następnego elementu


class LastMatcher:                  # występuje po ostatnim matcherze w wzorze, zwraca licznik który był inkrementowany 
    def match(self, string, i):     # po każdym dopasowaniu uzyskując długośc dopasowania
        return [i]  


def findMatches(pattern, sequence):
    links = [createMatcher(p) for p in pattern.split('-')]  # tworzymy po jednym matcherze dla każdego z elementów wzoru
    for i in range(len(links) - 1):
        links[i].setNext(links[i + 1])                      # łączymy matchery w łańcuch
    result = []
    for i in range(len(sequence)):                          # po każdym przebiegu pętli, kolejny element sekwencji wybierany jest jako startowy
        matchPos = links[0].deepCopy().match(sequence[i:])  # uzyskujemy długości możliwych dopasowań zaczynając z obecnej pozycji
        result += [(i, m + i) for m in set(matchPos)]       # używamy set() aby wyelminowac powtorzenia i zwracamy pary (poczatek, koniec) dopasowania
    return result


pt = 'x(1,3)'
s = 'AAAA'

for a, b in findMatches(pt, s):
    print((a, b))
    print(s[a:b])

