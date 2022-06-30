from celery import shared_task
from celery.utils.log import get_task_logger

from instaPost.tasks.getAccessToken import getLongLivedAccessToken
from instaPost.tasks.post_insta import PostInsta


logger = get_task_logger(__name__)


@shared_task
def refreshAccessToken():

    getTokenObj = getLongLivedAccessToken(logger)
    getTokenObj.do_task()


@shared_task
def postInsta():

    post_ins = PostInsta(logger)
    post_ins.do_task()

