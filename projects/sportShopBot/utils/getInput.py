from botCommands.BotCommand import BotCommand


async def mkInpt(label, botCmdObj:BotCommand, post=False, value=False, optional=False):

    inpt = await botCmdObj.askUser("mk inpt", options=[post, label, optional])

    if inpt == "منوی اصلی":
        return "menu"
    elif inpt == "بازگشت":
        return "back"
    elif inpt == "-1":
        inpt = value
    elif inpt == "-2":
        inpt = None

    return inpt
