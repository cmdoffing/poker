from hand import Hand, Card
from game import Game
import unittest

class TestCard( unittest.TestCase ):
    def test_card( self ):
        c = Card("th")
        self.assertEqual( c.rank, "T")
        self.assertEqual( c.suit, "H")
        self.assertEqual( c.ordering, 10)

class TestHand( unittest.TestCase ):
    def test_hand(self):
        h = Hand( "4d QD 5s 9c th 3h qs")
        self.assertEqual( len(h.cards), 7)
        self.assertEqual( h.cards[0].rank, "Q")
        self.assertEqual( h.cards[2].rank, "T")

    def test_hand_highCards(self):
        h = Hand( "4d KD 5s 9c th 3h qs")
        self.assertEqual( h.bestHandRank, 1 )
        self.assertEqual( h.bestHand, "High Cards")

    def test_hand_1pair(self):
        h = Hand( "4d QD 5s 9c th 3h qs")
        self.assertEqual( h.bestHandRank, 2 )
        self.assertEqual( h.bestHand, "One Pair")

    def test_hand_2pair(self):
        h = Hand( "4d QD 5s 4c th 3h qs")
        self.assertEqual( h.bestHandRank, 3 )
        self.assertEqual( h.bestHand, "Two Pair")

    def test_hand_threeOfKind(self):
        h = Hand( "4d QD 5s Qc th 3h qs")
        self.assertEqual( h.bestHandRank, 4 )
        self.assertEqual( h.bestHand, "Three Of Kind")

    def test_hand_straight(self):
        h = Hand( "4d 7D 5s 4c th 3h 6s")
        self.assertEqual( h.bestHandRank, 5 )
        self.assertEqual( h.bestHand, "Straight")

    def test_hand_flush(self):
        h = Hand( "4d 7D 5s 4s tD 3d 8d")
        self.assertEqual( h.bestHandRank, 6 )
        self.assertEqual( h.bestHand, "Flush")

    def test_hand_fullHouse(self):
        h = Hand( "4d QD 3s Qc th 3h qs")
        self.assertEqual( h.bestHandRank, 7 )
        self.assertEqual( h.bestHand, "Full House")

    def test_hand_fourOfKind(self):
        h = Hand( "4d QD 3s Qc 3h qh qs")
        self.assertEqual( h.bestHandRank, 8 )
        self.assertEqual( h.bestHand, "Four Of Kind")

    def test_hand_straightFlush(self):
        h = Hand( "4d 5d 3d Qc 6d qh 7d")
        self.assertEqual( h.bestHandRank, 9 )
        self.assertEqual( h.bestHand, "Straight Flush")


class TestGame( unittest.TestCase ):
    def testStraightFlushPass(self):
        s = """
            KS ts js 8c qs 2c 9s
            5s ts js 8s qs 2c
            """
        g = Game( s )
        winners = g.getWinningHands()
        losers  = g.getLosingHands()
        self.assertEqual( winners[0].bestHand, 'Straight Flush' )
        self.assertEqual( winners[0].bestHandRank, 9 )
        self.assertEqual( losers[0].bestHand, 'Pass' )
        self.assertEqual( losers[0].bestHandRank, 0 )

    def testStraightFlush(self):
        s = """KS ts js 8c qs 2c 9s
               5d ts js 8s qs 2c 9s
               5d 4d 3d 2d ad 5h ts
               5d 4d 3d 2h 2s 2d ad"""
        g = Game( s )
        winners = g.getWinningHands()
        losers  = g.getLosingHands()
        self.assertEqual( winners[0].bestHand, 'Straight Flush' )
        self.assertEqual( winners[0].bestHandRank, 9 )
        self.assertEqual( losers[0].bestHand, 'Straight Flush' )
        self.assertEqual( losers[0].bestHandRank, 9 )
        self.assertEqual( losers[1].bestHandRank, 9 )
        self.assertEqual( losers[2].bestHandRank, 9 )

    def test4OfKind(self):
        s = """KS 9d kh kc 7d Kd 2d
               qS 8d qh qc 8d qd 2d"""
        g = Game( s )
        winners = g.getWinningHands()
        losers  = g.getLosingHands()
        self.assertEqual( winners[0].bestHand, 'Four Of Kind' )
        self.assertEqual( winners[0].bestHandRank, 8 )
        self.assertEqual( losers[0].bestHand, 'Four Of Kind' )
        self.assertEqual( losers[0].bestHandRank, 8 )

    def testStraight(self):
        s = """3c 9d kh 6c 5d 4s 2d
               3c 9d kh ac 5d 4s 2d
            """
        g = Game( s )
        winners = g.getWinningHands()
        losers  = g.getLosingHands()
        self.assertEqual( winners[0].bestHand, 'Straight' )
        self.assertEqual( winners[0].bestHandRank, 5 )
        self.assertEqual( losers[0].bestHand, 'Straight' )
        self.assertEqual( losers[0].bestHandRank, 5 )

    def testHighCards(self):
        s = """3c 9d kh qc 7d js 2d
               3c 9d kh qc 8d js 2d"""
        g = Game( s )
        winners = g.getWinningHands()
        losers  = g.getLosingHands()
        self.assertEqual( winners[0].bestHand, 'High Cards' )
        self.assertEqual( winners[0].bestHandRank, 1 )
        self.assertEqual( losers[0].bestHand, 'High Cards' )
        self.assertEqual( losers[0].bestHandRank, 1 )

    def testThreeOfKind(self):
        s = """3c 9d kh kc 7d Kd 2d
               3c 9d kh kc 8d Kd 2d"""
        g = Game( s )
        winners = g.getWinningHands()
        losers  = g.getLosingHands()
        self.assertEqual( winners[0].bestHand, 'Three Of Kind' )
        self.assertEqual( winners[0].bestHandRank, 4 )
        self.assertEqual( losers[0].bestHand, 'Three Of Kind' )
        self.assertEqual( losers[0].bestHandRank, 4 )

    def testBigGame(self):
        s = """
           6d QD 5s 4c th 3h qs
           4d QD 5s 4c th 3h qs
           4d QD 5s 4c 4h 3h qs
           4d QD 5s 2c 4h QH qs
           3d 7d kh kc 8d jd 2d
           3c 7d kh kc 8d Kd 2d
           3d 5d kh kc 8d jd 2d
           """
        g = Game( s )
        winners = g.getWinningHands()
        losers  = g.getLosingHands()
        self.assertEqual( winners[0].bestHand, 'Full House' )
        self.assertEqual( winners[0].bestHandRank, 7 )
        self.assertEqual( losers[0].bestHand, 'Full House' )
        self.assertEqual( losers[0].bestHandRank, 7 )
        self.assertEqual( losers[1].bestHandRank, 6 )
        self.assertEqual( losers[2].bestHandRank, 6 )
        self.assertEqual( losers[3].bestHandRank, 4 )
        self.assertEqual( losers[4].bestHandRank, 3 )
        self.assertEqual( losers[5].bestHandRank, 2 )

if __name__ == "__main__":
    unittest.main()
