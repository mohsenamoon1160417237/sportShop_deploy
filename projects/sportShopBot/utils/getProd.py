from urls.mkUrl import prepareUrl

from api.sendReq import makeApiCall

from botCommands.BotCommand import BotCommand


async def prpLsText(prod):

    intro = "کالا"
    title = "عنوان: " + "\n" + prod['title']
    prod_note = "شرح: " + "\n" + prod['note'] + "\n\n" +\
                ".............................................................." + "\n"

    if len(prod['attrs']) == 0:
        attrs = "-"
    else:
        attrs = ""

        for num, attr in enumerate(prod['attrs']):

            number = str(num + 1) + ":"
            #key = "عنوان: " + "\n" + attr['key']
            key = attr['key'] + ":"
            #value = "شرح: " + "\n" + attr['value']
            value = attr['value']
            if attr['note'] is None:
                attr['note'] = "-"
            note = "شرح اضافی: " + "\n" + attr['note']

            obj = number + "\n\n" + key + "\t" + value + "\n\n" + note + "\n\n"
            attrs += obj + "\n\n"

    if attrs == "-":
        attr_spc = "\n\n"
    else:
        attr_spc = ""
    attrs = "توضیحات:" + "\n\n" + attrs + attr_spc + \
            ".............................................................." + "\n"

    if len(prod['props']) == 0:
        props = "-"
    else:
        props = ""

        for num, prop in enumerate(prod['props']):

            number = str(num + 1) + ":"
            if prop['weight'] is None:
                prop['weight'] = "-"
            weight = "وزن: " + "\n" + str(prop['weight'])
            if prop['size'] is None:
                prop['size'] = "-"
            size = "سایز: " + "\n" + str(prop['size'])
            if prop['color'] is None:
                prop['color'] = "-"
            color = "رنگ: " + "\n" + prop['color']
            price = "قیمت: " + "\n" + str(prop['price'])
            stock_count = "موجودی انبار: " + "\n" + str(prop['stock_count'])
            pre_order_count = "تعداد پیش فروش: " + "\n" + str(prop['pre_order_count'])

            obj = number + "\n\n" + weight + "\n\n" + size + "\n\n" + color + "\n\n" +\
                  price + "\n\n" + stock_count + "\n\n" + pre_order_count + "\n\n"
            props += obj + "\n\n"

    if props == "-":
        props_spc = "\n\n"
    else:
        props_spc = ""

    props = "ویژگی ها" + "\n\n" + props + props_spc + \
            ".............................................................." + "\n"

    txt = intro + "\n\n" + title + "\n\n" + prod_note + "\n\n" + attrs + "\n\n" + props
    return txt


async def getProd(prod_id: int, botCmdObj:BotCommand):

    url = prepareUrl("get or delete prod", [prod_id])

    response = await makeApiCall(url, 'get')

    prod = response['product']
    cat_id = int(prod['cat_id'])

    next_id = prod['next_id']
    if next_id is None:
        next_id = 'none'

    prev_id = prod['prev_id']
    if prev_id is None:
        prev_id = 'none'

    txt = await prpLsText(prod)

    await botCmdObj.sendMsg(txt, "get prod", [cat_id, prod_id, next_id, prev_id])
