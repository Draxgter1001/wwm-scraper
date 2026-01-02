# WWM Wiki Scraper (Python Edition) v1.0

A robust, high-performance web scraper for the **Where Winds Meet** FextraLife Wiki. 

It is designed to build the open-source WWM API dataset.

## Features

- **Hybrid Architecture**: Combines Scrapy's fast async engine with BeautifulSoup's parsing flexibility.
- **Smart Extractors**: Logic ported and improved for complex entities:
  - **Bosses**: Phase detection, attack color/type analysis (Red/Yellow/Blue).
  - **Martial Arts**: Weapon synergy mapping and skill extraction.
- **Anti-Ban System**: Built-in User-Agent rotation and randomized polite delays.
- **Clean JSON**: Structured, hierarchical output ready for API consumption.
- **Resilient Parsing**: Handles Fextralife's inconsistent HTML structures (nested tables, malformed headers) better than DOM traversal.

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install scrapy beautifulsoup4 lxml scrapy-fake-useragent
```

## Run the Scraper

You can run the full extraction pipeline using the runner script. The scraper will automatically detect categories 
and route data to the correct JSON file.

```bash
# Runs the spider for all configured categories
python main.py
```
Alternatively, use the Scrapy CLI:
```bash
# Run the specific spider
scrapy crawl wwm_spider
```

## Output Structure

Instead of a single massive file, the scraper uses a custom pipeline to organize data by category in the output/ directory.
```
output/
├── bosses.json            # Detailed boss stats, phases, and rewards
├── martial-arts.json      # Weapon skills and synergy data
├── armor.json             # Armor sets and stats
├── skills.json            # General skills and mystic arts
└── ... (other categories)
```

## JSON Schema Example (Bosses)
File: ```output/bosses.json```

```
[
    {
        "id": "lucky-seventeen",
        "name": "Lucky Seventeen",
        "category": "bosses",
        "url": "[https://wherewindsmeet.wiki.fextralife.com/Lucky+Seventeen](https://wherewindsmeet.wiki.fextralife.com/Lucky+Seventeen)",
        "data": {
            "basicInfo": {
                "location": "Qinghe",
                "boss_type": "Campaign Boss"
            },
            "phases": [
                {
                    "phase": 1,
                    "name": "Phase 1",
                    "description": "The boss starts by..."
                }
            ],
            "attacks": [
                {
                    "name": "Crescent Slash",
                    "type": "Blue",
                    "effect": "Parriable",
                    "description": "A horizontal swing that flashes blue..."
                }
            ],
            "rewards": [
                "Skill Book: Tides",
                "Gold Leaf"
            ]
        },
        "scraped_at": "2026-01-02T12:00:00.000000",
        "extractor_used": "boss_extractor"
    }
]
```
## Project Structure

```
wwm_python_scraper/
├── main.py                 # Entry point script
├── scrapy.cfg              # Scrapy deployment config
└── wwm/
    ├── __init__.py
    ├── items.py            # Data models (Schema)
    ├── settings.py         # Config (Delays, User-Agents)
    ├── pipelines.py        # HANDLES FILE SPLITTING (MultiFilePipeline)
    ├── extractors.py       # THE BRAINS: Parsing logic (Bosses, Weapons)
    └── spiders/
        ├── __init__.py
        └── wiki_spider.py  # THE ENGINE: Crawling & Link Discovery
```

## Configuration
Settings are managed in ```wwm/settings.py.```

### Pipeline Configuration
The ```MultiFilePipeline``` is enabled by default to handle file splitting.

```
ITEM_PIPELINES = {
   'wwm.pipelines.MultiFilePipeline': 300,
}
```

### Politeness Settings
To avoid getting banned by Fextralife:
```
DOWNLOAD_DELAY = 2.0        # Seconds between requests
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS = 4
```

## Development
### Adding a New Extractor

1. Open ```wwm/extractors.py.```
2. Create a new class (e.g., ```GearExtractor```).
3. Implement a static ```extract(soup, item)``` method using BeautifulSoup.
4. Update the ```run_extractor``` factory function at the bottom of the file to route the specific category to your new class.

## Legal
This tool is designed for the open-source WWM API project.
- **Respect Robots.txt**: The scraper is configured to obey robots.txt by default.
- **Attribution**: Content belongs to FextraLife and the game developers. Ensure your API credits the source.

## License
MIT License