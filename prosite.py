class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def isNaN(num):
    return num != num

class PrositeMatcher:        
    def __init__(self, pattern):
        def matcher(lt):
            if lt == 'x':
                return lambda x: True
            elif lt.startswith('[') and lt.endswith(']'):
                return lambda x: x in lt[1:-1]
            elif lt.startswith('{') and lt.endswith('}'):
                return lambda x: x not in lt[1:-1]
            else:
                return lambda x: x == lt
        
        parts = pattern.split('-')
        self.matchers = [matcher(x) for x in parts]

        
    def match(self, string):
        def matchSt(st, matchers=self.matchers):
#             print(st)
            if not matchers: # wszystkie matchery zwróciły true, znaleziono wzrór
                return True
            elif st == '':   # nie ma czego sprawdzac
                return False
            elif matchers[0](st[0]):  # symbol na obecnej pozycji pasuje do wzoru, sprawdz nastepny
                return matchSt(st[1:], matchers[1:])
            else:                     #symbol nie pasuje do wzoru, nie ma dopasowania
                return False

        if string == '':
            return - float('NaN')
        elif matchSt(string):   #sprawdz czy string pasuje do wzroru zaczynajac od obecnej pozycji
            return 0
        else:
            return 1 + self.match(string[1:]) #jesli nie pasuje, to sprawdz nastepna
        
    def highlightMatch(self, string):
        match_start = self.match(string)
        if isNaN(match_start):
            print(string)
            return
            
        match_end = match_start + len(self.matchers)
        output_string = string[:match_start] + bcolors.OKGREEN + string[match_start:match_end] + bcolors.ENDC + string[match_end:]
        print(output_string)

PrositeMatcher('A-x-x-[QWERD]-C-{PDOA}-x-O').highlightMatch('POQAFSFSAQQDCKDOA')