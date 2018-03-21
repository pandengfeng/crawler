drop table qidian_book_detail_info;
drop table qidian_book_tags;
drop table qidian_book_author;
drop table qidian_book_reader;
drop table qidian_book_reader_pay_detail;

create table qidian_book_detail_info(
    book_id VARCHAR(128) not null PRIMARY  KEY COMMENT '作品id',
    book_name VARCHAR(128) COMMENT '作品名称',
    book_author VARCHAR(128) COMMENT '作者',
    book_author_url VARCHAR(128) COMMENT '作者页面url',
    book_words_number VARCHAR(128)COMMENT '字数',
    book_click_quantity VARCHAR(128) COMMENT '点击量',
    book_recommend_number VARCHAR(128) COMMENT '推荐数',
    book_monthly_ticket_number VARCHAR(128) COMMENT '月票数',
    book_support_number VARCHAR(128) COMMENT '打赏数',
    book_introduction text COMMENT '简介',
    book_chapter_number VARCHAR(128) COMMENT '章节数',
    book_discuss_number VARCHAR(128) COMMENT '讨论数',
    book_near_update_time VARCHAR(128) COMMENT '最近更新时间',
    book_page_url VARCHAR(128) COMMENT '作品页面链接'
);


create table qidian_book_tags(
    book_id VARCHAR(128) not null COMMENT '作品id',
    book_tag VARCHAR(128) not null COMMENT '标签' 
);


create table qidian_book_author(
    book_author_id VARCHAR(128) not null PRIMARY  KEY COMMENT '作者id',
    book_author VARCHAR(128) ,
    book_author_sex VARCHAR(128) COMMENT '性别',
    book_author_books VARCHAR(128) COMMENT '作品数量',
    book_author_write_num VARCHAR(128) COMMENT '总创作字数',
    book_author_write_days VARCHAR(128) COMMENT '总创作天数',
    book_author_address VARCHAR(128) COMMENT '地址'
);


create table qidian_book_reader(
    book_reader_id VARCHAR(128) not null PRIMARY  KEY COMMENT '读者id',
    book_reader_sex VARCHAR(128) COMMENT '性别',
    book_reader_name VARCHAR(128) COMMENT '名字',
    book_reader_focus VARCHAR(128) COMMENT '关注',
    book_reader_fans VARCHAR(128) COMMENT '粉丝',
    book_reader_address VARCHAR(128) COMMENT '地址',
    book_reader_vip_level VARCHAR(128) COMMENT 'VIP等级',
    book_reader_experience_level VARCHAR(128) COMMENT '经验等级',
    book_reader_collection_number VARCHAR(128) COMMENT '书架收藏数',
    book_reader_subscribe_number VARCHAR(128) COMMENT '订阅数',
    book_reader_exceptional_number VARCHAR(128) COMMENT '打赏数',
    book_reader_monthly_ticket_number VARCHAR(128) COMMENT '投月票数',
    book_reader_recommend_number VARCHAR(128) COMMENT '投推荐票数'
);


create table qidian_book_reader_pay_detail(
    book_reader_id VARCHAR(128) not null COMMENT '读者id',
    book_id VARCHAR(128) not null COMMENT '作品id',
    book_reader_fans_level VARCHAR(128) not null COMMENT '作品粉丝等级',
    book_name VARCHAR(128) not null COMMENT '作品名称'
);
