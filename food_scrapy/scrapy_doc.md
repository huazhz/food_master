1. 爬到多少个item就自动停止

   ```shell
   $ scrapy crawl xiachufang -s CLOSESPIDER_ITEMCOUNT=90
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

4. 缺少动态链接库

    ```shell
    # ImportError: libffi.so.6: cannot open shared object file: No such file or directory 

    echo $LD_LIBRARY_PATH
    export LD_LIBRARY_PATH="/usr/local/lib/python3.6/dist-packages/.libs_cffi_backend"
    
    # 解决方法    
    cp /usr/local/lib/python3.6/dist-packages/.libs_cffi_backend/libffi-d78936b1.so.6.0.4 /usr/lib/

    ```





5. 更改utf8为utf8mb4，储存emoji

    done


6. Scrapy重启 

7. #### 添加 爬取起始页参数

    done

8. 改变爬取策略，brutal force

    ```
    以fid为标识，自增爬取

    redis: fid_flag
    ```

    done

    ​

9. 回调函数不运行

    加大深度优先

10. 爬虫被重定向了

   解决思路：

   1. 带上cookie
   2. 直接爬手机版

11. Scrapy下载图片

    默认图片名为hash值，需要重写get_media_request方法

12. 给原有spider打patch 

    ```shell
    celery -A food_scrapy.food_scrapy.spiders.xiachufangpatch  worker --loglevel=info
    ```

    ​

13. 被302重定向了

