# wwm/extractors.py
import re
from bs4 import BeautifulSoup


def clean(text):
    if not text: return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text


class PageParser:
    @staticmethod
    def extract_stats_table(soup):
        """Scrapes the 'Infobox' style table usually found on the right or top"""
        stats = {}
        tables = soup.select('table.infobox, table.wiki_table')

        for table in tables:
            rows = table.select('tr')
            for row in rows:
                th = row.select_one('th')
                td = row.select_one('td')

                if not th and len(row.select('td')) == 2:
                    cols = row.select('td')
                    key = clean(cols[0].get_text())
                    val = clean(cols[1].get_text())
                    if key and val:
                        stats[key.lower().replace(' ', '_')] = val

                elif th and td:
                    key = clean(th.get_text())
                    val = clean(td.get_text())
                    if key and val:
                        stats[key.lower().replace(' ', '_')] = val
        return stats

    @staticmethod
    def extract_text_sections(soup):
        """
        Groups paragraphs under headers and stops before footer links.
        """
        sections = {}
        content_block = soup.select_one('#wiki-content-block')
        if not content_block:
            return {"error": "No content block found"}

        current_header = "General"
        buffer = []

        # Iterate over all direct children
        for element in content_block.children:
            text_content = clean(element.get_text())

            # Stop Condition: Avoid indexing the "All Weapons..." footer lists
            if text_content.startswith("All ") and "Where Winds Meet" in text_content:
                break

            # Header detection
            if element.name in ['h2', 'h3', 'h4', 'h5']:
                if buffer:
                    sections[current_header] = " ".join(buffer)
                    buffer = []
                current_header = text_content

            elif element.name in ['p', 'ul', 'ol', 'div']:
                if len(text_content) > 1 and "Edit" not in text_content:
                    buffer.append(text_content)

        if buffer:
            sections[current_header] = " ".join(buffer)

        return sections


# --- SPECIALIZED LOGIC WRAPPERS ---

class GenericExtractor:
    @staticmethod
    def extract(soup, item):
        item['stats'] = PageParser.extract_stats_table(soup)
        item['sections'] = PageParser.extract_text_sections(soup)

        # FIX 3: Description Extraction
        # Pull the first part of the 'General' section to the top level
        if 'General' in item['sections']:
            full_text = item['sections']['General']
            # Take the first sentence or first 200 chars
            summary = full_text.split('. ')[0] + '.'
            item['description'] = summary
        else:
            item['description'] = ""

        # FIX 4: Basic Recipe Parsing (Optional enhancement)
        # If we see "recipe" keys in sections, try to move them to structured stats
        recipe_key = next((k for k in item['sections'] if 'recipe' in k.lower()), None)
        if recipe_key:
            item['stats']['recipe_text'] = item['sections'][recipe_key]

        return item


class BossExtractor:
    @staticmethod
    def extract(soup, item):
        item = GenericExtractor.extract(soup, item)

        phases = []
        sections = item['sections']

        for header, content in sections.items():
            if 'phase' in header.lower():
                phases.append({
                    "name": header,
                    "description": content
                })

        if phases:
            item['stats']['phases_structured'] = phases

        return item


# --- FACTORY ---

def run_extractor(category, response, item):
    soup = BeautifulSoup(response.body, 'lxml')

    img = soup.select_one('.infobox img, table img')
    if img and img.has_attr('src'):
        item['image_url'] = response.urljoin(img['src'])

    if category == 'bosses':
        BossExtractor.extract(soup, item)
    else:
        GenericExtractor.extract(soup, item)