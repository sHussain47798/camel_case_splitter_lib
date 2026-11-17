"""Tests for camel_case_splitter_lib."""

import unittest

from camel_case_splitter_lib import split, split_identifier


class SplitIdentifierTests(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(split_identifier(""), [])
        self.assertEqual(split(""), [])

    def test_single_lowercase_word(self):
        self.assertEqual(split_identifier("hello"), ["hello"])

    def test_single_uppercase_word(self):
        self.assertEqual(split_identifier("HELLO"), ["hello"])

    def test_pascal_case(self):
        self.assertEqual(split_identifier("PascalCase"), ["pascal", "case"])

    def test_camel_case(self):
        self.assertEqual(split_identifier("camelCase"), ["camel", "case"])

    def test_acronym_followed_by_word(self):
        self.assertEqual(split_identifier("HTTPServer"), ["http", "server"])

    def test_acronym_alone(self):
        self.assertEqual(split_identifier("HTTP"), ["http"])

    def test_acronym_with_trailing_uppercase(self):
        self.assertEqual(split_identifier("XMLHttpRequest"), ["xml", "http", "request"])

    def test_digits_are_their_own_tokens(self):
        self.assertEqual(split_identifier("parse2D"), ["parse", "2", "d"])

    def test_digits_before_letters(self):
        self.assertEqual(split_identifier("2DArray"), ["2", "d", "array"])

    def test_separators_are_dropped(self):
        self.assertEqual(split_identifier("foo_bar-baz qux"), ["foo", "bar", "baz", "qux"])

    def test_repeated_separators_do_not_produce_empty_tokens(self):
        self.assertEqual(split_identifier("__foo__bar__"), ["foo", "bar"])

    def test_leading_and_trailing_separators(self):
        self.assertEqual(split_identifier("_camelCase_"), ["camel", "case"])

    def test_unicode_letters_are_not_special(self):
        # Non-ASCII letters are treated as ordinary characters, so they do not
        # create case boundaries.  This keeps the splitter deterministic.
        self.assertEqual(split_identifier("caféBar"), ["cafébar"])

    def test_type_error_for_non_string(self):
        with self.assertRaises(TypeError):
            split_identifier(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            split(None)  # type: ignore[arg-type]

    def test_split_is_alias(self):
        self.assertEqual(split("HTTPServer"), split_identifier("HTTPServer"))


if __name__ == "__main__":
    unittest.main()
