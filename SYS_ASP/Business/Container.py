class Container:
    def __init__(self, ID, StackId, SlotId, ContId, ContName,ContType,ContHeight, ContWeight, PortUnload, PortOnShip):
        self.ID = ID
        self.StackId = StackId
        self.SlotId = SlotId
        self.ContId = ContId
        self.ContName = ContName
        self.ContType = ContType
        self.ContHeight= ContHeight
        self.ContWeight = ContWeight
        self.PortUnload = PortUnload
        self.PortOnShip = PortOnShip

import openpyxl
def getContainer (url, numContainer):
    url = '/home/code/SYS_ASP/Data/Container.xlsx'
    res = []

    wb = openpyxl.load_workbook(url)
    sheet = wb['Container']
    maxRow = sheet.max_row
    if numContainer > maxRow:
        numContainer = maxRow
    #get data all slot
    allContainer =[]
    for i in range(2, numContainer+1 ):
        cellStackId = sheet['B' + str(i)]
        cellSlotId = sheet['C' + str(i)]
        cellId = sheet['D' + str(i)]
        cellContType = sheet['F' + str(i)]
        cellContWeight = sheet['H' + str(i)]
        cellContHeight = sheet['G' + str(i)]
        cellPortUnload = sheet['I' + str(i)]
        cellOnShip = sheet['J' + str(i)]
        cellReefer = sheet['K' + str(i)]
        cellOverLoad = sheet['L' + str(i)]
        allContainer.append([cellId.value, cellContType.value, cellContWeight.value, cellContHeight.value, cellPortUnload.value, cellReefer.value, cellOverLoad.value, cellOnShip.value, cellStackId.value, cellSlotId.value])
    # get data container of type
    #res = [ j[0] for j in allContainer if j[1] == containerType]
    res = allContainer
    return res

def loadingPort(contPortUnLoad, PortUnLoad):
    if contPortUnLoad == PortUnLoad:
        return 1
    return 0