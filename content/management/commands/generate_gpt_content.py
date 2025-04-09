from django.core.management.base import BaseCommand, CommandError
from investment.models import InvestmentOpportunity
from content.services import create_gpt_content_version

class Command(BaseCommand):
    help = "Generate GPT-powered content for a given InvestmentOpportunity"

    def add_arguments(self, parser):
        parser.add_argument('asset_id', type=int, help='ID of the InvestmentOpportunity')

    def handle(self, *args, **options):
        asset_id = options['asset_id']
        try:
            opportunity = InvestmentOpportunity.objects.get(id=asset_id)
        except InvestmentOpportunity.DoesNotExist:
            raise CommandError(f"Asset with ID {asset_id} does not exist.")

        self.stdout.write(f"Generating content for {opportunity.ticker} — {opportunity.opportunity_name}...")

        version = create_gpt_content_version(opportunity)

        self.stdout.write(self.style.SUCCESS(
            f"✅ Content saved as version {version.version} (ID: {version.id})"
        ))

        self.stdout.write("🔍 Preview:")
        self.stdout.write(version.content[:500] + ("..." if len(version.content) > 500 else ""))
