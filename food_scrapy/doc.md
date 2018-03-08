
####解决no module named food_scrapy

    在Pycharm的project interpreter里将food_scrapy添加到sys.path中
    
#### 解决表情包等特殊字符插入问题
    
    utf-8 --> urf8mb4


#### 清空recipe队列 

    LTRIM recipe 0 0
    
#### 清空爬取url

    del urlset
    
    
#### 解决MultipleObjectsReturned

    不要在class meta里加上联合约束
    要想办法在程序中解决
    https://stackoverflow.com/questions/17960593/multipleobjectsreturned-with-get-or-create/29521117#29521117
    

####  一个爬虫只跑5分钟，然后celery开启另一个爬虫实例

    CLOSESPIDER_TIMEOUT = 300
    
    
### 