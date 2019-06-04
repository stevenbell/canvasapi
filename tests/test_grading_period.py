from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.grading_period import GradingPeriod
from tests import settings


@requests_mock.Mocker()
class TestGradingPeriod(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        self.grading_period = GradingPeriod(
            self.canvas._Canvas__requester,
            {"title": "grading period 1", "id": "1", "course_id": 1}
        )

    def test_str(self, m):

        test_str = str(self.grading_period)
        self.assertIsInstance(test_str, str)

    # update()
    def test_update(self, m):
        register_uris({'grading_period': ['update']}, m)

        title = 'New title'
        edited_grading_period = self.grading_period.update(grading_period={'title': title})

        self.assertIsInstance(edited_grading_period, GradingPeriod)
        self.assertTrue(hasattr(edited_grading_period, 'title'))
        self.assertEqual(edited_grading_period.title, title)
        self.assertTrue(hasattr(edited_grading_period, course_id))
        self.assertEqual(edited_grading_period.course_id, self.course_id)