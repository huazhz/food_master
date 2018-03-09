#### 爬到多少个item就自动停止

```shell
$ scrapy crawl manual -s CLOSESPIDER_ITEMCOUNT=90
```



#### 爬多少时间停止

```shell
scrapy crawl fast -s CLOSESPIDER_TIMEOUT=10
```


#### 爬多少页停止

```shell
scrapy crawl fast -s CLOSESPIDER_PAGECOUNT=10
```



#### 缺少动态链接库

```shell
# ImportError: libffi.so.6: cannot open shared object file: No such file or directory 

echo $LD_LIBRARY_PATH
export LD_LIBRARY_PATH="/usr/local/lib/python3.6/dist-packages/.libs_cffi_backend"

# 解决方法    
cp /usr/local/lib/python3.6/dist-packages/.libs_cffi_backend/libffi-d78936b1.so.6.0.4 /usr/lib/

```


#### 更改utf8为utf8mb4，储存emoji

#### Scrapy重启 

添加 爬取起始页参数

#### 从顶级目录向下遍历爬取

#### 突破UA限制

#### 突破IP限制

#### 使用消息队列

#### 使用celery定时任务

#### 改变爬取策略，brutal force

​	以fid为标识，自增爬取

​	redis: fid_flag

#### 回调函数不运行


加大深度优先



####解决no module named food_scrapy

    在Pycharm的project interpreter里将food_scrapy添加到sys.path中

#### 解决表情包等特殊字符插入问题

    utf-8 --> urf8mb4


#### 清空recipe队列 

    LTRIM recipe 0 0

#### 清空爬取url

    del urlset

​    
#### 解决MultipleObjectsReturned

    不要在class meta里加上联合约束
    要想办法在程序中解决
    https://stackoverflow.com/questions/17960593/multipleobjectsreturned-with-get-or-create/29521117#29521117


####  一个爬虫只跑5分钟，然后celery开启另一个爬虫实例

    CLOSESPIDER_TIMEOUT = 300

​    



##To be solved ...



1. ####TimeoutError

2. ####ConnectionRefusedError

   ​

3. ####celery指定时间启动不生效

   时区设置没生效，那就将东8区减8

   ​

4. ####爬虫分布式多机爬取