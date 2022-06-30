from projects.sportShop.manageProduct.instaPost.helpers.postCarousel import PostInstagramContent
from projects.sportShop.manageProduct.instaPost.helpers.PrepareCapt import PrepareCaptionImage

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

                postObj = PostInstagramContent(caption,
                                               img_urls)

                postObj.createCarouselContainer()

                for prop in postable_props:
                    prop.insta_posted = True
                    prop.save()

                if not_posted_props.count() <= 3:

                    prop = not_posted_props.first()
                    product = prop.product
                    product.insta_perm = False
                    product.save()

                self.logger.info("posted!")

            else:

                self.logger.info("No result!")

            sleep(600)
