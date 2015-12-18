import sets

import xlrd
import xlwt
import re
import os


# ----------------------------------------------------------------------
class ProcessIntercection:
    def __init__(self, type, processType):
        self.path = []
        self.keywordList = {}
        self.keywordDict = {}
        self.type = type
        self.processType = processType

    def open_file(self, path):

        """
        Open and read an Excel file
        """
        try:
            book = xlrd.open_workbook(path)
            # get the first worksheet
            first_sheet = book.sheet_by_index(0)
            keywordList = []
            keywordDict = {}
            for r in range(1, first_sheet.nrows):
                #print first_sheet.cell(r, 2).value
                keyword = first_sheet.cell(r, 2).value
                #print keyword
                categories = first_sheet.cell(r, 3).value
                #print categories
                categoriesToAdd = categories.strip().lower();
                # print categoriesToAdd
                keywords = keyword.split(';')
                for currentKeyword in keywords:
                    keywordForAdd = currentKeyword.strip().lower();
                    if keywordForAdd and keywordForAdd != 'Keywords':
                        keywordList.append(keywordForAdd)
                        original_list = keywordDict.get(keywordForAdd)
                        if not original_list:
                            original_list = []
                        if categoriesToAdd not in set(original_list):
                            original_list.append(categoriesToAdd)
                            keywordDict[keywordForAdd] = original_list
            # print keywordList
            # print keywordDict
            return (keywordList, keywordDict)
        except:
            print 'An exception flew by!'
            raise

    def open_file_category(self, path):

        """
        Open and read an Excel file
        """
        try:
            book = xlrd.open_workbook(path)
            # get the first worksheet
            first_sheet = book.sheet_by_index(0)
            keywordList = []
            keywordDict = {}
            for r in range(1, first_sheet.nrows):
                # print first_sheet.cell(r, 2).value
                keywordForRe = first_sheet.cell(r, 3).value
                p = re.compile(r'\([^)]*\)')
                keyword = re.sub(p, '', keywordForRe)
                # print keyword
                categories = first_sheet.cell(r, 2).value
                # print categories
                categoriesToAdd = categories.strip().lower();
                # print categoriesToAdd
                keywords = keyword.split(';')
                for currentKeyword in keywords:
                    keywordForAdd = currentKeyword.strip().lower();
                    if keywordForAdd and keywordForAdd != 'Keywords':
                        keywordList.append(keywordForAdd)
                        original_list = keywordDict.get(keywordForAdd)
                        if not original_list:
                            original_list = []
                        if categoriesToAdd not in set(original_list):
                            original_list.append(categoriesToAdd)
                            keywordDict[keywordForAdd] = original_list
            # print keywordList
            # print keywordDict
            return (keywordList, keywordDict)
        except:
            print 'An exception flew by!'
            raise
    def getAllFileNames(self):
        filenameList = []
        for (dirpath, dirnames, filenames) in os.walk(os.curdir):
            break
        for f in filenames:
            filename, file_extension = os.path.splitext(f)
            #print filename
            #print file_extension
            if file_extension == '.xlsx':
                filenameList.append(f)

        return filenameList

    def inputFileName(self):
        try:
            pathList = []
            if self.processType == 'no':
                path = raw_input("Please enter Excel file name:")
                pathList.append(path)
            elif self.processType == 'yes':
                pathList = self.getAllFileNames()
            #print pathList
            for path in pathList:
                keywordList = ()
                if self.type == 'keyword':
                    keywordList = self.open_file(path)
                elif self.type == 'category':
                    keywordList = self.open_file_category(path)

                fileName_ = path.split('.')
                # print fileName_
                self.path.append(fileName_[0])
                # print self.path

                self.keywordList[fileName_[0]], self.keywordDict[fileName_[0]] = keywordList
            return
        except Exception, e:
            print 'File maybe wrong, please try again', e

    def intersect(self, lists):
        if (len(lists) <= 1):
            return lists[0]

        return list(set.intersection(*map(set, lists)))

    def processKeyWordData(self):
        try:
            keyLists = []
            for filename in self.path:
                keyLists.append(self.keywordList[filename])
            keywordIntersection = self.intersect(keyLists)

            # print len(keywordIntersection)

            filename = raw_input("Please enter file name to save the results:")

            workbook = xlwt.Workbook(encoding='utf-8')
            style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
            worksheet = workbook.add_sheet(type, cell_overwrite_ok=True)
            worksheet.write(0, 0, 'intersection ' + self.type, style0)

            fileCount = len(self.path)
            for j in range(0, fileCount):
                if self.type == 'keyword':
                    worksheet.write(0, j + 1, self.path[j] + ' category', style0)
                elif self.type == 'category':
                    worksheet.write(0, j + 1, self.path[j] + ' keyword', style0)
            keywordIntersectionList = keywordIntersection
            keywordRowCount = len(keywordIntersectionList)
            keywordRowStart = 0
            for idx in range(0, keywordRowCount):
                keywordRowStart = keywordRowStart + 1
                item = keywordIntersectionList[idx]
                worksheet.write(keywordRowStart, 0, item)
                categoryFileList = []
                for filenm in self.path:
                    categoryList = self.keywordDict[filenm].get(item)
                    # print categoryList
                    categoryFileList.append(categoryList)
                maxcount = max(len(l) for l in categoryFileList)
                worksheet.write(keywordRowStart, 0, item + '  (max:' + str(maxcount) + ')')
                # print maxcount
                categoryRowStart = keywordRowStart + 1
                for i in range(0, maxcount):
                    categoryColumnStart = 1
                    for categoryList in categoryFileList:
                        category = ' '
                        if i < len(categoryList):
                            category = categoryList[i]
                        worksheet.write(keywordRowStart, categoryColumnStart, len(categoryList))
                        worksheet.write(categoryRowStart, categoryColumnStart, category)
                        categoryColumnStart = categoryColumnStart + 1
                    categoryRowStart = categoryRowStart + 1
                    keywordRowStart = categoryRowStart
            workbook.save(filename)

            return True
        except:
            print 'File name maybe wrong, please try again'
            return False


# ----------------------------------------------------------------------
if __name__ == "__main__":
    '''
    ready = raw_input("Have you put Excel files in this folder? Please type Yes or No")
    if ready.lower() != 'yes':
        exit()
    '''
    type = ''
    while True:
        type = raw_input("What type of intersection? Please type keyword or category")
        if type.strip().lower() != 'category' and type != 'keyword':
            continue;
        break;

    processType = raw_input("Do you want to process all *.xlsx files? Please type Yes or No or Exit")
    myProcess = ProcessIntercection(type.strip().lower(), processType.strip().lower())
    if processType.lower() == 'no':
        while True:
            myProcess.inputFileName()
            continueLoad = raw_input("Continue add more files? Please type Yes or No")
            if continueLoad.lower() != 'yes':
                break
    elif processType.lower() == 'yes':
        myProcess.inputFileName()
    else:
        exit()

    myProcess.processKeyWordData()
