import datetime
import os
import codecs

def generatePage(result_path, Spage_time, news_num, video_num, player_num, game_num):
    # path = 'C:\\Users\\gao\\Desktop\\bysj\\result\\%sresult'%result_path
    # news_list = os.listdir(path+'\\news')
    # video_list = os.listdir(path+'\\video')
    # player_list = os.listdir(path+'\\player')
    # game_list = os.listdir(path+'\\game')
    # 生成文件的路径，需要更改
    # 由于mac命令行会在空格前增加转义字符，需要对字符串进行处理
    path = ('/Users/xiaor/Project/Laboratory_project/result/%sresult' % result_path).replace(' ', '_')
    # 判断news文件夹是否存在
    isExists = os.path.exists(path + '/news')
    if not isExists:
        news_list = []
    else:
        news_list = os.listdir(path + '/news')

    isExists = os.path.exists(path + '/video')
    if not isExists:
        video_list = []
    else:
        video_list = os.listdir(path + '/video')

    isExists = os.path.exists(path + '/player')
    if not isExists:
        player_list = []
    else:
        player_list = os.listdir(path + '/player')

    isExists = os.path.exists(path + '/game')
    if not isExists:
        game_list = []
    else:
        game_list = os.listdir(path + '/game')

    news_text_list = []
    player_text_list = []
    for news in news_list:
        # with codecs.open('%s'%path+'\\news\\'+'%s'%news, mode='r', encoding='utf-8') as file_txt:
        with codecs.open('%s' % path + '/news/' + '%s' % news, mode='r', encoding='utf-8') as file_txt:
            lines = file_txt.readlines()
            news_text_list.append(lines)    #这个数组每一个元素代表一篇文章，每一篇文章中每一个元素代表原文中的一行
    for player in player_list:
        # with codecs.open('%s'%path+'\\player\\'+'%s'%player, mode='r', encoding='utf-8') as file_txt:
        with codecs.open('%s' % path + '/player/' + '%s' % player, mode='r', encoding='utf-8') as file_txt:
            lines = file_txt.readlines()
            player_text_list.append(lines)    #这个数组每一个元素代表一个运动员的信息，每一个运动员信息中的买一个元素代表运动员信息的一项
    task_str = '举重竞技系统 %s任务包含 %d 条运动员信息，%d 条赛事信息，%d 条视频信息和%d 条新闻信息'%(Spage_time, player_num, game_num, video_num, news_num)
    player_str = ''''''
    for player_text in player_text_list:
        print("player_text")
        print(player_text)
        player_str = player_str +'\n' + r'''<tr>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
</tr>'''%(player_text[0],player_text[1],player_text[2],player_text[3],player_text[4],)
    game_str = ''''''
    for game_title in game_list:
        game_str = game_str + '\n' +r'''<img class="img-fluid" src="%s\game\%s" alt="">'''%(path,game_title)
    video_str = ''''''
    for video_title in video_list:
        video_str = video_str + '\n' + r'''<div class="col-lg-4 col-md-6 col-sm-12">
<div class="_45lio">
<div class="_jk58o">
<video width="360" height="270" controls>
<source src="%s\video\%s" type="video/mp4">
</video>
</div>
<div class="_45lik">
<p>%s</p>
</div>
</div>
</div>'''%(path,video_title,video_title)
    news_str = ''''''
    for news_text in news_text_list:
        news_str = news_str + '\n' + r'''<div class="post-details">
<h2 class="post-title">%s</h2>
'''%news_text[0]
        l = len(news_text)
        for i in range(1,l):
            news_str = news_str + '\n' + r'''<p>%s</p>'''%news_text[i]
    html_str = r'''<!DOCTYPE html>
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>体育竞技备战系统结果展示</title>
        <link href="../assets/css/plugins.css" rel="stylesheet">
        <link href="../assets/css/styles.css" rel="stylesheet">
    </head>
	
    <body class="blue-skin">
        <div class="Loader"></div>
        <div id="main-wrapper">
			<div class="header header-light">
				<div class="container">
					<div class="row">
						<div class="col-lg-12 col-md-12 col-sm-12">
							<nav id="navigation" class="navigation navigation-landscape">
								<div class="nav-header">
									<a class="nav-brand" href="#">
										TOP
									</a>
									<div class="nav-toggle"></div>
								</div>
								<div class="nav-menus-wrapper">
									<ul class="nav-menu">
									
										<li class="active"><a href="#a">Play&Game<span class="submenu-indicator"></span></a></li>
										
										<li><a href="#b">Video<span class="submenu-indicator"></span></a></li>
										
										<li><a href="#c">News<span class="submenu-indicator"></span></a></li>
										
										<li><a href="#d">About</a></li>
									</ul>
								</div>
						</div>
					</div>
				</div>
			</div>
			<div class="clearfix"></div>
			<div class="hero-banner bg-cover" style="background:#93d4f0 url(assets/img/7f30fbdd913a43818fde6f0eedcde3b3.jpg) no-repeat;" data-overlay="5">
				<div class="container">
					<h1 class="small">体育竞技备战系统结果展示</h1>
					<p class="lead">%s</p>
				</div>
			</div>
			<a id="a"></a>
			<section class="gray-light min-sec">
				<div class="container">
					<div class="row justify-content-center">
						<div class="col-lg-7 col-md-9">
							<div class="sec-heading">
								<h2>运动员信息 & 赛事信息展示</h2>
							</div>
						</div>
					</div>
					<h4>运动员基本信息</h4>
					<div class="row justify-content-center">
						<table class="table table-striped">
							<tr>
								<td>运动员姓名</td>
								<td>运动员出生日期</td>
								<td>运动员代表队</td>
								<td>运动员级别</td>
								<td>运动员历史最佳成绩</td>
							</tr>
							%s
						</table>
					</div>
					<h4>运动员具体信息</h4>
					<div class="row justify-content-center">
						<table class="table table-striped">
							<tr>
								<td>时间\运动员姓名</td>
								<td>吕小军</td>
								<td>侯志慧</td>
								<td>蒋惠花</td>
							</tr>
							<tr>
								<td>2021年</td>
								<td>乌兹别克斯坦举重亚锦赛男子81公斤级冠军</td>
								<td>乌兹别克斯坦举重亚锦赛女子49公斤级冠军</td>
								<td>乌兹别克斯坦举重亚锦赛女子49公斤级亚军</td>
							</tr>
							<tr>
								<td>2020年</td>
								<td>“钱江源国家公园杯”2020年全国男子举重锦标赛男子81公斤级冠军</td>
								<td>“崀山杯”2020年全国女子举重锦标赛暨东京奥运会模拟赛49公斤级亚军</td>
								<td>无</td>
							</tr>
							<tr>
								<td>2019年</td>
								<td>泰国芭提雅世界举重锦标赛男子81公斤级冠军</td>
								<td>泰国芭提雅世界举重锦标赛女子49公斤级亚军</td>
								<td>泰国芭提雅世界举重锦标赛女子49公斤级冠军</td>
							</tr>
							<tr>
								<td>2018年</td>
								<td>土库曼斯坦世界举重锦标赛男子81公斤级冠军</td>
								<td>土库曼斯坦世界举重锦标赛女子49公斤级亚军</td>
								<td>土库曼斯坦世界举重锦标赛女子49公斤级季军</td>
							</tr>
							<tr>
								<td>2017年</td>
								<td>第十三届全运会举重比赛男子77公斤级冠军</td>
								<td>第十三届全运会举重比赛女子48公斤级冠军</td>
								<td>第十三届全运会举重比赛女子48公斤级第六名</td>
							</tr>
							<tr>
								<td>2016年</td>
								<td>里约奥运会举重男子77公斤级亚军</td>
								<td>全国女子举重锦标赛暨里约奥运会选拔赛女子48公斤级冠军</td>
								<td>无</td>
							</tr>
							<tr>
								<td>2015年</td>
								<td>休斯顿世界举重锦标赛男子77公斤级抓举金牌，挺举无成绩</td>
								<td>世界青年举重锦标赛女子48公斤级亚军</td>
								<td>休斯顿世界举重锦标赛女子48公斤级冠军</td>
							</tr>
						</table>
					</div>
					<h4>最新赛事信息</h4>
					<div class="row justify-content-center">
						%s
					</div>
				</div>
			</section>
			<a id="b"></a>
			<section class="min-sec">
				<div class="container">
					
					<div class="row justify-content-center">
						<div class="col-lg-7 col-md-9">
							<div class="sec-heading">
								<h2>视频信息展示</h2>
								<p>共 %d 条 举重 相关视频信息</p>
							</div>
						</div>
					</div>
					
					<div class="row">
                        %s
					</div>	
				</div>
			</section>
			<a id="c"></a>
			<section class="gray-light">
				<div class="container">
					<div class="row">
					<div class="col-lg-12 col-md-12 col-sm-12 col-12">
						<div class="blog-details single-post-item format-standard">
							%s
						</div>
					</div>
				</div>
			</section>
			<a id="d"></a>
			<section class="call-to-act" style="background:#5d47dd url(assets/img/landing-bg.png) no-repeat">
				<div class="container">
					<div class="row justify-content-center">
						<div class="col-lg-7 col-md-8">
							<div class="clt-caption text-center mb-4">
								<h3>举重竞技备战系统</h3>
								<p>任务开始时间：%s</p>
							</div>
						</div>				
					</div>
				</div>
			</section>
		</div>
		<script src="../assets/js/jquery.min.js"></script>
		<script src="../assets/js/popper.min.js"></script>
		<script src="../assets/js/bootstrap.min.js"></script>
		<script src="../assets/js/select2.min.js"></script>
		<script src="../assets/js/owl.carousel.min.js"></script>
		<script src="../assets/js/ion.rangeSlider.min.js"></script>
		<script src="../assets/js/counterup.min.js"></script>
		<script src="../assets/js/custom.js"></script>
	</body>
</html>'''%(task_str, player_str, game_str, len(video_list) + 1, video_str, news_str, Spage_time)
    # with codecs.open('%s\\result.html'%path, mode='a', encoding='utf-8') as file_txt:
    with codecs.open('%s/result.html' % path, mode='a', encoding='utf-8') as file_txt:
        file_txt.write(html_str)

if __name__ == "__main__":
    result_path = datetime.datetime.now().strftime('%Y-%m-%d %H')
    Spage_time = datetime.datetime.now().strftime('%Y年%m月%d日%H点')
    news_num = 0
    video_num = 0
    player_num = 0
    game_num = 0
    generatePage(result_path, Spage_time, news_num, video_num, player_num, game_num)