# ScrapyZol
Use python scrapy to scratch the hottest phones' infomation.

Example:
```Bash
scrapy crawl PhoneSpider -t json -o a.json
```
> This will save the scratched data into a.json file.


### Add scrapy-splash for js generated html content
1. install `scrapy-splash`
```
pip install scrapy-splash
```

2. install docker, refer to different manuals for different architecture
3. pull splash image and start it
```
docker pull scrapinghub/splash
docker run -p 8050:8050 scrapinghub/splash
```

Then you can see splash testing page in web browser at url: http://localhost:8050

4. in python code, you need to change `settings`.py and use `scrapy_splash.SplashRequest` instead of `scrapy.Request`
```
#In settings.py
-----------------------
SPIDER_MIDDLEWARES = {
#    'zol.middlewares.ZolSpiderMiddleware': 543,
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'zol.middlewares.MyCustomDownloaderMiddleware': 543,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
}


SPLASH_URL = 'http://localhost:8050'

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
```