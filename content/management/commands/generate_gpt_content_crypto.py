from django.core.management.base import BaseCommand, CommandError
from crypto.models import CryptoAsset
from content.services import create_gpt_content_version_for_crypto


class Command(BaseCommand):
    help = "Generate GPT content for a single CryptoAsset by symbol or ID"

    def add_arguments(self, parser):
        parser.add_argument("symbol_or_id", type=str)

    def handle(self, *args, **options):
        query = options["symbol_or_id"]
        try:
            asset = (
                CryptoAsset.objects.filter(symbol__iexact=query).first()
                or CryptoAsset.objects.filter(coingecko_id__iexact=query).first()
            )
            if not asset:
                raise CommandError(f"No CryptoAsset found for symbol or ID: {query}")

            self.stdout.write(f"Generating content for {asset.symbol} — {asset.name}...")

            version = create_gpt_content_version_for_crypto(asset)

            self.stdout.write(
                self.style.SUCCESS(f"✓ Created ContentVersion v{version.version} for {asset.symbol}")
            )


            self.stdout.write("🔍 Preview:")
            self.stdout.write(version.content[:500] + ("..." if len(version.content) > 500 else ""))

        except Exception as e:
            raise CommandError(f"Error generating content: {str(e)}")
