from django.test import TestCase
from affiliate.models import AffiliateLink
from investment.models import InvestmentOpportunity
from content.services import create_gpt_content_version, save_content_version

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


class AffiliateInjectionTests(TestCase):
    def test_link_appended(self):
        AffiliateLink.objects.create(url="http://x", description="stock‑x")
        opp = InvestmentOpportunity.objects.create(ticker="AAPL", opportunity_name="Apple", description="Test")
        cv = save_content_version(content="Body", opportunity=opp)
        self.assertIn("(affiliate)", cv.content)


class DisclosureInjectionTests(TestCase):
    def setUp(self):
        self.opportunity = InvestmentOpportunity.objects.create(
            ticker="DISC",
            opportunity_name="Disclosure Test Opportunity",
            description="Testing disclosure injection.",
            data={}
        )

    def test_disclosure_injected_into_saved_content(self):
        raw_body = "This is a simple content body for disclosure testing."

        content_version = save_content_version(
            content=raw_body,
            opportunity=self.opportunity,
            changes="Disclosure Injection Test",
            metrics={"dummy_metric": 123},
            title="Disclosure Test Title"
        )

        saved_content = content_version.content

        self.assertIn("Not financial advice", saved_content)
        self.assertIn("affiliate links", saved_content)
        self.assertIn("This is a simple content body", saved_content)