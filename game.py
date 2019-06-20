from hand import *

class Game:

    def __init__(self, cardStr):
        """ Takes one or more lines of card strings and creates a game. """
        lines = cardStr.splitlines()
        lines2 = [ln for ln in lines if ln.strip() != '']
        self.hands = []
        for ln in lines2:
            self.hands.append( Hand(ln) )

    def getWinningHands(self):
        """
        Sort all hands by hand rank and cards,
        then step thru the hands and compare side by side.
        Compare hand ranks.
        Or: just see if the next hand is equal to the first.
        If so, include hand2 in the output, else we are done.
        Step thru the sorted hands by index. When the equality test fails, 
        take a slice from the hand at index 0 to index 1 (if only one hand),
        or whatever index hand2 is at.
        Return a list of winning hands, usually only one.
        """
        self.hands.sort( reverse=True )
        result = self.hands[0:1]
        for h in self.hands[1:]:
            if self.handsAreEqual( result[0], h ):
                result.append( h )
        return result

    def handsAreEqual(self, hand1, hand2 ):
        return hand1.bestHandRank == hand2.bestHandRank and \
               hand1.cards[0] == hand2.cards[0] and \
               hand1.cards[1] == hand2.cards[1] and \
               hand1.cards[2] == hand2.cards[2] and \
               hand1.cards[3] == hand2.cards[3] and \
               hand1.cards[4] == hand2.cards[4]

    def getLosingHands(self):
        winners = self.getWinningHands()
        losing  = [hand for hand in self.hands if hand not in winners]
        return losing
