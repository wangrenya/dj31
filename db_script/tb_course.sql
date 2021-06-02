INSERT INTO `tb_teachers` values(1,now(),now(),0,'蓝羽', 'python高级讲师','讲师简介','/media/avatar.jpeg');
INSERT INTO `tb_teachers` values(2,now(),now(),0,'诗诗', 'python小姐姐','女神','/media/avatar.jpeg');



insert into tb_course_category (name, create_time, update_time, is_delete) values
('日韩', now(), now(), 0),
('欧美', now(), now(), 0),
('法剧', now(), now(), 0);




insert into tb_course (title, cover_url, video_url, `profile`, outline, teacher_id, category_id, create_time, update_time, is_delete) values
('竹林', 'http://kf5krminv5u968gdqp5.exp.bcevod.com/mda-kf9fcz1sy86c2ixc/mda-kf9fcz1sy86c2ixc.jpg', 'http://kf5krminv5u968gdqp5.exp.bcevod.com/mda-kf9fcz1sy86c2ixc/mda-kf9fcz1sy86c2ixc.m3u8',  '减肥从运动开始', '人气少女东京不热', 1, 2, now(), now(), 0),

('告白气球', 'http://kf5krminv5u968gdqp5.exp.bcevod.com/mda-kf9mwirawv31n9c6/mda-kf9mwirawv31n9c6.jpg', 'http://kf5krminv5u968gdqp5.exp.bcevod.com/mda-kf9mwirawv31n9c6/mda-kf9mwirawv31n9c6.m3u8',  '喝奶茶也要投票', '好兄弟一辈子', 1, 1, now(), now(), 0);





