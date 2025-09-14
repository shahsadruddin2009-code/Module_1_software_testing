import unittest
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def calculate_discount(loyalty_points):
    """
    Returns the discount percentage based on loyalty points.
    - 1000 or more: 20%
    - 500 to 999: 10%
    - 0 to 499: 0%
    - Negative points: raises ValueError
    """
    if loyalty_points < 0:
        raise ValueError("Loyalty points cannot be negative")
    if loyalty_points >= 1000:
        return 20
    elif loyalty_points >= 500:
        return 10
    else:
        return 0
os.system('cls')
class TestCalculateDiscount(unittest.TestCase):
    """
    Unit tests for the calculate_discount function, which determines discount percentage based on loyalty points.
    The tests cover the following cases:
    - High loyalty points (1000+) providing 20% discount
    - Medium loyalty points (500-999) providing 10% discount
    - Low loyalty points (0-499) providing 0% discount
    - Boundary values between discount tiers (499/500 and 999/1000)
    - Negative loyalty points (edge case)
    Each test method validates that the calculate_discount function returns the expected
    discount percentage for various inputs within each range.
    """
    
    def test_high_loyalty_points(self):
        """Test that 1000 or more loyalty points gives 20% discount"""
        self.assertEqual(calculate_discount(1000), 20)
        self.assertEqual(calculate_discount(1500), 20)
    
    def test_medium_loyalty_points(self):
        """Test that 500-999 loyalty points gives 10% discount"""
        self.assertEqual(calculate_discount(500), 10)
        self.assertEqual(calculate_discount(750), 10)
        self.assertEqual(calculate_discount(999), 10)
    
    def test_low_loyalty_points(self):
        """Test that 0-499 loyalty points gives 0% discount"""
        self.assertEqual(calculate_discount(0), 0)
        self.assertEqual(calculate_discount(250), 0)
        self.assertEqual(calculate_discount(499), 0)
   
    def test_no_discount_for_low_points(self):
        """Test no discount for low loyalty points"""
        self.assertEqual(calculate_discount(200), 0)
        self.assertEqual(calculate_discount(50), 0)
        self.assertEqual(calculate_discount(100), 0)
    
    def test_bigdiscount_for_high_points(self): 
        """Test big discount for high loyalty points"""
        self.assertEqual(calculate_discount(1500), 20)
        self.assertEqual(calculate_discount(2000), 20)
        self.assertEqual(calculate_discount(1000), 20)

    def test_boundary_values(self):
        """Test boundary values between discount tiers"""
        self.assertEqual(calculate_discount(499), 0)
        self.assertEqual(calculate_discount(500), 10)
        self.assertEqual(calculate_discount(999), 10)
    
    def test_negative_points(self):
        """Test with negative loyalty points (edge case)"""
        with self.assertRaises(ValueError):
            calculate_discount(-100)
   
    def test_not_string(self):
        """Test with string input (edge case)"""
        with self.assertRaises(TypeError):
            calculate_discount("Shahzad")
        
if __name__ == '__main__':
    unittest.main()