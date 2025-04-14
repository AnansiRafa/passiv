from django.test import TestCase
from investment.models import InvestmentOpportunity
from content.services import create_gpt_content_version

class ContentMetricsTest(TestCase):
    def setUp(self):
        self.op = InvestmentOpportunity.objects.create(
            ticker="AAPL",
            opportunity_name="Apple Spike",
            description="iPhone 99 Launch",
            data={"growth": 1.2}
        )

    def test_content_metrics(self):
        cv = create_gpt_content_version(self.op)
        self.assertIn("readability_score", cv.metrics)
        self.assertIn("sentiment", cv.metrics)
        self.assertGreater(cv.metrics["word_count"], 0)