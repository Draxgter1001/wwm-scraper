BOT_NAME = 'wwm'
SPIDER_MODULES = ['wwm.spiders']
NEWSPIDER_MODULE = 'wwm.spiders'

ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 1.0 # Slightly faster but still polite
CONCURRENT_REQUESTS = 6

ITEM_PIPELINES = {
   'wwm.pipelines.MultiFilePipeline': 300,
}