import sets

import xlrd
import xlwt

# ----------------------------------------------------------------------
class ProcessIntercection:
    def __init__(self):
        self.path1 = ''
        self.path2 = ''
        self.keywordList1 = []
        self.keywordList2 = []
        self.keywordDict1 = {}
        self.keywordDict2 = {}
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
                keyword = str(first_sheet.cell(r, 2).value)
                categories = str(first_sheet.cell(r, 3).value)
                categoriesToAdd = categories.strip().lower();
                #print categoriesToAdd
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
            #print keywordList
            #print keywordDict
            return (keywordList, keywordDict)
        except:
            print 'An exception flew by!'
            raise


    def inputFileName(self, times):
        while True:
            try:
                path = raw_input("Please enter " + times + " Excel file name:")
                keywordList = self.open_file(path)
                if times == 'first':
                    self.path1 = path
                    (self.keywordList1, self.keywordDict1) = keywordList
                    #print self.keywordList1
                    #print self.keywordDict1
                elif times == 'second':
                    self.path2 = path
                    (self.keywordList2, self.keywordDict2) = keywordList
                    #print self.keywordList2
                    #print self.keywordDict2
                return
            except:
                print 'File name maybe wrong, please try again'


    def processData(self):
        try:
            set1 = sets.Set(self.keywordList1)
            set2 = sets.Set(self.keywordList2)
            keywordIntersection = set1.intersection(set2)
            #print keywordIntersection
            filename = raw_input("Please enter file name to save the results:")

            workbook = xlwt.Workbook(encoding = 'ascii')
            worksheet = workbook.add_sheet('Worksheet', cell_overwrite_ok=True)
            style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
            worksheet.write(0, 0, 'intersection keyword', style0)
            fileNm1 = self.path1.split('.')
            fileNm2 = self.path2.split('.')

            worksheet.write(0, 1, fileNm1[0] + ' category', style0)
            worksheet.write(0, 2, fileNm2[0] + ' category', style0)

            #f = open(filename, 'a')
            #f.write("---------------------" + self.path1 + " and " + self.path2 + " keyword intersection start--------------------------\n");
            #f.writelines(["%s\t%s\n" %(self.path1, self.path2)])
            keywordIntersectionList = list(keywordIntersection)
            keywordRowCount = len(keywordIntersectionList)
            #print keywordRowCount
            keywordRowStart = 0
            for idx in range(0, keywordRowCount):
                #f.writelines(["[%s]\n" % item])
                #print "idx=%d\n" %idx
                keywordRowStart = keywordRowStart + 1
                item = keywordIntersectionList[idx]
                #print item

                worksheet.write(keywordRowStart, 0, item)

                categoryList1 = self.keywordDict1.get(item)
                #print categoryList1
                categoryList2 = self.keywordDict2.get(item)
                #print categoryList2

                maxcount = max(len(categoryList1),len(categoryList2))
                #print maxcount
                categoryRowStart = keywordRowStart
                for i in range(0, maxcount):
                    #print "i=%d" %i
                    category1 = ' '
                    category2 = ' '
                    if i < len(categoryList1):
                        category1 = categoryList1[i]
                    if i < len(categoryList2):
                        category2 = categoryList2[i]
                    #print category1, category2


                    worksheet.write(categoryRowStart, 1, category1)
                    worksheet.write(categoryRowStart, 2, category2)
                    categoryRowStart = categoryRowStart + 1
                    keywordRowStart = categoryRowStart
            #print "here"
            workbook.save(filename)
            return True
        except:
            print 'File name maybe wrong, please try again'
            return False

# ----------------------------------------------------------------------
if __name__ == "__main__":
    ready = raw_input("Have you put Excel files in this folder? Please type Yes or No")
    if ready.lower() != 'yes':
        exit()
    while True:
        myProcess = ProcessIntercection()
        myProcess.inputFileName('first')
        myProcess.inputFileName('second')
        myProcess.processData()
        next = raw_input("Continue to compare? Please type Yes or No")
        if next.lower() != 'yes':
            exit()


