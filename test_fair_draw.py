import unittest
import os
from fair_draw import get_fair_shuffle, load_participants, calculate_participant_hash

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

        res_orig, hash_orig, seed_orig = get_fair_shuffle(participants_orig, self.signal)
        res_rev, hash_rev, seed_rev = get_fair_shuffle(participants_rev, self.signal)
        
        self.assertEqual(res_orig, res_rev)
        self.assertEqual(hash_orig, hash_rev)
        self.assertEqual(seed_orig, seed_rev)
        self.assertIsInstance(seed_orig, int)

    def test_signal_sensitivity(self):
        """Test that different signals produce different results."""
        participants = load_participants(self.candidates_path)
        res1, hash1, seed1 = get_fair_shuffle(participants, "Signal A")
        res2, hash2, seed2 = get_fair_shuffle(participants, "Signal B")
        
        # Participant hash should be the same
        self.assertEqual(hash1, hash2)
        # Seed and result should be different
        self.assertNotEqual(seed1, seed2)
        self.assertNotEqual(res1, res2)
        self.assertIsInstance(seed1, int)

    def test_duplicate_handling(self):
        """Test that duplicates result in a different seed and thus different outcome."""
        participants = load_participants(self.candidates_path)
        participants_dup = load_participants(self.candidates_dup_path)
        
        # Verify dup list is larger
        self.assertGreater(len(participants_dup), len(participants))
        
        res_unique, hash_unique, seed_unique = get_fair_shuffle(participants, self.signal)
        res_dup, hash_dup, seed_dup = get_fair_shuffle(participants_dup, self.signal)
        
        # Participant hash should be different
        self.assertNotEqual(hash_unique, hash_dup)
        # Seed should be different
        self.assertNotEqual(seed_unique, seed_dup)
        # Result should be different
        self.assertNotEqual(res_unique, res_dup)
        self.assertIsInstance(seed_unique, int)

    def test_empty_salt(self):
        """Test that empty salt raises ValueError."""
        participants = load_participants(self.candidates_path)
        with self.assertRaises(ValueError):
            get_fair_shuffle(participants, "")
        with self.assertRaises(ValueError):
            get_fair_shuffle(participants, "   ")
        with self.assertRaises(ValueError):
            get_fair_shuffle(participants, None)

    def test_calculate_participant_hash(self):
        """Test that participant hash is calculated correctly and order-independently."""
        p1 = ["Alice", "Bob"]
        p2 = ["Bob", "Alice"]
        
        h1 = calculate_participant_hash(p1)
        h2 = calculate_participant_hash(p2)
        
        self.assertEqual(h1, h2)
        self.assertIsInstance(h1, str)
        self.assertEqual(len(h1), 64) # SHA-256 hex digest length

    def test_hash_collision_resistance(self):
        """Test that concatenation collisions are prevented."""
        # These would produce the same string if simply joined: "AliceBob"
        p1 = ["Alice", "Bob"]
        p2 = ["Ali", "ceBob"]
        
        h1 = calculate_participant_hash(p1)
        h2 = calculate_participant_hash(p2)
        
        self.assertNotEqual(h1, h2)

if __name__ == '__main__':
    unittest.main()
