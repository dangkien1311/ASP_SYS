import openpyxl

class Stack:
    def __init__(self, ID, ShipId, BayId, StackId, StackName, StackType, StackTotalSlot, StackWeightLimit, StackHeightLimit, StackIndex, StackUsed):
        self.ID = ID
        self.ShipId = ShipId
        self.BayId = BayId
        self.StackId = StackId
        self.StackName = StackName
        self.StackType = StackType
        self.StackTotalSlot = StackTotalSlot
        self.StackWeightLimit = StackWeightLimit
        self.StackHeightLimit = StackHeightLimit
        self.StackIndex = StackIndex
        self.StackUsed = StackUsed

import openpyxl
def getStack (url, numStack):
    url = 'SYS_ASP\Data\Stack.xlsx'
    res = [];

    wb = openpyxl.load_workbook(url);
    sheet = wb['Stack'];
    maxRow = sheet.max_row;
    #if numStack > maxRow:
    #    return res;
    #get data stack
    for i in range(2, maxRow + 1 ):
        cellId = sheet['D' + str(i)];
        cellW = sheet['H' + str(i)];
        cellH = sheet['I' + str(i)];
        cellU = sheet['K' + str(i)];
        res.append([cellId.value, cellW.value, cellH.value, cellU.value]);
    return res;


