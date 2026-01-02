import os
from scrapy.exporters import JsonItemExporter


class MultiFilePipeline:
    def open_spider(self, spider):
        self.exporters = {}

    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()
            exporter.file.close()

    def process_item(self, item, spider):
        cat = item.get('category', 'misc')

        if cat not in self.exporters:
            if not os.path.exists('output'): os.makedirs('output')
            f = open(f'output/{cat}.json', 'wb')
            exporter = JsonItemExporter(f, encoding='utf-8', indent=4)
            exporter.start_exporting()
            self.exporters[cat] = exporter

        self.exporters[cat].export_item(item)
        return item