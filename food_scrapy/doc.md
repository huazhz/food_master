
####解决no module named food_scrapy

    在Pycharm的project interpreter里将food_scrapy添加到sys.path中
    
#### 解决表情包等特殊字符插入问题
    
    utf-8 --> urf8mb4


#### 清空recipe队列 

    LTRIM recipe 0 0
    
#### 清空爬取url

    del urlset
    
    
#### 解决MultipleObjectsReturned

    在class meta里加上联合约束
    https://stackoverflow.com/questions/17960593/multipleobjectsreturned-with-get-or-create/29521117#29521117