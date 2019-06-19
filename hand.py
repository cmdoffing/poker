import unittest

class Card:
    """ A single card """

    order = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
             "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

    def __init__(self, cardStr):
        self.rank = cardStr[0].upper()
        self.suit = cardStr[1].upper()
        self.ordering = self.order[ self.rank ]
        self.isAce = self.rank == "A"

    def toString(self):
        return self.rank + self.suit + " "
        

class Hand:
    """A poker hand"""

    def __init__(self, handStr):
        cardStrs = handStr.strip().split()
        self.cards = [Card(s) for s in cardStrs]
        self.cards.sort(key=lambda c: c.ordering, reverse=True)
        self.suited = sorted( self.cards, key=lambda c: c.suit)
        self.setBestHand()

    def toString(self):
        cards = self.bestCards + self.remainingCards( self.bestCards )
        result = ""
        for c in cards:
            result += c.toString()
        return result + ": " + self.bestHand

    def __lt__(self, hand2):
        """
        Pre: The bestCards are already arranged in high to low order of 
        significant cards. I.e., if the hand is 3-of-a-kind with 4D 4H 4C 8S 9H,
        the 4's will be placed first to give proper comparison of hands.
        Similar considerations apply to ful house's, pairs, 4-of-kinds, etc.
        """
        if   self.bestHandRank  > hand2.bestHandRank:
            return False
        elif self.bestHandRank  < hand2.bestHandRank:
            return True
        if   self.bestCards[0].ordering > hand2.bestCards[0].ordering:
            return False
        elif self.bestCards[0].ordering < hand2.bestCards[0].ordering:
            return True
        elif self.bestCards[1].ordering > hand2.bestCards[1].ordering:
            return False
        elif self.bestCards[1].ordering < hand2.bestCards[1].ordering:
            return True
        elif self.bestCards[2].ordering > hand2.bestCards[2].ordering:
            return False
        elif self.bestCards[2].ordering < hand2.bestCards[2].ordering:
            return True
        elif self.bestCards[3].ordering > hand2.bestCards[3].ordering:
            return False
        elif self.bestCards[3].ordering < hand2.bestCards[3].ordering:
            return True
        elif self.bestCards[4].ordering > hand2.bestCards[4].ordering:
            return False
        elif self.bestCards[4].ordering < hand2.bestCards[4].ordering:
            return True
        else:
            return False

    def hasOrderingCard(self, order):
        """
        Check cards to see if a card with the given ordering is present. 
        Use this to properly check for runs, even in the presence of pairs.
        """
        for c in self.cards:
            if c.ordering == order:
                return c
        return False

    def hasLowStraight(self):
        """ Get a low straight (Ace 2 3 4 5) if resent. """
        c1 = self.hasOrderingCard( 14 )
        c2 = self.hasOrderingCard( 2 )
        c3 = self.hasOrderingCard( 3 )
        c4 = self.hasOrderingCard( 4 )
        c5 = self.hasOrderingCard( 5 )
        if c1 and c2 and c3 and c4 and c5:
            return [c5, c4, c3, c2, c1]
        else:
            return []


    def cardsHaveStraight(self, candidateCards):
        lastOrdering = candidateCards[0].ordering
        straightCards = [candidateCards[0]]
        count = 1
        for c in candidateCards[1:]:
            nextOrderedCard = self.hasOrderingCard( lastOrdering - 1 )
            if nextOrderedCard:
                straightCards.append( nextOrderedCard )
                lastOrdering = lastOrdering - 1
                count += 1
                if count == 5:
                    return straightCards
            else:
                break
        return []


    def handHasStraight(self):
        lowStraight = self.hasLowStraight()
        if lowStraight:
            return lowStraight

        high1 = self.cards
        straight = self.cardsHaveStraight(high1)
        if straight:
            return straight
        high2 = self.cards[1:]
        straight = self.cardsHaveStraight(high2)
        if straight:
            return straight
        high3 = self.cards[2:]
        straight = self.cardsHaveStraight(high3)
        if straight:
            return straight
        return []


    def haveSameSuit(self, crds):
        """Takes 5 cards sorted by suit and returns True if all have the same suit. """
        for i in range(4):
            if crds[i].suit != crds[i+1].suit:
                return False
        return True

    def isStraightFlush(self, crds):
        """ Takes 5 crds and returns True iff they are a straight flush. """
        return self.haveSameSuit( crds ) and self.cardsHaveStraight( crds )

    def straightFlushCards( self ):
        crds = self.cards[0:5]
        if self.isStraightFlush(crds):
            return crds
        crds = self.cards[1:6]
        if self.isStraightFlush(crds):
            return crds
        crds = self.cards[2:7]
        if self.isStraightFlush(crds):
            return crds
        return []

    def isFourOfKind(self, crds):
        """ Takes 4 cards and returns True if all 4 have the same rank. """
        return crds[0].rank == crds[1].rank == crds[2].rank == crds[3].rank

    def handHasFourOfKind(self):
        first4  = self.cards[0:4]
        if self.isFourOfKind( first4 ):
            return first4
        second4 = self.cards[1:5]
        if self.isFourOfKind( second4 ):
            return second4
        third4  = self.cards[2:6]
        if self.isFourOfKind( third4 ):
            return third4
        fourth4 = self.cards[3:7]
        if self.isFourOfKind( fourth4 ):
            return fourth4
        return []

    def handHasFlush(self):
        first5 = self.suited[0:5]
        if self.haveSameSuit(first5):
            return first5
        second5 = self.suited[1:6]
        if self.haveSameSuit(second5):
            return second5
        third5 = self.suited[2:7]
        if self.haveSameSuit(third5):
            return third5
        return []

    def handHasThreeOfKind(self):
        for i in range(5):
            if self.cards[i].rank == self.cards[i+1].rank == self.cards[i+2].rank:
                return self.cards[i:i+3]
        return []

    def cardsHavePair(self, crds):
        for i in range( len(crds) - 1 ):
            if crds[i].rank == crds[i+1].rank:
                return crds[i:i+2]
        return []

    def handHasTwoPair(self):
        pair1 = self.cardsHavePair(self.cards)
        if pair1:
            remCards = self.remainingCards(pair1)
            pair2 = self.cardsHavePair(remCards)
            if pair2:
                return pair1 + pair2
        return []

    def handHasFullHouse(self):
        """ 
        Place the three-of-a-kind at the 
        front to simplify later processing.
        """
        threeOfKind = self.handHasThreeOfKind()
        if threeOfKind:
            remCards = self.remainingCards(threeOfKind)
            pair = self.cardsHavePair(remCards)
            if pair:
                return threeOfKind + pair
        return []

    def remainingCards(self, crds):
        """ 
        Subtract the cards in the crds parameter from 
        all the hand's cards in self.cards.
        """
        return [card for card in self.cards if card not in crds]

    def best5(self, crds):
        """ 
        Takes less than 5 cards and returns the best 5 card hand. 
        PLace the given cards in front and the rest of the cards behind.
        This will simplify comparing hands.
        """
        numCardsToGet = 5 - len(crds)
        rest = self.remainingCards(crds)
        newCards = rest[ 0:numCardsToGet ]
        return crds + newCards

    def setBestHand(self):
        if len(self.cards) < 7:   # or 'pass' in handStr:
            self.bestHand = "Pass"
            self.bestHandRank = 0
            self.bestCards = self.cards[0:5]
            return
        sfc = self.straightFlushCards()
        if sfc:
            self.bestHand = "Straight Flush"
            self.bestHandRank = 9
            self.bestCards = sfc
        elif self.handHasFourOfKind():
            self.bestHand = "Four Of Kind"
            self.bestHandRank = 8
            fok = self.handHasFourOfKind()
            self.bestCards = self.best5(fok)
        elif self.handHasFullHouse():
            self.bestHand = "Full House"
            self.bestHandRank = 7
            self.bestCards = self.handHasFullHouse()
        elif self.handHasFlush():
            self.bestHand = "Flush"
            self.bestHandRank = 6
            self.bestCards = self.handHasFlush()
        elif self.handHasStraight():
            self.bestHand = "Straight"
            self.bestHandRank = 5
            self.bestCards = self.handHasStraight()
        elif self.handHasThreeOfKind():
            self.bestHand = "Three Of Kind"
            self.bestHandRank = 4
            threeOfKind = self.handHasThreeOfKind()
            self.bestCards = self.best5(threeOfKind)
        elif self.handHasTwoPair():
            self.bestHand = "Two Pair"
            self.bestHandRank = 3
            twoPair = self.handHasTwoPair()
            self.bestCards = self.best5(twoPair)
        elif self.cardsHavePair(self.cards):
            self.bestHand = "One Pair"
            self.bestHandRank = 2
            onePair = self.cardsHavePair(self.cards)
            self.bestCards = self.best5(onePair)
        else:
            # Only a high card hand is left.
            self.bestHand = "High Cards"
            self.bestHandRank = 1
            self.bestCards = self.best5([])

if __name__ == "__main__":
    h = Hand( "4d QD 5s 4c th 3h qs" )
    h2 = Hand( "3d 5d kh kc 8d jd 2d" )
    print( h.toString() )
    comp = h.__lt__( h2 )
    print( comp )
