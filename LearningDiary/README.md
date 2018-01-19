### Learning diary
*   当访问某些网站时,需要将settings.py中
```
# Obey robots.txt rules ,default True
ROBOTSTXT_OBEY = False
```
否则,会访问不到获取不到部分网页.
参考:http://blog.csdn.net/you_are_my_dream/article/details/60479699

*   当需要登录时,可先登录利用记住我的方式设置cookies,以达到爬虫以登录状态访问网站.
