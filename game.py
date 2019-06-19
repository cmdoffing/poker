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


if __name__ == "__main__":
    s1 = """
           6d QD 5s 4c th 3h qs
           4d QD 5s 4c th 3h qs
           4d QD 5s 4c 4h 3h qs
           4d QD 5s 2c 4h QH qs
           3d 7d kh kc 8d jd 2d
           3c 7d kh kc 8d Kd 2d
           3d 5d kh kc 8d jd 2d
        """

    s2 = """3c 9d kh kc 7d Kd 2d
            3c 9d kh kc 8d Kd 2d"""
    s3 = """3c 9d kh qc 7d js 2d
            3c 9d kh qc 8d js 2d"""
    s4 = """3c 9d kh 6c 5d 4s 2d
            3c 9d kh ac 5d 4s 2d"""
    s5 = """KS 9d kh kc 7d Kd 2d
            qS 8d qh qc 8d qd 2d"""
    s6 = """KS ts js 8c qs 2c 9s
            5d ts js 8s qs 2c 9s
            5d 4d 3d 2d ad 5h ts"""
    s7 = """
         KS ts js 8c qs 2c 9s
         5s ts js 8s qs 2c
         """
    g = Game( s6 )
    print("----------- Winning ------------")
    winners = g.getWinningHands()
    for h in winners:
        print(h.toString())
    print("----------- Losing -------------")
    losing = g.getLosingHands()
    for h in losing:
        print(h.toString())
