# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
import tweepy
from datetime import datetime
from multiprocessing import Process
import time
import random
from Config import Config
import logging

#画面表示用テンプレートHTMLのファイル名
LOGIN_TEMPLATE_NAME = 'login.html' #ログイン画面
HOME_TEMPLATE_NAME = 'home.html' #タイムライン表示用

conf = Config()
CONSUMER_KEY = conf.CONSUMER_KEY
CONSUMER_SECRET = conf.CONSUMER_SECRET
CALLBACK_URL = conf.CALLBACK_URL

logger = logging.getLogger(__name__)

def RedirectHome():
    return HttpResponseRedirect(reverse('tw.views.index'))

def isAuthorized(request):
    key = request.session.get('key')
    secret = request.session.get('secret')
    return (key and secret)

def getApi(key, secret):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(key, secret)
    return tweepy.API(auth_handler=auth)

def index(request):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    if not isAuthorized(request):
        return render_to_response(LOGIN_TEMPLATE_NAME)
    key = request.session.get('key')
    secret = request.session.get('secret')
    auth.set_access_token(key, secret)
    api = tweepy.API(auth_handler=auth)

    username = auth.get_username()
    me = api.me()
    timeline_list = api.home_timeline()
    ctxt = RequestContext(request, {
        'IsMyHome': True,
        'MyScreenName': me.screen_name,
        'OwnerName': me.name,
        'OwnerScreenName': me.screen_name,
        'OwnerProfileImage': me.profile_image_url_https,
        'OwnerDiscription': me.description,
        'Result': timeline_list
    })

    return render_to_response(HOME_TEMPLATE_NAME, ctxt)

def login(request):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)
    try:
        auth_url = auth.get_authorization_url()
    except tweepy.TweepError:
        return RedirectHome()

    request.session['request_token'] = (auth.request_token.key, auth.request_token.secret)
    return HttpResponseRedirect(auth_url)

def get_callback(request):
    verifier = request.GET.get('oauth_verifier')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    token = request.session.get('request_token')
    del request.session['request_token']
    auth.set_request_token(token[0], token[1])

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        return RedirectHome()

    request.session['key'] = auth.access_token.key
    request.session['secret'] = auth.access_token.secret

    api = tweepy.API(auth_handler=auth)
    me = api.me()
    logger.info("screen_name:%s login" % (me.screen_name,))

    return RedirectHome()

def lazyPost(text, key, secret):
    lazy = Config().LAZY
    lazyTime = random.randint(lazy[0], lazy[1])
    api = getApi(key, secret)
    logger.info("screen_name:%s lazy(sec):%d" % (api.me().screen_name, lazyTime))
    time.sleep(lazyTime)
    postTweet(text, key, secret)

def postTweet(tweet, key, secret):
    api = getApi(key, secret)
    api.update_status(tweet)
    logger.info("screen_name:%s tweet success" % (api.me().screen_name, ))

def post(request):
    if not (isAuthorized(request) and request.method == 'POST'):
        return RedirectHome()

    tweet = request.POST["tweet"]
    if tweet == "":
        return RedirectHome()

    key = request.session.get('key')
    secret = request.session.get('secret')

    p = Process(target=lazyPost, args=(tweet, key, secret))
    p.daemon = True
    p.start()
    return RedirectHome()

def delete(request, id):
    if isAuthorized(request):
        api = getApi(request.session.get('key'), request.session.get('secret'))
        tweet = api.get_status(id)
        tweet.destroy()
        logger.info("screen_name:%s tweet_id:%s delete" % (api.me().screen_name, id))
    return RedirectHome()

def friends(request, username):
    if not isAuthorized(request):
        return RedirectHome()

    key = request.session.get('key')
    secret = request.session.get('secret')
    api = getApi(key, secret)
    user = api.get_user(username)
    userTimeLine = user.timeline()

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    myName = api.me()

    ctxt = RequestContext(request, {
        'MyScreenName': myName.screen_name,
        'OwnerName': user.name,
        'OwnerScreenName': user.screen_name,
        'OwnerProfileImage': user.profile_image_url_https,
        'OwnerDiscription': user.description,
        'Result': userTimeLine
    })
    return render_to_response(HOME_TEMPLATE_NAME, ctxt)

def logout(request):
    api = getApi(request.session.get('key'), request.session.get('secret'))
    logger.info("screen_name:%s logout" % (api.me().screen_name, ))
    del request.session['key']
    del request.session['secret']
    return RedirectHome()
