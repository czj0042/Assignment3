from unittest import TestCase
import httplib
from urllib import urlencode


class ProbTest(TestCase):
    def setUp(self):
        self.inputDictionary = {}
        self.BX_URL = 'umphrda-bx-tcurve.mybluemix.net'
        self.BX_PORT = 80
        self.BX_PATH = '/prob?'
        self.ERROR = "error"

#----------------------------------------------------------------
#  Helper functions
#----------------------------------------------------------------
    def tearDown(self):
        self.inputDictionary = {}

    def setT(self, t):
        self.inputDictionary["t"] = t

    def setN(self, n):
        self.inputDictionary["n"] = n

    def setTails(self, tails):
        self.inputDictionary["tails"] = tails
        
    def prob(self, url, parm):
        try:
            theParm = urlencode(parm)
            theConnection = httplib.HTTPConnection(url, self.BX_PORT)
            theConnection.request("GET", self.BX_PATH + theParm)
            theStringResponse = theConnection.getresponse().read()
            return theStringResponse
        except Exception as e:
            return "error encountered during transaction"
        
#----------------------------------------------------------------   
#  Acceptance Tests
#----------------------------------------------------------------
#
#  100 prob
#    Desired level of confidence:  boundary value analysis
#    Input-output analysis   <type, range, presence, assumptions>
#        inputs:        n -> integer, .GE. 2 and .LE. 32; mandatory; unvalidated
#                       t -> float, .GE. 0, mandatory; unvalidated
#                       tails -> integer, {1,2}; optional; defaults to 1; unvalidated
#
#         outputs:    string representing a float, .GE. 0 and .GE. 1, mandatory; validated
#     Happy path
#         n:      nominal value of n        n=6     
#                 low bound of n            n=2
#                 high bound of n           n=32
#        t:        nominal value of t        t=1.89
#                low value of t            t=0
#        tails    value 1                    tails=1
#                value 2                    tails=2
#                missing                    
#        output:
#                The output is an interaction of t x tails x n:
#                    nominal n, nominal t, 1 tail
#                    low n, nbominal t, 1 tail
#                    high n, noninal t, 1 tail
#                    nominal n, nominal t, 2 tail
#                    low n, nbominal t, 2 tail
#                    high n, noninal t, 2 tail
#                    nominal n, nominal t, no tails
#                    low n, nbominal t, no tails
#                    high n, noninal t, no tails
#                    nominal n, low t, 1 tail
#                    nomina n, low t, 2 tails
#                    nominal n, low t, missing tails
#                The order of t x tails n:
#                    n, t, tails
#                    n, tails, t
#                    etc ...                 <-- please add tests
#
# Sad path
#    n:    above high bound n
#            below low bound n
#            missing n
#            non-integer n
#    others ?                                  <-- please add tests

# Happy Path
    def test100_010_ShouldCalculateProbWithNominalnNominalT1Tail(self):
        self.setN(7)
        self.setT(1.8946)
        self.setTails(1)
        result = self.prob(self.BX_URL, self.inputDictionary)
        self.assertAlmostEquals(float(result), 0.95, 3)
               
    def test100_020_ShouldCalculateProbWithLownNominalT1Tail(self):
        self.setN(2)
        self.setT(2.92)
        self.setTails(1)
        result = self.prob(self.BX_URL, self.inputDictionary)
        self.assertAlmostEquals(float(result), 0.95, 3)
        
# Sad path
    def test_100_910_ShouldProduceErrorOnAboveHighBoundN(self):
        self.setN(34)
        self.setT(2.92)
        self.setTails(1)
        result = self.prob(self.BX_URL, self.inputDictionary)
        self.assertEquals(result[len(self.ERROR)],self.ERROR)


