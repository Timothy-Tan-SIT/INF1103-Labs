import unittest
from unittest.mock import patch

from input_helpers import (
    get_non_negative_float, get_non_negative_int, get_positive_float, get_positive_int
)
from tests.helpers import capture_output


def run_with_inputs(function, inputs: list[str]):  # type: ignore[no-untyped-def]
    # Feeds the given inputs to input() one by one and returns (result, printed text).
    with patch("builtins.input", side_effect=inputs):
        return capture_output(function)


class TestGetPositiveFloat(unittest.TestCase):
    def test_lab_scenario_abc_then_minus_five_then_valid(self) -> None:
        result, output = run_with_inputs(lambda: get_positive_float("Price: "),
                                         ["abc", "-5", "12.50"])
        self.assertEqual(result, 12.5)
        self.assertEqual(output.splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_zero_is_rejected(self) -> None:
        result, output = run_with_inputs(lambda: get_positive_float("Price: "), ["0", "3"])
        self.assertEqual(result, 3.0)
        self.assertIn("greater than zero", output)

    def test_nan_and_infinity_are_rejected(self) -> None:
        result, output = run_with_inputs(lambda: get_positive_float("Price: "),
                                         ["nan", "inf", "7"])
        self.assertEqual(result, 7.0)
        self.assertEqual(output.count("Please enter a valid number"), 2)

    def test_blank_input_is_asked_again(self) -> None:
        result, _ = run_with_inputs(lambda: get_positive_float("Price: "), ["", "  ", "9"])
        self.assertEqual(result, 9.0)

    def test_valid_first_time_prints_nothing(self) -> None:
        result, output = run_with_inputs(lambda: get_positive_float("Price: "), ["4.25"])
        self.assertEqual((result, output), (4.25, ""))


class TestOtherHelpers(unittest.TestCase):
    def test_non_negative_float_accepts_zero(self) -> None:
        result, output = run_with_inputs(lambda: get_non_negative_float("W: "), ["-1", "0"])
        self.assertEqual(result, 0.0)
        self.assertIn("not negative", output)

    def test_non_negative_int_rejects_decimals_and_text(self) -> None:
        result, output = run_with_inputs(lambda: get_non_negative_int("Stock: "),
                                         ["2.5", "ten", "-3", "10"])
        self.assertEqual(result, 10)
        self.assertEqual(output.count("valid whole number"), 2)
        self.assertIn("not negative", output)
        self.assertIsInstance(result, int)

    def test_positive_int_rejects_zero(self) -> None:
        result, output = run_with_inputs(lambda: get_positive_int("Qty: "), ["0", "2"])
        self.assertEqual(result, 2)
        self.assertIn("greater than zero", output)
        self.assertIsInstance(result, int)


if __name__ == "__main__":
    unittest.main()
