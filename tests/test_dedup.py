"""Testes de narrative/dedup.py.

Corre com: python -m unittest tests.test_dedup -v
"""
from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone

from narrative.dedup import dedup_hash, group_id, normalize, same_group


class TestNormalize(unittest.TestCase):
    def test_lowercase_and_sort(self):
        self.assertEqual(normalize("Fed Holds Rates Steady"),
                         normalize("rates steady fed holds"))

    def test_strips_punctuation(self):
        self.assertEqual(normalize("Fed: holds rates!"),
                         normalize("Fed holds rates"))

    def test_removes_stopwords_en(self):
        # "the Fed" e "Fed" devem dar mesma normalização
        self.assertEqual(normalize("the Fed holds"), normalize("Fed holds"))

    def test_removes_stopwords_pt(self):
        self.assertEqual(normalize("o Copom mantém a Selic"),
                         normalize("Copom mantém Selic"))

    def test_preserves_accents(self):
        # manutenção de acentos é importante: "e" vs "é" são tokens diferentes
        self.assertIn("mantém", normalize("Copom mantém Selic"))


class TestDedupHash(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(dedup_hash("Fed holds rates"),
                         dedup_hash("Fed holds rates"))

    def test_length_16(self):
        self.assertEqual(len(dedup_hash("anything")), 16)

    def test_variations_collapse(self):
        # 5 variações da mesma notícia → mesmo hash
        variations = [
            "Fed holds rates steady",
            "The Fed holds rates steady",
            "Fed: holds rates steady!",
            "Rates steady — Fed holds",
            "FED HOLDS RATES STEADY",
        ]
        hashes = {dedup_hash(v) for v in variations}
        self.assertEqual(len(hashes), 1, f"Expected 1 hash, got {hashes}")

    def test_different_stories_differ(self):
        self.assertNotEqual(dedup_hash("Fed holds rates"),
                            dedup_hash("Fed cuts rates"))


class TestSameGroup(unittest.TestCase):
    BASE = "2026-04-15T10:00:00Z"

    def test_same_title_within_window(self):
        later = "2026-04-15T18:00:00Z"
        self.assertTrue(same_group(
            "Fed holds rates", self.BASE,
            "Fed Holds Rates",  later,
        ))

    def test_same_title_outside_window(self):
        day_after = "2026-04-16T12:00:00Z"
        self.assertFalse(same_group(
            "Fed holds rates", self.BASE,
            "Fed Holds Rates",  day_after,
        ))

    def test_different_stories(self):
        self.assertFalse(same_group(
            "Fed holds rates",  self.BASE,
            "ECB cuts rates",   self.BASE,
        ))

    def test_accepts_datetime_objects(self):
        a = datetime.fromisoformat("2026-04-15T10:00:00+00:00")
        b = datetime.fromisoformat("2026-04-15T11:00:00+00:00")
        self.assertTrue(same_group("Same story", a, "same STORY", b))


class TestGroupId(unittest.TestCase):
    def test_format(self):
        gid = group_id("Fed holds", "2026-04-15T10:00:00Z")
        self.assertRegex(gid, r"^[0-9a-f]{16}_\d{8}$")

    def test_same_story_different_days_differ(self):
        a = group_id("Fed holds rates", "2026-04-15T10:00:00Z")
        b = group_id("Fed holds rates", "2026-04-16T10:00:00Z")
        self.assertNotEqual(a, b)

    def test_same_story_same_day_equal(self):
        a = group_id("Fed holds rates", "2026-04-15T10:00:00Z")
        b = group_id("Fed holds rates", "2026-04-15T22:00:00Z")
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
