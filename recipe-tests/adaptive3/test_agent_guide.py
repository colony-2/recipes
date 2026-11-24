"""Check the guide linked from session instructions using the local checkout."""
from pathlib import Path
import re
import unittest

import yaml


class AgentGuide(unittest.TestCase):
    def test_link_points_to_the_documented_worker_and_job_commands(self):
        root = Path(__file__).resolve().parents[2]
        context = yaml.safe_load((root / "recipes/adaptive3/prompts/context.yaml").read_text())
        link = re.search(
            r"https://raw\.githubusercontent\.com/colony-2/recipes/refs/heads/main/(guides/[\w/-]+\.md)",
            context["outputs"]["instructions"],
        )
        self.assertIsNotNone(link, "New sessions need a URL for the C2 guide")
        guide = (root / link[1]).read_text()
        for reference in (
            "--require-capability docker", "--cursor CURSOR", "--output FILE",
            "job restart-points", "ask.yaml@main", "guides/ASK_RECIPE.md", "2,000",
        ):
            with self.subTest(reference=reference):
                self.assertIn(reference, guide)
