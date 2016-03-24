file = open('100_power_list.txt', 'r')
for line in file.readlines():
    print line.replace(" ", "")