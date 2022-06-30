from ...models.defineProduct import DefineProduct
from ...models.productProp import ProductProp
from ...models.productAttr import ProductAttr
from ...models.galleryImage import GalleryImage

from django.db.models import Count, Q


class PrepareCaptionImage:

    def __init__(self, domain):

        self.domain = domain

    def get_prod(self):

        an_prods = DefineProduct.objects.annotate(props_posted_count=Count('props',
                                                                           filter=Q(props__insta_posted=True)))
        prods = an_prods.filter(props_posted_count__gt=0,
                                insta_perm=True)

        if not prods.exists():
            prods = an_prods.filter(insta_perm=True)
            if not prods.exists():
                print("no product")
                return None
        return prods.first()

    def get_not_posted_props(self, prod):

        if prod is None:
            return None

        not_posted_props = ProductProp.objects.filter(product=prod,
                                                      insta_posted=False)
        return not_posted_props

    def prepProdText(self, prod):

        cat = prod.cat
        cat_title = "💥🥎 " + cat.title + " 💥🥎"
        cat_note = cat.description

        prod_title = prod.title
        prod_desc = prod.note

        return [cat_title, cat_note, prod_title, prod_desc]

    def prepText(self, props, product):

        txtLs = self.prepProdText(product)

        cat_title = txtLs[0] + "\n\n"
        cat_note = txtLs[1] + "\n\n"
        prod_title = txtLs[2] + "\n\n"
        prod_desc = txtLs[3] + "\n\n"

        attrs = ProductAttr.objects.filter(product=product)

        if not attrs.exists():
            attrs_text = ""
        else:
            attrs_text = "\n"

            for attr in attrs:

                key =attr.key + " : "
                value = attr.value + " 📌" + "\n"
                if attr.note is None:
                    note = "\n"
                else:
                    note = attr.note + "\n\n"

                attr_text = key + value + note
                attrs_text += attr_text

        props_text = "مشخصات :" + "\n\n" + "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰" + "\n\n"

        for prop in props:

            if prop.weight is None:
                weight = ""
            else:
                weight = "وزن: " + str(prop.weight) + " ⚖ ️" + "\n\n"

            if prop.size is None:
                size = ""
            else:
                size = "سایز: " + str(prop.size) + " 📏 " + "\n\n"

            if prop.color is None:
                color = ""
            else:
                color = "رنگ: " + prop.color + " 🎨 " + "\n\n"
            line = "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n"
            prop_text = weight + size + color + line
            props_text += prop_text

        price = "قیمت: دایرکت یا واتساپ" + " 💰 " + "\n\n"
        price += "09121231234" + " 📲 " + "\n\n"

        order = "برای سفارش می توانید به دایرکت مراجعه و یا با شماره بالا تماس بگیرید" + "\n" + " 🎁😉 "

        fin_text = cat_title + cat_note + prod_title + attrs_text + props_text + prod_desc + price + order

        return fin_text

    def doPrepareCapt(self):

        prod = self.get_prod()

        if prod is None:
            return None

        not_posted_props = self.get_not_posted_props(prod)

        if not_posted_props is None:
            print("no props")
            return None

        if not_posted_props.count() > 3:
            postable_props = not_posted_props[:3]
        else:
            postable_props = not_posted_props

        txt = self.prepText(postable_props, prod)

        return [txt, not_posted_props, postable_props]

    def create_img_url(self, url):

        return self.domain + url

    def doPrepareImgUrls(self):

        prod = self.get_prod()
        if prod is None:
            return None

        imgs = GalleryImage.objects.filter(Q(format="jpg") |
                                           Q(format="jpeg"),
                                           product=prod)
        if not imgs.exists():
            return ["https://cdn.pixabay.com/photo/2015/04/19/08/32/marguerite-729510_1280.jpg",
                    "https://cdn.pixabay.com/photo/2015/04/19/08/32/marguerite-729510_1280.jpg"]
        else:
            img_urls = []

            if imgs.count() > 10:

                imgs = imgs[:10]

            for img in imgs:

                img_url = self.create_img_url(img.image.url)
                img_urls.append(img_url)

            return img_urls
