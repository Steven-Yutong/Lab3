# Software Architecture and Design Patterns -- Lab 3 starter code
# An implementation of the Service Layer
# Copyright (C) 2021 Hui Lan

import model

# word and its difficulty level
WORD_DIFFICULTY_LEVEL = {'starbucks':5, 'luckin':4, 'secondcup':4, 'costa':3, 'timhortons':3, 'frappuccino':6}


class UnknownUser(Exception):
    print("用户不存在")
    pass


class NoArticleMatched(Exception):
    print("无相关文章")
    pass


def read(user, user_repo, article_repo, session):
    # 判断用户是否在库内
    username = user.username
    if user_repo.get(username) is None or user_repo.get(username).password != user.password:
        # 注意!!!! 要用raise,而不是return!!!
        raise UnknownUser

    user_level = 0  # 用户的英语等级(初始化为0)
    amount = 0  # 单词数量
    # all_words 为NewWord中指定用户拥有的所有单词
    all_words = session.query(model.NewWord).filter_by(username=username).all()
    for user_word in all_words:
        user_level += WORD_DIFFICULTY_LEVEL[user_word.word]
        amount += 1
    user_level = user_level / amount
    article = None  # 初始化文章
    article_level = 0  # 文章的等级(初始化为0)
    for article0 in article_repo.list():
        if article0.level > user_level:
            if article is None or article0.level < article_level:
                article_level = article0.level
                article = article0
    # 找不到需要的文章
    if article is None:
        raise NoArticleMatched
    session.query(model.User).filter_by(username=username).one().read_article(article)
    session.commit()
    return article.article_id


