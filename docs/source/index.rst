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

项目Github地址：\ `Github <https://github.com/Steven-Yutong/PhotoString.git>`__

项目Read the Docs地址：\ `Read the Docs <https://photostring-yutong.readthedocs.io/zh/latest/>`__

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

