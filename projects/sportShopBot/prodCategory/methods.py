from api.sendReq import makeApiCall

from urls.mkUrl import prepareUrl

from botCommands.BotCommand import BotCommand

from prodCategory.parent import ProdCatparent
from prodMan.prod import ProdHandle

from utils.getInput import mkInpt
from utils.getProdItem import getProdItem
from utils.getCat import prGetText


class ProdCatMethods:

    def __init__(self, bot, msg, cli, main_menu, botCmdObj:BotCommand):

        self.bot = bot
        self.msg = msg
        self.cli = cli
        self.main_menu = main_menu
        self.botCmdObj = botCmdObj

    #liste tamame prod cat haye mojood
    async def doList(self):

        url = prepareUrl("cat list")
        cat = await getProdItem(self.botCmdObj,
                                url,
                                "cats",
                                tp='cat')
        if cat != "menu" and cat != "back" and cat != "empty":
            #await self.doGet(int(cat['id']))
            pass
        else:
            #agar khali bashad ya user gozineye eshtebah vared konad be menooye asli barmigardad
            await self.main_menu(self.cli, self.msg)

    #get kardane yek prod cat
    async def doGet(self, cat_id: int):

        url = prepareUrl("get or delete or edit cat", [cat_id])
        response = await makeApiCall(url, 'get')

        cat = response['cat']

        txt = await prGetText(cat)

        await self.botCmdObj.sendMsg(txt)

        #namayeshe gozine haye manage kardane prod category

        input = await self.botCmdObj.askUser("cat manage")

        if input == "نمایش لیست کالاهای گروه":
            prodMan = ProdHandle(self.bot, self.msg, self.cli, self.main_menu, cat_id, self, self.botCmdObj)
            await prodMan.doList()
        elif input == "افزودن کالا به گروه":
            prodMan = ProdHandle(self.bot, self.msg, self.cli, self.main_menu, cat_id, self, self.botCmdObj)
            await prodMan.doCreateUpdate(post=True)
        elif input == "افزودن گروه":
            await self.doCreateUpdate(post=True)
        elif input == "حذف گروه":
            await self.doDelete(cat_id)
        elif input == "اصلاح گروه":
            await self.doCreateUpdate(post=False, ttl=cat['title'], desc=cat['description'], cat=cat)
        elif input == "حذف سرگروه":
            prodCatPar = ProdCatparent(self.bot, self.msg, self.cli, self.main_menu, self, self.botCmdObj)
            await prodCatPar.remParent(cat['id'])
        elif input == "افزودن سرگروه":
            prodCatPar = ProdCatparent(self.bot, self.msg, self.cli, self.main_menu, self, self.botCmdObj)
            await prodCatPar.addParent(cat['id'])
        elif input == "منوی اصلی":
            await self.main_menu(self.cli, self.msg)
        else:
            await self.doList()

    async def doDelete(self, cat_id: int):

        url = prepareUrl("get or delete or edit cat", [cat_id])

        input = await self.botCmdObj.askUser("conf cat del")

        if input == "بله":

            await makeApiCall(url, 'delete')

            await self.botCmdObj.sendMsg("گروه درخواستی حذف شد.")
            await self.doList()
        elif input == "منوی اصلی":
            #agar user gozineye menooye asli ra vared konad barmigardad be menoye asli
            await self.main_menu(self.cli, self.msg)
        else:
            await self.doGet(cat_id)

    #ijad ya eslahe yek prod cat
    async def doCreateUpdate(self, post: bool, ttl=False, desc=False, cat=None):

        if post is True:
            text = "گروه جدید اضافه شد."
            url = prepareUrl("add cat")
        else:
            text = "گروه اصلاح شد."
            cat_id = int(cat['id'])
            url = prepareUrl("get or delete or edit cat", [cat_id])

        title = await mkInpt("عنوان", self.botCmdObj, value=ttl, post=post)
        if title != "menu" and title != "back":
            description = await mkInpt("شرح", self.botCmdObj, value=desc, post=post)
            if description != "menu" and description != "back":

                data = {"title": title,
                        "description": description}

                if post is True:

                    response = await makeApiCall(url, 'post', data)
                else:
                    response = await makeApiCall(url, 'put', data)

                cat = response['cat']

                await self.botCmdObj.sendMsg(text)
                #baad az anjame amaliiate eslah ya add kardane prod cat be tabee get kardane hamin prod cate jadid miravad.
                await self.doGet(int(response['cat']['id']))

            elif description == "menu":
                await self.main_menu(self.cli, self.msg)
            else:
                if post is True:
                    #agar ghasde anjame add category ra dashte bashad bad as vared kardane gozineye menu tavassote user
                    #be menooye aslie bot bar migardad.
                    await self.main_menu(self.cli, self.msg)
                else:
                    #agar ghasde anjame eslahe category ra dashte bashad bad as vared kardane gozineye bazgasht tavassote user
                    #be tabee get kardane cate mojood miravad.
                    await self.doGet(int(cat['id']))
        elif title == "menu":
            await self.main_menu(self.cli, self.msg)
        else:
            if post is True:
                await self.main_menu(self.cli, self.msg)
            else:
                await self.doGet(int(cat['id']))
