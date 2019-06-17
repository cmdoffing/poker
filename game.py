from hand import *

class Game:

    def __init__(self, cardStr):
        """ Takes one or more lines of card strings and creates a game. """
        lines = cardStr.splitlines()
        self.hands = []
        for ln in lines:
            self.hands.append( Hand(ln) )
    
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

        bestFlushHand = self.bestFlush()
        if bestFlushHand:
            return bestFlushHand

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

    # I need to be able to compare the bestFive cards in order and to 
    # sort them in order. I also need to be able to select those hands
    # that are the same at the top, as those will be the winners.
    # Delete this function.!!!
    # ----------------------------------------------------
    def compareTwoHands(self, hand1, hand2 ):
        if   hand1.cards[0].rank > hand2.cards[0].rank:
            return hand1
        elif hand1.cards[0].rank < hand2.cards[0].rank:
            return hand2
        elif hand1.cards[1].rank > hand2.cards[1].rank:
            return hand1
        elif hand1.cards[1].rank < hand2.cards[1].rank:
            return hand2
        elif hand1.cards[2].rank > hand2.cards[2].rank:
            return hand1
        elif hand1.cards[2].rank < hand2.cards[2].rank:
            return hand2
        elif hand1.cards[3].rank > hand2.cards[3].rank:
            return hand1
        elif hand1.cards[3].rank < hand2.cards[3].rank:
            return hand2
        elif hand1.cards[4].rank > hand2.cards[4].rank:
            return hand1
        elif hand1.cards[4].rank < hand2.cards[4].rank:
            return hand2
        else:
            return hand1


    def displayGame(self):
        bh = self.bestHands()
        for h in bh:
            print( h.toString() )
        print('-------------------')
        remHands = [h for h in self.hands if h not in bh]
        for hand in remHands:
            print( hand.toString() )


if __name__ == "__main__":
    s = """4d QD 5s 4c th 3h qs
           3d 5d kh kc 8d jd 2d"""
    g = Game( s )
    g.hands.sort(reverse=True)
    g.displayGame()
