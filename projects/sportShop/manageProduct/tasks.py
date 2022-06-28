from celery import shared_task
from celery.utils.log import get_task_logger

from .instaPost.getAccessToken import getLongLivedAccessToken
from .instaPost.postCarousel import PostInstagramContent
from .instaPost.PrepareCapt import PrepareCaptionImage

import os

logger = get_task_logger(__name__)


@shared_task
def refreshAccessToken():

    getTokenObj = getLongLivedAccessToken()
    getTokenObj.doGetToken()


@shared_task
def postInsta():

    for x in range(3):

        prepObj = PrepareCaptionImage("http://quicksmart.pro")
        ls = prepObj.doPrepareCapt()

        img_urls = prepObj.doPrepareImgUrls()

        if ls is not None:

            caption = ls[0]
            props = ls[1]
            postObj = PostInstagramContent(caption,
                                           img_urls)

            postObj.createCarouselContainer()
            for prop in props:
                prop.insta_posted = True
                prop.save()

            logger.info("posted!")
        else:

            logger.info("No result!")
