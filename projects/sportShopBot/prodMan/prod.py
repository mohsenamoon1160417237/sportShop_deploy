from api.sendReq import makeApiCall

from urls.mkUrl import prepareUrl

from utils.getProdItem import getProdItem
from utils.getInput import mkInpt
from utils.getProd import prpLsText

from prodMan.attr import ProdAttrHandle
from prodMan.prop import ProdPropHandle
from prodMan.img import ProdImgHandle

from botCommands.BotCommand import BotCommand

import asyncio


class ProdHandle:

    def __init__(self, bot, msg, cli, main_menu, cat_id: int, prodCatObj, botCmdObj:BotCommand):

        self.bot = bot
        self.msg = msg
        self.cli = cli
        self.main_menu = main_menu
        self.cat_id = cat_id
        self.prodCatObj = prodCatObj
        self.botCmdObj = botCmdObj

    async def doCreateUpdate(self, post: bool,  title=False, note=False, prod=None):

        if post is True:
            text = "کالای جدید اضافه شد."
            url = prepareUrl("add prod", [self.cat_id])
        else:
            text = "کالا اصلاح شد."
            prod_id = int(prod['id'])
            url = prepareUrl("edit prod", [self.cat_id, prod_id])

        title = await mkInpt("عنوان", self.botCmdObj, value=title, post=post)
        if title != "menu" and title != "back":
            note = await mkInpt("شرح", self.botCmdObj, value=note, post=post)
            if note != "menu" and note != "back":

                data = {"title": title,
                        "note": note}

                if post is True:
                    response = await makeApiCall(url, 'post', data)
                else:
                    response = await makeApiCall(url, 'put', data)

                prod_id = int(response['product']['id'])

                await self.botCmdObj.sendMsg(text)
                await self.chooseOpt(prod_id, self.cat_id)

            elif note == "back":
                if post is True:
                    await self.prodCatObj.doGet(self.cat_id)
                else:
                    await self.doList()
            else:
                await self.main_menu(self.cli, self.msg)
        elif title == "back":
            if post is True:
                await self.prodCatObj.doGet(self.cat_id)
            else:
                await self.doList()
        else:
            await self.main_menu(self.cli, self.msg)

    async def doList(self):

        #liste tamame prod haye in cat
        url = prepareUrl("prod list", [self.cat_id])

        #entekhabe yek prod va raftan be tabee chooseOpt e aan prod
        prod = await getProdItem(self.botCmdObj,
                                 url,
                                 "products",
                                 tp="prod")

        if prod != "menu" and prod != "back" and prod != "empty":
            #await self.chooseOpt(prod, self.cat)
            pass
        elif prod == "empty":
            await self.prodCatObj.doGet(self.cat_id)

    async def chooseOpt(self, prod_id, cat_id):

        url = prepareUrl("get or delete prod", [prod_id])
        response = await makeApiCall(url, 'get')

        self.prod = response['product']
        prod = self.prod

        txt = await prpLsText(prod)
        await self.botCmdObj.sendMsg(txt)

        #namayeshe gozinehaye mojood baraye manage kardane prod.
        input = await self.botCmdObj.askUser("prod manage")

        if input == "اصلاح کالا":
            await self.doCreateUpdate(post=False, title=prod['title'], note=prod['note'], prod=prod)
        elif input == "حذف کالا":
            await self.doDelete(int(prod['id']))
        elif input == "مشاهده لیست توضیحات کالا":
            prodAttr = ProdAttrHandle(self.bot, self.msg, self.cli, self.main_menu, prod_id, cat_id, self, self.botCmdObj)
            await prodAttr.doList()
        elif input == "افزودن توضیح کالا":
            prodAttr = ProdAttrHandle(self.bot, self.msg, self.cli, self.main_menu, prod_id, cat_id, self, self.botCmdObj)
            await prodAttr.doCreateUpdate(post=True)
        elif input == "مشاهده لیست ویژگی های کالا":
            prodProp = ProdPropHandle(self.bot, self.msg, self.cli, self.main_menu, prod_id, cat_id, self, self.botCmdObj)
            await prodProp.doList()
        elif input == "افزودن ویژگی کالا":
            prodProp = ProdPropHandle(self.bot, self.msg, self.cli, self.main_menu, prod_id, cat_id, self, self.botCmdObj)
            await prodProp.doCreateUpdate(post=True)
        elif input == "افزودن تصویر به کالا":
            prodImg = ProdImgHandle(self.bot, self.msg, self.cli, self.main_menu, prod_id, cat_id, self, self.botCmdObj)
            await prodImg.doUpload()
        elif input == "مشاهده لیست تصاویر کالا":
            prodImg = ProdImgHandle(self.bot, self.msg, self.cli, self.main_menu, prod_id, cat_id, self, self.botCmdObj)
            await prodImg.doList()
        elif input == "اجازه دادن برای آپلود در اینستاگرام":
            await self.addInstaPerm(int(prod['id']))
        elif input == "بازگشت":
            await self.doList()
        else:
            await self.main_menu(self.cli, self.msg)

    async def doDelete(self, prod_id: int):

        url = prepareUrl("get or delete prod", [prod_id])
        response = await makeApiCall(url, 'delete')

        await self.botCmdObj.sendMsg("کالا حذف شد.")
        await self.doList()

    async def addInstaPerm(self, prod_id: int):

        url = prepareUrl("add prod insta perm", [prod_id])
        response = await makeApiCall(url, 'post')

        if response['status'] == "Not enough jpg images":

            await self.botCmdObj.sendMsg("تعداد عکس های با فرمت jpg کالا کمتر از ۲ عدد است.")
            await asyncio.sleep(2)

        else:

            await self.botCmdObj.sendMsg("اجازه اضافه شد")

        await self.chooseOpt(prod_id, self.cat_id)
