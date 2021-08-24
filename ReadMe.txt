
一、项目要求：
信息搜集：
    1、运动员基本信息；      百度百科
    2、比赛成绩（全国和国际性赛事前3或前8都搜集进来）；
    3、运动员相关的新闻和视频；         协会官网+
    4、比赛地的天气气象（该项目的全国比赛和国际比赛，数据要求：比赛名称，时间，地点，比赛成绩（前3或者前8））；

二、项目进度：
2021/08/15-
搜索并确定数据源
1、官网；
2、维基百科、百度百科；
3、网页搜索；

2021/08/16      修改及维护代码
2021/08/17-18   确定数据源
2021/08/19      完成video的爬取
2021/08/24      基本完成newsSpider及初版playerSpider



三、结果形式：
result:
    举重
        吕小军
            吕小军.txt   包含： 姓名   出生地   出生日期  运动项目    所属运动队   主要奖项
            news
            video
    跳水
    跆拳道
    。。。




四、遇到的问题及解决方案：
1、  2021/08/19      python修改task.xml文件时，中文总是出现问题        通过 basetask.write(_basexml, encoding = 'utf-8')修改写入的编码方式
2、  2021/08/19      xml文件转义字符                                 在读取url时，进行替换
3、  2021/08/20-21      央视新闻的链接为ajax动态加载，无法简单通过get请求获取数据      抓包发现，其数据是通过json保存的，需要查看浏览器的Query String Parameters,构造资源所在的新url进行访问。
4、



五、信息暂存：
<url title="http://www.cwa.org.cn/zhongguoliliang/">
   <item>举重</item>
   <spidertype>news</spidertype>
   <starttime>2021051819</starttime>
   <endtime>2022051819</endtime>
   <runtime>2021081812</runtime>
   <state>running</state>
   <cycle>24</cycle>
   <depth>2</depth>
   <pstate>run</pstate>
   <uid>3</uid>
</url>
<url title="https://baike.baidu.com/item/%E5%90%95%E5%B0%8F%E5%86%9B/3293553?fr=aladdin">
   <item>举重</item>
   <spidertype>player1</spidertype>
   <starttime>2021051819</starttime>
   <endtime>2022051819</endtime>
   <runtime>2021081812</runtime>
   <state>running</state>
   <cycle>24</cycle>
   <depth>1</depth>
   <pstate>run</pstate>
   <uid>4</uid>
</url>
<url title="https://baike.baidu.com/item/%E4%BE%AF%E5%BF%97%E6%85%A7/19733278?fr=aladdin">
   <item>举重</item>
   <spidertype>player2</spidertype>
   <starttime>2021051819</starttime>
   <endtime>2022051819</endtime>
   <runtime>2021081812</runtime>
   <state>running</state>
   <depth>1</depth>
   <cycle>24</cycle>
   <pstate>run</pstate>
   <uid>5</uid>
</url>
<url title="https://baike.baidu.com/item/%E8%92%8B%E6%83%A0%E8%8A%B1/9620518?fr=aladdin">
   <item>举重</item>
   <spidertype>player3</spidertype>
   <starttime>2021051819</starttime>
   <endtime>2022051819</endtime>
   <runtime>2021081812</runtime>
   <state>running</state>
   <cycle>24</cycle>
   <depth>1</depth>
   <pstate>run</pstate>
   <uid>6</uid>
</url>
<url title="https://new.qq.com/omn/20210418/20210418A01F8I00.html">
   <item>举重</item>
   <spidertype>game1</spidertype>
   <starttime>2021051819</starttime>
   <endtime>2022051819</endtime>
   <runtime>2021081812</runtime>
   <state>running</state>
   <cycle>24</cycle>
   <depth>1</depth>
   <pstate>run</pstate>
   <uid>7</uid>
</url>
<url title="https://search.cctv.com/search.php?qtext=王涵&amp;type=video">
   <item>跳水</item>
   <spidertype>video</spidertype>
   <starttime>2021051819</starttime>
   <endtime>2022052000</endtime>
   <runtime>2021081812</runtime>
   <state>running</state>
   <cycle>24</cycle>
   <depth>2</depth>
   <pstate>run</pstate>
   <uid>2</uid>
</url>