def engToPersNum(num):

    persNums = ["۰","۱","۲","۳","۴","۵","۶","۷","۸","۹"]

    spNum = str(num)

    for count, n in enumerate(spNum):

        if n == '1':
            spNum = spNum.replace(spNum[count], persNums[1])
        elif n == '2':
            spNum = spNum.replace(spNum[count], persNums[2])
        elif n == '3':
            spNum = spNum.replace(spNum[count], persNums[3])
        elif n == '4':
            spNum = spNum.replace(spNum[count], persNums[4])
        elif n == '5':
            spNum = spNum.replace(spNum[count], persNums[5])
        elif n == '6':
            spNum = spNum.replace(spNum[count], persNums[6])
        elif n == '7':
            spNum = spNum.replace(spNum[count], persNums[7])
        elif n == '8':
            spNum = spNum.replace(spNum[count], persNums[8])
        elif n == '9':
            spNum = spNum.replace(spNum[count], persNums[9])
        elif n == '0':
            spNum = spNum.replace(spNum[count], persNums[0])

    return spNum
