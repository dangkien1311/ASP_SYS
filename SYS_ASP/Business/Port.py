class Port(object):

    def __init__(self, ID, PortId, PortName,PortTotalSlot, PortIndex):
        self.ID = ID
        self.PortId = PortId
        self.PortName = PortName
        self.PortTotalSlot = PortTotalSlot
        self.PortIndex = PortIndex

import openpyxl
def getPort (url, numPort):
    url = 'SYS_ASP\Data\Port.xlsx'
    res = [];

    wb = openpyxl.load_workbook(url);
    sheet = wb['Port'];
    maxRow = sheet.max_row;
    if numPort > maxRow:
        numPort = maxRow;
    #    return res;
    #get data stack
    for i in range(2, numPort+1 ):
        cellId = sheet['A' + str(i)];
        res.append(cellId.value);
    return res;