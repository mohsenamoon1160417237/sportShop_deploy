from ..helpers.postCarousel import PostInstagramContent
from ..helpers.PrepareCapt import PrepareCaptionImage

from time import sleep


class PostInsta:

    def __init__(self, logger):

        self.logger = logger

    def do_task(self):

        for x in range(3):

            prepObj = PrepareCaptionImage("http://quicksmart.pro")
            ls = prepObj.doPrepareCapt()

            img_urls = prepObj.doPrepareImgUrls()

            if ls is not None:

                caption = ls[0]
                not_posted_props = ls[1]
                postable_props = ls[2]

                print(not_posted_props.count())
                print(postable_props.count())

                if postable_props.count() != 0:

                    postObj = PostInstagramContent(caption,
                                                   img_urls)

                    postObj.createCarouselContainer()

                    for prop in postable_props:
                        prop.insta_posted = True
                        prop.save()

                    self.logger.info("posted!")

                else:
                    self.logger.info("No result!")

            elif ls is None:

                self.logger.info("No result!")

            sleep(10)
