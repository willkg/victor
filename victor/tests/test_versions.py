from unittest import TestCase

from nose.tools import eq_

from victor.cmdline import get_version_from_requirement


class GetVersionFromRequirementTests(TestCase):
    def test_basic(self):
        for text, expected in (('foo', ('foo', '')),
                               ('foo==1.0', ('foo', '1.0')),
                               ('foo>=1.0', ('foo', '1.0')),
                               ('foo>1.0', ('foo', '1.0')),
        ):
            eq_(get_version_from_requirement(text), expected)
