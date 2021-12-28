.. Lab3 documentation master file, created by
   sphinx-quickstart on Tue Dec 28 10:55:42 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Welcome to Lab3's documentation!
================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Lab3
=============================

小组成员信息： 

201932110143 王炫 

201932110145 邬程峰 

201932110146 吴彬宇

201932110147 吴雨桐 

201932110148 谢铭轩

项目Github地址：\ `Github <https://github.com/Steven-Yutong/Lab3.git>`__

项目Read the Docs地址：\ `Read the Docs <https://lab3-yutong.readthedocs.io/en/latest/>`__

Abstract
--------

完成一个简单的项目实例，在此过程中切身体验、学习测试驱动开发的流程，理解依赖反转在实际工程中的好处并学习其用法。

Introduction
------------

1. 在本实验中，通过这个简单的实际项目我们将了解如何通过遵循依赖倒置的原则来保持领域模型的纯粹性——让基础设施依赖于领域模型。

2. 需要在services.py文件中为项目实现一个服务(read)。该服务将选择一篇适合用户阅读的文章。read函数接受四个参数(user, user_repo, article_repo, session)作为输入；如果用户已成功分配了要读取的文章，则返回文章ID。

Materials and Methods
---------------------

以\ `书本第二节(Repository Pattern) <https://www.cosmicpython.com/book/chapter_02_repository.html>`__\ 和\ `书本第四节(Flask API and Service  Layer) <https://www.cosmicpython.com/book/chapter_04_service_layer.html>`__\ 的项目源码为开发基础，结合书本中讲到的仓库模型、域模型以及服务层等知识内容，对本实验的项目进行开发。

Results
-------

orm.py

.. code:: python

   # Software Architecture and Design Patterns -- Lab 3 starter code
   # Copyright (C) 2021 Hui Lan

   from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey
   from sqlalchemy.orm import mapper, relationship

   import model

   metadata = MetaData()

   articles = Table(
       'articles',
       metadata,
       Column('article_id', Integer, primary_key=True, autoincrement=True),
       Column('text', String(10000)),
       Column('source', String(100)),
       Column('date', String(10)),
       Column('level', Integer, nullable=False),
       Column('question', String(1000)),
       )


   users = Table(
       'users',
       metadata,
       Column('username', String(100), primary_key=True),
       Column('password', String(64)),
       Column('start_date', String(10), nullable=False),
       Column('expiry_date', String(10), nullable=False),
       )

   newwords = Table(
       'newwords',
       metadata,
       Column('word_id', Integer, primary_key=True, autoincrement=True),
       Column('username', String(100), ForeignKey('users.username')),
       Column('word', String(20)),
       Column('date', String(10)),
       )

   readings = Table(
       'readings',
       metadata,
       Column('id', Integer, primary_key=True, autoincrement=True),
       Column('username', String(100), ForeignKey('users.username')),
       Column('article_id', Integer, ForeignKey('articles.article_id')),
       )


   def start_mappers():
       articles_mapper = mapper(model.Article, articles)
       newWords_mapper = mapper(model.NewWord, newwords)
       # users_mapper
       mapper(
           model.User,
           users,
           properties={
               'newwords': relationship(
                   newWords_mapper),
               '_read': relationship(
                   articles_mapper, secondary=readings
               )
           }
       )

services.py

.. code:: python

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

Discussions
-----------

修改工作的详细解释
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 由于这是测试驱动开发，根据项目测试提供的需求，我需要完成对应的服务以及完善相应的对象映射，才能够让测试通过。
2. 在orm.py文件的start_mappers()方法中，写了article，newword和usermodel这三个来自model.py的类的映射mapper，使得在调用start_mappers()方法后会以model中的域模型为基础，以orm.py中的所有初始化Table为原型创建对应的数据库表。
3. 在services.py的read方法中实现了判断用户是否合法、判断文章是否在库内和为用户提供文章进行阅读三个方法。根据测试的要求，让第一和第二个方法以raise对应的Exception为结尾，第三个方法以整个read函数的返回值article.id为结尾。

read方法是否遵循单一职责原则（SRP）？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

单一职责原则(SRP)：一个类应该有且仅有一个引起它变化的原因，否则类应该被拆分。

read方法并没有遵循单一职责原则。read方法中包含了\ **判断用户是否合法**\ 、\ **判断文章是否在库内**\ 和\ **为用户提供文章进行阅读**\ 三个方法，而前两种方法并不是read方法的主体方法，即其方法的具体实现逻辑、内容不应该是read方法需要了解的；当判断用户是否合法或是判断文章是否在库内的需求改变，则需要对read整个方法进行修改、测试，大大降低了维护的效率。

应当将read中的前两种方法拆分出去，如命名两个validate_user和validate_article类，在类中分别达成对应的需求。


