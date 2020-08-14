# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render

from .settings import STATIC_URL
from .models import blog
from django.views.generic.base import View
import json
from elasticsearch import Elasticsearch

client = Elasticsearch(hosts=["127.0.0.1:9200"])
photo_path_prefix = STATIC_URL


class SearchSuggest(View):
    def get(self, request):
        keyword = request.GET.get('s', '')
        re_datas = []
        if keyword:
            s = blog.search()
            s = s.suggest('my_suggest', keyword, completion={
                "field": "body", "size": 10, "fuzzy": {"fuzziness": 1}})
            suggestion = s.execute()
            for match in suggestion.suggest.my_suggest._l_[0]['options']:
                source = match['_source']
                re_datas.append(source["head"] + ", " + source["body"])
        return HttpResponse(json.dumps(re_datas), content_type="application/json")
        pass


class SearchSearch(View):
    def get(self, request):
        key_words = request.GET.get('q', '')
        #print(key_words)
        page = request.GET.get('p', 1)
        try:
            page = int(page)
        except:
            page = 1

        page_size = 10
        start_time = datetime.now()
        response = client.search(
            index="bblog",
            body={
                "query": {
                    "multi_match": {
                        "analyzer":"ik_max_word",
                        "query": key_words,
                        "fields": ["title", "text"],
                    }
                },
                "from": (page - 1) * page_size,
                "size": page_size,
                "highlight": {
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ['</span>'],
                    "fields": {
                        "title": {},
                        "content": {},

                    }
                }
            }
        )
        end_time = datetime.now()
        last_sec = (end_time - start_time).total_seconds()
        total_nums = response['hits']['total']['value']
        page_nums = int(math.ceil(total_nums / 10.0))
        hit_list = []
        num=0
        for hit in response['hits']['hits']:
            num+=1
            hit_dict = {}
            keyfields = ["title","text","url"]
            '''
            for keyfield in keyfields:
                if keyfield in hit['highlight']:
                    hit_dict[keyfield] = "".join(hit['highlight'][keyfield])
                else:
                    hit_dict[keyfield] = hit['_source'][keyfield]
                    '''
            hit_dict['num'] = num
            hit_dict['title'] = hit['_source']['title']
            hit_dict['url'] = hit['_source']['url']
            hit_dict['score'] = hit['_score']

            hit_list.append(hit_dict)

        topn_search = []
        return render(request, "result.html", {"page": page,
                                               "all_hits": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums,
                                               "last_seconds": last_sec,
                                               "topn_search": topn_search})
        pass
