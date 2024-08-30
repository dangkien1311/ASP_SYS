class Slot:
    def __init__(self, ID, ShipId, BayId, StackId, SlotId, SlotName, SlotType, SlotTotalSlot, SlotWeightLimit, SlotHeightLimit, SlotIndex):
        self.ID = ID
        self.ShipId = ShipId
        self.BayId = BayId
        self.StackId = StackId
        self.SlotId = SlotId
        self.SlotName = SlotName
        self.SlotType = SlotType
        self.SlotIndex = SlotIndex

import openpyxl
def getSlot (url, numSlot):
    url = '/home/code/SYS_ASP/Data/Slot.xlsx'
    res = [];

    wb = openpyxl.load_workbook(url);
    sheet = wb['Slot'];
    maxRow = sheet.max_row;
    #if numSlot > maxRow:
    #    return res;
    #get data all slot
    allSlot =[]
    for i in range(2, maxRow+1 ):
        cellId = sheet['E' + str(i)];
        if cellId.value is None:
            continue
        cellStackId = sheet['D' + str(i)];
        cellSlotType = sheet['G' + str(i)];
        cellSlotNumRF = sheet['I' + str(i)];
        allSlot.append([cellId.value, cellStackId.value,cellSlotType.value, cellSlotNumRF.value]);
    # get data slot in stack
    #for i in listStack:
        #listSlot = [ j[0] for j in allSlot if j[1] == i];
        #res.append(listSlot);
    res = allSlot;
    return res;