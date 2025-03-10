import unittest


class TestBinaryConversion(unittest.TestCase):

    def setUp(self):
        class Converter:
            def convert_bin_to_decimal(self, list_of_bits):
                return sum(val * (2 ** idx) for idx, val in enumerate(reversed(list_of_bits)))

        self.converter = Converter()

    def test_empty_list(self):
        self.assertEqual(self.converter.convert_bin_to_decimal([]), 0)

    def test_single_bit_zero(self):
        self.assertEqual(self.converter.convert_bin_to_decimal([0]), 0)

    def test_single_bit_one(self):
        self.assertEqual(self.converter.convert_bin_to_decimal([1]), 1)

    def test_multiple_bits(self):
        self.assertEqual(self.converter.convert_bin_to_decimal([1, 0, 1, 1]), 11)

    def test_leading_zeros(self):
        self.assertEqual(self.converter.convert_bin_to_decimal([0, 0, 1, 1]), 3)

    def test_large_binary_number(self):
        self.assertEqual(self.converter.convert_bin_to_decimal([1, 1, 1, 1, 1, 1, 1, 1]), 255)

    def test_all_zeros(self):
        self.assertEqual(self.converter.convert_bin_to_decimal([0, 0, 0, 0]), 0)

    def test_mixed_bits(self):
        self.assertEqual(self.converter.convert_bin_to_decimal([1, 0, 0, 1, 1, 0]), 38)

if __name__ == '__main__':
    unittest.main()
