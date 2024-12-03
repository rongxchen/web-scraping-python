from weibo import weibo_service


res = weibo_service.search("cicc")
weibo_service.save(res, "./csv/weibo")
