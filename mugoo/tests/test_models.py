import datetime

from django.test import TestCase

from mugoo.webapp.models import Book

import pytest

def test_book_string_representation(self):
    book=Book(title="Book for testing",version=2,author="sid kala",isbn=123456789123,postedon=datetime.datetime.now())
    self.assertEqual(str(book),book.title)