#!/usr/bin/python
# -*- coding: UTF-8 -*-

import codecs

slugs = codecs.open("../data/slug.txt", "r", encoding="UTF-8").readlines()
slugs_tag = codecs.open("../data/slug_tag.txt", "w+", encoding="UTF-8")

for slug in slugs:
  slugs_tag.write(slug.replace(' ', '-').lower())