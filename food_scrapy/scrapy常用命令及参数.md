1. 爬到多少个item就自动停止

   ```shell
   $ scrapy crawl manual -s CLOSESPIDER_ITEMCOUNT=90
   ```

   ​


2. 爬多少时间停止

   ```shell
   scrapy crawl fast -s CLOSESPIDER_TIMEOUT=10
   ```


3. 爬多少页停止

   ```shell
   scrapy crawl fast -s CLOSESPIDER_PAGECOUNT=10
   ```

   ​

