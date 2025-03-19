import unittest
import numpy as np
from benchmark_functions import Hypersphere  # Assuming this is defined correctly

class TestHypersphere(unittest.TestCase):

    def setUp(self):
        """Initialize a Hypersphere function instance before each test."""
        self.hypersphere = Hypersphere(n_dimensions=3)  # Using 3D example

    def test_evaluate(self):
        """Test _evaluate() function with a sample input."""
        point = [1.0, 2.0, 3.0]
        result = self.hypersphere._evaluate(point)
        expected = 1.0**2 + 2.0**2 + 3.0**2  # Should be 14.0
        self.assertEqual(result, expected)

    def test_evaluate_zero_input(self):
        """Test _evaluate() with zero vector (should return 0)."""
        point = [0.0, 0.0, 0.0]
        result = self.hypersphere._evaluate(point)
        self.assertEqual(result, 0.0)

    def test_evaluate_negative_values(self):
        """Test _evaluate() with negative values (should still return positive result)."""
        point = [-1.0, -2.0, -3.0]
        result = self.hypersphere._evaluate(point)
        expected = (-1.0)**2 + (-2.0)**2 + (-3.0)**2  # Should be 14.0
        self.assertEqual(result, expected)

    def test_evaluate_gradient(self):
        """Test _evaluate_gradient() correctness."""
        point = [1.0, 2.0, 3.0]
        result = self.hypersphere._evaluate_gradient(point)
        expected = [2*x for x in point]  # Should be [2.0, 4.0, 6.0]
        self.assertEqual(result, expected)

    def test_evaluate_gradient_zero(self):
        """Test gradient at zero (should return all zeros)."""
        point = [0.0, 0.0, 0.0]
        result = self.hypersphere._evaluate_gradient(point)
        expected = [0.0, 0.0, 0.0]
        self.assertEqual(result, expected)

    def test_evaluate_hessian(self):
        """Test _evaluate_hessian() returns correct diagonal Hessian matrix."""
        point = [1.0, 2.0, 3.0]  # Input doesn't change Hessian, it's always the same
        result = self.hypersphere._evaluate_hessian(point)

        expected = np.identity(3) * 2.0  # Should be 3x3 identity matrix scaled by 2
        np.testing.assert_array_equal(result, expected)

if __name__ == "__main__":
    unittest.main()
