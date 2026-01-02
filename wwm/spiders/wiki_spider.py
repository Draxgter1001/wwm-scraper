# wwm/spiders/wiki_spider.py
import scrapy
from datetime import datetime
from ..items import ScrapedEntity
from ..extractors import run_extractor


class WikiSpider(scrapy.Spider):
    name = "wwm_spider"
    allowed_domains = ["wherewindsmeet.wiki.fextralife.com"]

    START_URLS_MAP = {
        "weapons": "https://wherewindsmeet.wiki.fextralife.com/Martial+Arts+Weapons",
        "armor": "https://wherewindsmeet.wiki.fextralife.com/Armor",
        "gear-sets": "https://wherewindsmeet.wiki.fextralife.com/Gear+Sets",
        "items": "https://wherewindsmeet.wiki.fextralife.com/Items",
        "crafting": "https://wherewindsmeet.wiki.fextralife.com/Crafting",
        "stats": "https://wherewindsmeet.wiki.fextralife.com/Stats",
        "status-effects": "https://wherewindsmeet.wiki.fextralife.com/Status+Effects",
        "skills": "https://wherewindsmeet.wiki.fextralife.com/Skills",
        "martial-arts": "https://wherewindsmeet.wiki.fextralife.com/Martial+Arts",
        "inner-ways": "https://wherewindsmeet.wiki.fextralife.com/Inner+Ways",
        "mystic-skills": "https://wherewindsmeet.wiki.fextralife.com/Mystic+Skills",
        "locations": "https://wherewindsmeet.wiki.fextralife.com/Locations",
        "enemies": "https://wherewindsmeet.wiki.fextralife.com/Enemies",
        "bosses": "https://wherewindsmeet.wiki.fextralife.com/Bosses",
        "sects": "https://wherewindsmeet.wiki.fextralife.com/Sects"
    }

    # REPLACEMENT FOR start_requests
    def start_requests(self):
        for category, url in self.START_URLS_MAP.items():
            yield scrapy.Request(
                url,
                callback=self.parse_list_page,
                meta={'category': category}
            )

    def parse_list_page(self, response):
        category = response.meta['category']
        self.logger.info(f"--- Indexing Category: {category} ---")

        # 1. Table Links (Primary)
        links = response.css('table.wiki_table td a::attr(href), table.infobox td a::attr(href)').getall()

        # 2. List/Grid Links (Secondary)
        if not links:
            links = response.css('div.col-sm-2 a::attr(href), ul li a::attr(href)').getall()

        unique_links = set(links)

        for link in unique_links:
            # Filter bad links
            if any(x in link for x in ["/file/", "board", "Login", "Edit", "#"]):
                continue

            yield response.follow(link, self.parse_entity, meta={'category': category})

    def parse_entity(self, response):
        entity = ScrapedEntity()
        entity['id'] = response.url.split('/')[-1].replace('+', '-').lower()

        # FIX 1: Name Extraction & Fallback
        # Try H1, then Title, then fallback to ID-based formatting
        h1_name = response.css('h1#page-title::text').get(default='').strip()
        if h1_name:
            entity['name'] = h1_name
        else:
            # "bighead-carp" -> "Bighead Carp"
            entity['name'] = entity['id'].replace('-', ' ').title()

        raw_category = response.meta['category']
        entity['url'] = response.url
        entity['scraped_at'] = datetime.now().isoformat()

        # FIX 2: Category Guard / Correction
        # Re-assign items that were miscategorized (e.g. currencies in armor list)
        if entity['id'] in ['currencies', 'general-information']:
            entity['category'] = 'misc'
        elif entity['id'] in ['consumables', 'consumable-items']:
            entity['category'] = 'items'
        else:
            entity['category'] = raw_category

        # Run the updated Extractor
        run_extractor(entity['category'], response, entity)

        yield entity