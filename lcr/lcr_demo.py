# I had to install selenium and webdriver-manager

from lcr import API as LCR

lcr = LCR("<LDS USERNAME>", "<LDS PASSWORD>", 222976)

months = 5
move_ins = lcr.members_moved_in(months)

for member in move_ins:
    print("{}: {}".format(member['spokenName'], member['textAddress']))