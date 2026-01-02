# wwm/items.py
import scrapy


class ScrapedEntity(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()

    # "Structured" data (strictly parsed numbers/stats)
    stats = scrapy.Field()

    # "Unstructured" content (The text guides, lore, strategy)
    # This will look like: { "How to Obtain": "...", "Combat Strategy": "..." }
    sections = scrapy.Field()

    # Metadata
    scraped_at = scrapy.Field()