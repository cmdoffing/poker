from hand import *

class Game:

    def __init__(self, cardStr):
        """ Takes one or more lines of card strings and creates a game. """
        lines = cardStr.splitlines()
        self.hands = []
        for ln in lines:
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

    
    def sortHandsByRank(self):
        return self.hands.sort( key=lambda h: h.bestHandRank, reverse=True )

    def bestHands(self):
        self.sortHandsByRank()
        topHandRank = self.hands[0].bestHandRank
        # Filter out all hands that do not have topHandRank
        topRankHands = [h for h in self.hands if h.bestHandRank == topHandRank]
        if len(topRankHands) <= 1:
            # There is only one hand with the top rank, so we're done
            return topRankHands
        
        # There is more than one hand with the bestHandRank.
        sfHands = self.bestStraightFlush()
        if sfHands:
            return sfHands

        fourOfKindHands = self.bestFourOfKind()
        if fourOfKindHands:
            return fourOfKindHands

        fullHouse = self.bestFullHouse()
        if fullHouse:
            return fullHouse

        #bestFlushHand = self.bestFlush()
        #if bestFlushHand:
        #    return bestFlushHand

        straight = self.bestStraight()
        if straight:
            return straight

        three = self.bestThreeOfKind()
        if three:
            return three

        return self.hands[0:1]   # Only a high cards hand is left


    def bestStraightFlush(self):
        """ 
        Pre: self.hands have been sorted in descending order of hand rank.
        There can only be one best straight flush. No ties are possible.
        """
        sfHands = [h for h in self.hands if h.bestHandRank == 9]
        if sfHands:
            sortedHands = sfHands.sort( key=lambda h: h.cards[0].ordering, reverse=True )
            return sortedHands[0:1]
        else:
            return []

    def bestFourOfKind(self):
        """ There can be at most 2 4-of-a-kind hands. """
        hands = [h for h in self.hands if h.bestHandRank == 8]
        if hands:
            sortedHands = hands.sort( key=lambda h: h.cards[0].ordering, reverse=True )
            return sortedHands[0:1]
        else:
            return []

    def bestFullHouse(self):
        hands = [h for h in self.hands if h.bestHandRank == 7]
        if hands:
            sortedHands = hands.sort( key=lambda h: h.cards[0].ordering, reverse=True )
            return sortedHands[0:1]
        else:
            return []

    def bestFlush(self):
        flushHands = [h for h in self.hands if h.bestHandRank == 6]
        if flushHands:
            sortedHands = flushHands.sort( key=lambda h: h.cards[0].ordering, reverse=True )
            return sortedHands[0:1]
        else:
            return []

    def bestStraight(self):
        hands = [h for h in self.hands if h.bestHandRank == 5]
        if hands:
            sortedHands = hands.sort( key=lambda h: h.cards[0].ordering, reverse=True )
            return sortedHands[0:1]
        else:
            return []

    def bestThreeOfKind(self):
        hands = [h for h in self.hands if h.bestHandRank == 4]
        if hands:
            sortedHands = hands.sort( key=lambda h: h.cards[0].ordering, reverse=True )
            return sortedHands[0:1]
        else:
            return []


    def displayGame(self):
        bh = self.bestHands()
        for h in bh:
            print( h.toString() )
        print('-------------------')
        remHands = [h for h in self.hands if h not in bh]
        for hand in remHands:
            print( hand.toString() )


if __name__ == "__main__":
    s = """6d QD 5s 4c th 3h qs
           4d QD 5s 4c th 3h qs
           4d QD 5s 4c 4h 3h qs
           3d 7d kh kc 8d jd 2d
           3d 5d kh kc 8d jd 2d"""
    g = Game( s )
    winners = g.getWinningHands()
    for h in winners:
        print(h.toString())
    print("----------------------------------")
    losing = g.getLosingHands()
    for h in losing:
        print(h.toString())
    print("----------------------------------")
    g.displayGame()
