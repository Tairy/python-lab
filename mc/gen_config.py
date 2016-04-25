# encoding: utf-8

file = open("db.txt")
target = open("target.txt", 'w+')

lines = file.readlines()
index = 0
positionY = 0
for line in lines:
    positionX = index % 9 + 1
    if(positionX == 1):
        positionY += 1
        if(positionY > 6):
            positionY %= 6

    lineInfo = line.split()
    index += 1
    target.write(
        "zl" + str(positionY) + str(positionX) + ":\n" +
        "\tCOMMAND:'op: pokegive {player} " + lineInfo[0] + " lvl1'\n" +
        "\tNAME: '&7 欢迎购买'\n" +
        "\tLORE:\n" +
        "\t- '" + lineInfo[1] + " 50 点卷'\n" +
        "\tID: 383\n" +
        "\tPOINTS: 50\n" +
        "\tKEEP-OPEN: true\n" +
        "\tPOSITION-X: " + str(positionX) + "\n" +
        "\tPOSITION-Y: " + str(positionY) + "\n"
    )