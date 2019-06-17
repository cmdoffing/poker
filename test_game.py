from hand import *

class TestCard( unittest.TestCase ):
    def test_card( self ):
        c = Card("th")
        self.assertEqual( c.rank, "T")
        self.assertEqual( c.suit, "H")
        self.assertEqual( c.ordering, 10)
        self.assertFalse( c.isAce)

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


if __name__ == "__main__":
    unittest.main()
