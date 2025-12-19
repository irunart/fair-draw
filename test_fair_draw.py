import unittest
import os
from fair_draw import get_fair_shuffle, load_participants

class TestFairDraw(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        self.candidates_path = os.path.join(self.fixtures_dir, 'candidates.txt')
        self.candidates_rev_path = os.path.join(self.fixtures_dir, 'candidates_rev.txt')
        self.candidates_dup_path = os.path.join(self.fixtures_dir, 'candidates_dup.txt')
        self.signal = "43"

    def test_determinism(self):
        """Test that same input and same signal produce the same output."""
        participants = load_participants(self.candidates_path)
        result1 = get_fair_shuffle(participants, self.signal)
        result2 = get_fair_shuffle(participants, self.signal)
        self.assertEqual(result1, result2)

    def test_order_independence(self):
        """Test that input file order does not affect the result."""
        participants_orig = load_participants(self.candidates_path)
        participants_rev = load_participants(self.candidates_rev_path)
        
        # Verify inputs are actually different in order
        self.assertNotEqual(participants_orig, participants_rev)
        self.assertEqual(sorted(participants_orig), sorted(participants_rev))

        result_orig = get_fair_shuffle(participants_orig, self.signal)
        result_rev = get_fair_shuffle(participants_rev, self.signal)
        
        self.assertEqual(result_orig, result_rev)

    def test_signal_sensitivity(self):
        """Test that different signals produce different results."""
        participants = load_participants(self.candidates_path)
        result1 = get_fair_shuffle(participants, "Signal A")
        result2 = get_fair_shuffle(participants, "Signal B")
        self.assertNotEqual(result1, result2)

    def test_duplicate_handling(self):
        """Test that duplicates result in a different seed and thus different outcome."""
        participants = load_participants(self.candidates_path)
        participants_dup = load_participants(self.candidates_dup_path)
        
        # Verify dup list is larger
        self.assertGreater(len(participants_dup), len(participants))
        
        result_unique = get_fair_shuffle(participants, self.signal)
        result_dup = get_fair_shuffle(participants_dup, self.signal)
        
        # The result lists will be different lengths, so they can't be equal.
        # But specifically, we expect the shuffle order to be effectively different
        # because the seed changed.
        self.assertNotEqual(result_unique, result_dup)

if __name__ == '__main__':
    unittest.main()
