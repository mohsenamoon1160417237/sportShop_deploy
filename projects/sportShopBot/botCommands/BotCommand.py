from pyromod import listen
from pyrogram.types import (ReplyKeyboardMarkup,
                            InlineKeyboardMarkup,
                            InlineKeyboardButton)


class BotCommand:

    def __init__(self, bot, msg):

        self.bot = bot
        self.msg = msg

    async def prepRepMarkTxt(self, ttl, options=None):

        if ttl == "choose":
            return "نوع عملیات را انتخاب کنید"

        elif ttl == "conf cat del":
            return "با حذف گروه تمام محصولات این گروه هم حذف می شوند. ادامه می دهید؟"

        elif ttl == "up img":
            return "تصویر را آپلود کنید:"

        elif ttl == "mk inpt":

            post = options[0]
            label = options[1]
            optional = options[2]

            if post is False:
                text = "{} جدید را وارد کنید(در صورتی که تمایل به تغییر {} ندارید عدد 1- را وارد کنید).".format(label,
                                                                                                                label)
            else:
                text = "{} را وارد کنید.".format(label)

            if optional is True:
                text += "در صورتی که می خواهید آن را خالی بگذارید عدد 2- را وارد کنید:"

            return text

        elif ttl == "del img":
            return "برای حذف تصویر عدد کنار آن را وارد کنید:"

    async def prepCatMainRepMark(self):

        reply_markup = ReplyKeyboardMarkup([
            ["نمایش لیست گروههای کالا"],
            ["افزودن گروه کالا"]
        ],
            one_time_keyboard=True,
            resize_keyboard=True
        )

        return reply_markup

    async def prepCatManRepMark(self):

        reply_markup = ReplyKeyboardMarkup([
            ["افزودن گروه"],
            ["نمایش لیست کالاهای گروه"],
            ["افزودن کالا به گروه"],
            ["اصلاح گروه", "حذف گروه"],
            ["افزودن سرگروه", "حذف سرگروه"],
            ["منوی اصلی", "بازگشت"]
        ],
            one_time_keyboard=True,
            resize_keyboard=True
        )

        return reply_markup

    async def prepConfDelCatRepMark(self):

        reply_markup = ReplyKeyboardMarkup([
            ["بله"],
            ["منوی اصلی", "بازگشت"]
        ],
            one_time_keyboard=True,
            resize_keyboard=True
        )

        return reply_markup

    async def prepProdManRepMark(self):

        reply_markup = ReplyKeyboardMarkup([
            ["اصلاح کالا", "حذف کالا"],
            ["اجازه دادن برای آپلود در اینستاگرام"],
            ["افزودن توضیح کالا", "مشاهده لیست توضیحات کالا"],
            ["افزودن ویژگی کالا", "مشاهده لیست ویژگی های کالا"],
            ["افزودن تصویر به کالا", "مشاهده لیست تصاویر کالا"],
            ["بازگشت", "منوی اصلی"]
        ],
            one_time_keyboard=True,
            resize_keyboard=True
        )

        return reply_markup

    async def prepProdAttrManRepMark(self):

        reply_markup = ReplyKeyboardMarkup([
            ["اصلاح توضیح", "افزودن توضیح"],
            ["حذف توضیح", "مشاهده لیست توضیحات"],
            ["بازگشت", "منوی اصلی"]
        ],
            one_time_keyboard=True,
            resize_keyboard=True
        )

        return reply_markup

    async def prepReturnRepMark(self):

        reply_markup = ReplyKeyboardMarkup([
            ["منوی اصلی", "بازگشت"]
        ],
            one_time_keyboard=True,
            resize_keyboard=True
        )

        return reply_markup

    async def prepProdPropManRepMark(self):

        reply_markup = ReplyKeyboardMarkup([
            ["اصلاح ویژگی", "افزودن ویژگی"],
            ["حذف ویژگی", "مشاهده لیست ویژگی ها"],
            ["بازگشت", "منوی اصلی"]
        ],
            one_time_keyboard=True,
            resize_keyboard=True
        )

        return reply_markup

    async def prepGetProdAttrInMark(self, ids):

        attr_id = ids[0]
        cat_id = ids[1]
        prod_id = ids[2]
        next_id = ids[3]
        prev_id = ids[4]

        reply_markup = InlineKeyboardMarkup([

            [InlineKeyboardButton(
                "مدیریت توضیح",
                callback_data="manage_attr_{}_{}_{}".format(attr_id,
                                                            cat_id,
                                                            prod_id)
            )],
            [
                InlineKeyboardButton(
                    "بعدی",
                    callback_data="next_attr_{}".format(next_id)
                ),
                InlineKeyboardButton(
                    "قبلی",
                    callback_data="prev_attr_{}".format(prev_id)
                )
            ],
            [InlineKeyboardButton(
                "بازگشت",
                callback_data="attr_back_{}_{}".format(cat_id,
                                                       prod_id)
            ),
                InlineKeyboardButton(
                    "منوی اصلی",
                    callback_data="menu"
                )]
        ])

        return reply_markup

    async def prepGetCatInMark(self, ids):

        cat_id = ids[0]
        next_id = ids[1]
        prev_id = ids[2]

        reply_markup = InlineKeyboardMarkup([

            [InlineKeyboardButton(
                "مدیریت گروه",
                callback_data="manage_cat_{}".format(cat_id)
            )],
            [InlineKeyboardButton(
                "بعدی",
                callback_data="next_cat_{}".format(next_id)
            ),
                InlineKeyboardButton(
                    "قبلی",
                    callback_data="prev_cat_{}".format(prev_id)
                )],

            [InlineKeyboardButton(
                "منوی اصلی",
                callback_data="menu"
            )
            ]
        ]
        )

        return reply_markup

    async def prepGetCatParInMark(self, ids):

        cat_id = ids[0]
        par_id = ids[1]
        next_id = ids[2]
        prev_id = ids[3]

        reply_markup = InlineKeyboardMarkup([

            [InlineKeyboardButton(
                "انتخاب به عنوان سرگروه",
                callback_data="cat_par_{}_{}".format(cat_id, par_id)
            )],
            [InlineKeyboardButton(
                "بعدی",
                callback_data="next_cat_par_{}_{}".format(next_id,
                                                          cat_id)
            ),
                InlineKeyboardButton(
                    "قبلی",
                    callback_data="prev_cat_par_{}_{}".format(prev_id,
                                                              cat_id)
                )],

            [InlineKeyboardButton(
                "منوی اصلی",
                callback_data="menu"
            )
            ]
        ]
        )

        return reply_markup

    async def prepGetProdInMark(self, ids):

        cat_id = ids[0]
        prod_id = ids[1]
        next_id = ids[2]
        prev_id = ids[3]

        reply_markup = InlineKeyboardMarkup([

            [InlineKeyboardButton(
                "مدیریت کالا",
                callback_data="manage_prod_{}_{}".format(cat_id,
                                                         prod_id)
            )],
            [
                InlineKeyboardButton(
                    "بعدی",
                    callback_data="next_prod_{}".format(next_id)
                ),
                InlineKeyboardButton(
                    "قبلی",
                    callback_data="prev_prod_{}".format(prev_id)
                )
            ],
            [InlineKeyboardButton(
                "بازگشت",
                callback_data="prod_back_{}".format(cat_id)
            ),
                InlineKeyboardButton(
                    "منوی اصلی",
                    callback_data="menu"
                )]
        ]
        )

        return reply_markup

    async def prepGetProdPropInMark(self, ids):

        prop_id = ids[0]
        cat_id = ids[1]
        prod_id = ids[2]
        next_id = ids[3]
        prev_id = ids[4]

        reply_markup = InlineKeyboardMarkup([

            [InlineKeyboardButton(
                "مدیریت ویژگی",
                callback_data="manage_prop_{}_{}_{}".format(prop_id,
                                                            cat_id,
                                                            prod_id)
            )],
            [
                InlineKeyboardButton(
                    "بعدی",
                    callback_data="next_prop_{}".format(next_id)
                ),
                InlineKeyboardButton(
                    "قبلی",
                    callback_data="prev_prop_{}".format(prev_id)
                )
            ],
            [InlineKeyboardButton(
                "بازگشت",
                callback_data="prop_back_{}_{}".format(cat_id,
                                                       prod_id)
            ),
                InlineKeyboardButton(
                    "منوی اصلی",
                    callback_data="menu"
                )]
        ]
        )

        return reply_markup

    async def sendMsg(self, text, ttl=None, ids=None):

        reply_markup = None

        if ttl is not None:
            if ttl == "get attr":
                reply_markup = await self.prepGetProdAttrInMark(ids)

            elif ttl == "get cat":
                reply_markup = await self.prepGetCatInMark(ids)

            elif ttl == "get cat par":
                reply_markup = await self.prepGetCatParInMark(ids)

            elif ttl == "get prod":
                reply_markup = await self.prepGetProdInMark(ids)

            elif ttl == "get prop":
                reply_markup = await self.prepGetProdPropInMark(ids)

        await self.bot.send_message(self.msg.chat.id,
                                    text=text,
                                    reply_markup=reply_markup)

    async def askUser(self, ttl, img=False, options=None):

        if ttl == "cat main":
            reply_markup = await self.prepCatMainRepMark()
            text = await self.prepRepMarkTxt("choose")

        elif ttl == "cat manage":
            reply_markup = await self.prepCatManRepMark()
            text = await self.prepRepMarkTxt("choose")

        elif ttl == "conf cat del":
            reply_markup = await self.prepConfDelCatRepMark()
            text = await self.prepRepMarkTxt("conf cat del")

        elif ttl == "prod manage":
            reply_markup = await self.prepProdManRepMark()
            text = await self.prepRepMarkTxt("choose")

        elif ttl == "attr manage":
            reply_markup = await self.prepProdAttrManRepMark()
            text = await self.prepRepMarkTxt("choose")

        elif ttl == "img manage":
            reply_markup = await self.prepReturnRepMark()
            text = await self.prepRepMarkTxt("up img")

        elif ttl == "prop manage":
            reply_markup = await self.prepProdPropManRepMark()
            text = await self.prepRepMarkTxt("choose")

        elif ttl == "mk inpt":
            reply_markup = await self.prepReturnRepMark()
            text = await self.prepRepMarkTxt("mk inpt", options)

        elif ttl == "del img":
            reply_markup = await self.prepReturnRepMark()
            text = await self.prepRepMarkTxt("del img")

        input = await self.bot.ask(self.msg.chat.id,
                                   text,
                                   reply_markup=reply_markup)
        if img is True:
            return input

        return input.text

    async def sendPhoto(self, photo, caption):

        await self.bot.send_photo(chat_id=self.msg.chat.id,
                                  photo=photo,
                                  caption=caption)
