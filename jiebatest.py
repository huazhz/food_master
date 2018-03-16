#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jieba

seg_list = jieba.cut("我来到北京大学", cut_all=True)
print("full model: " + "/".join(seg_list))


seg_list = jieba.cut("我来到北京大学", cut_all=False)
print("default model: " + "/".join(seg_list))


seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")
print(','.join(seg_list))