# zhongwen
def generateLog(task_ID, S_time, E_time, task_list, news_num, video_num, player_num, game_num):
    w_str = """<section class="gray-light">
    <div class="container">
        <!-- News Detail -->
        <div class="col-lg-12 col-md-12 col-sm-12 col-12">
            <div class="blog-details single-post-item format-standard">
                <div class="post-details">
                    <p><h4><a href="/">Task ID:%s  </a></h4>Task execution time %s to %s ,a total of %d news crawling task, %d video crawling task, %d athlete information crawling task, %d competition information crawling task.</p>
                </div>
            </div>
        </div>
    </div>
</section>"""%(task_ID, S_time, E_time, news_num, video_num, player_num, game_num)

    # 此处修改为保存日志的的位置
    # f = open('C:\\Users\\gao\\Desktop\\bysj\\program\\templates\\journal.html','a')
    f = open('/Users/xiaor/Project/Laboratory_project/program/templates/journal.html', 'a')
    f.write(w_str)
    f.close()
    