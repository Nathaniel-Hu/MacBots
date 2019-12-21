"""
------------------------------------------------------------------------------------------------------------------------
Programmer(s): Nathaniel Hu
Program Library Version: 0.1.0 (Developmental)
Last Updated: December 21th, 2019
------------------------------------------------------------------------------------------------------------------------
Program Library Description
[insert program library description]
------------------------------------------------------------------------------------------------------------------------
"""


# creates and manages profiles for each course added to MacGradeBot
class MacBotCourseProfileCreator:
    def __init__(self, courseName, courseCode, courseCredits):
        self.currentVersion = 0.1

        self.courseName = courseName
        self.courseCode = courseCode
        self.courseCredits = courseCredits

        # e.g. "Assignments", "Minor Assignments", "Major Assignments", "Projects", "Midterm Tests", "Final Exam"
        self.courseItemTypes = []
        # ["itemType", "itemName", "percent achieved", "percentage weight"]
        self.courseItemsMatrix = []

        self.courseItemsMatrix2 = {}

        self.courseAvg = float()
        self.coursePercentAchieved = float()
        self.coursePercentWeighted = float()
        self.course12pGPA = float()
        # percentage to 12-point GPA converter information
        self.percentGPA = (90.0, 85.0, 80.0, 77.0, 73.0, 70.0, 67.0, 63.0, 60.0, 57.0, 53.0, 50.0, 0.0)
        self.gradeGPA = (12.0, 11.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0)
        # user choices (for use by courseProfileMain method)
        self.userChoices = ['add', 'edit', 'avg', 'gpa', 'display', 'exit']

    # main method controlling class instance
    def courseProfileMain(self):
        print("Updating/Syncing Data...")
        if len(self.courseItemsMatrix2) == 0:
            self.dataUpdateSync()
        print("Data Successfully Updated/Synced.")

        while True:
            print("Welcome to the MacBot Course Profile Creator for {}!".format(self.courseName))
            userChoice = input("Would you like to add, edit, average, calculate gpa, display course profile or exit?: ")

            # adds new item to course item matrix
            if (userChoice == self.userChoices[0]) and (self.currentVersion == 0.0):
                itemType, itemName, percentAchieved, percentageWeight = self.inputCourseItemInfo()
                self.addCourseItem(itemType, itemName, percentAchieved, percentageWeight)

            # adds new item to reformatted course item matrix
            elif (userChoice == self.userChoices[0]) and (self.currentVersion > 0.0):
                itemType, itemName, percentAchieved, percentageWeight = self.inputCourseItemInfo()

                # checks if item type is already in reformatted course item matrix
                if itemType not in self.courseItemsMatrix2:
                    # creates new dictionary for new item type
                    self.courseItemsMatrix2[itemType] = {}

                # creates new data entry for item name in item type dictionary
                self.courseItemsMatrix2[itemType][itemName] = [percentAchieved, percentageWeight]

            # edits given item in course item matrix
            elif (userChoice == self.userChoices[1]) and (self.currentVersion == 0.0):
                for i in range(len(self.courseItemsMatrix)):
                    print('Index #: {} '.format(i), self.courseItemsMatrix[i])

                itemIndex = int(input("Input the index # of the item you would like to edit here: "))

                print("Current Item Info: ", self.courseItemsMatrix[itemIndex])

                itemType, itemName, percentAchieved, percentageWeight = self.editCourseItemInfo(itemIndex)

                self.editCourseItem(itemType, itemName, percentAchieved, percentageWeight, itemIndex)

            # edits given item in reformatted course item matrix
            elif (userChoice == self.userChoices[1]) and (self.currentVersion > 0.0):
                for type in self.courseItemsMatrix2:
                    for item in type:
                        print(item)

                oldItemType = input("Input the type of the item you would like to edit (e.g. midterm) here: ").lower()

                while oldItemType not in self.courseItemsMatrix2:
                    oldItemType = input("Sorry, but that item type does not exist. Please re-enter the type of the " +
                                        "item you would like to edit (e.g. midterm) here: ").lower()

                oldItemName = input("Input the item name (type {}) you would like to edit here: ".format(oldItemType))

                while oldItemName not in self.courseItemsMatrix2[oldItemName]:
                    oldItemName = input("Sorry, but that item type does not exist. Please re-enter the item name " +
                                        "(type {}) you would like to edit here: ".format(oldItemType))

                self.editCourseItem2(oldItemType, oldItemName, *self.editCourseItemInfo2(oldItemType, oldItemName))

            # calculates course average with original format data
            elif (userChoice == self.userChoices[2]) and (self.currentVersion == 0.0):
                self.calcCourseAvg()

            # calculates course average with updated format data
            elif (userChoice == self.userChoices[2]) and (self.currentVersion > 0.0):
                self.calcCourseAvg2()

            # calculates course 12-point GPA
            elif userChoice == self.userChoices[3]:
                self.calcCourse12pGPA()

            # displays course profile with original format data
            elif (userChoice == self.userChoices[4]) and (self.currentVersion == 0.0):
                self.displayCourseProfile()

            # displays course profile with updated format data
            elif (userChoice == self.userChoices[4]) and (self.currentVersion > 0.0):
                self.displayCourseProfile2()

            else:
                print("exiting course profile for course", self.courseName)
                break

    # allows user to input information for given course item
    def inputCourseItemInfo(self):
        itemType = input("Enter the item type (e.g. minor assignment, midterm) here: ").lower()
        itemName = input("Enter the name of the item (e.g. minor assignment #1) here: ").lower().capitalize()
        percentAchieved = float(eval(input("Enter your percent achieved (e.g. 100.0, 6/8 * 100) here: ")))
        percentageWeight = float(input("Enter the percentage weight of {} here: ".format(itemName)))
        return itemType, itemName, percentAchieved, percentageWeight

    # allows user to input information to edit in given course item
    def editCourseItemInfo(self, itemIndex):
        itemType = input("Enter the item type (e.g. minor assignment, midterm) here: ").lower()
        if itemType == "":
            itemType = self.courseItemsMatrix[itemIndex][0]

        itemName = input("Enter the name of the item (e.g. minor assignment #1) here: ").lower().capitalize()
        if itemName == "":
            itemName = self.courseItemsMatrix[itemIndex][1]

        try:
            percentAchieved = float(eval(input("Enter your percent achieved (e.g. 100.0, 6/8 * 100) here: ")))
        except SyntaxError:
            percentAchieved = self.courseItemsMatrix[itemIndex][2]

        try:
            percentageWeight = float(input("Enter the percentage weight of {} here: ".format(itemName)))
        except ValueError:
            percentageWeight = self.courseItemsMatrix[itemIndex][3]

        return itemType, itemName, percentAchieved, percentageWeight

    # allows user to input information to edit in given course item (for reformatted data entries)
    def editCourseItemInfo2(self, oldItemType, oldItemName):
        itemType = input("Enter the item type (e.g. minor assignment, midterm) here: ").lower()
        if itemType == "":
            itemType = oldItemType

        itemName = input("Enter the name of the item (e.g. minor assignment #1) here: ").lower().capitalize()
        if itemName == "":
            itemName = oldItemName

        try:
            percentAchieved = float(eval(input("Enter your percent achieved (e.g. 100.0, 6/8 * 100) here: ")))
        except SyntaxError:
            percentAchieved = self.courseItemsMatrix2[oldItemName][oldItemType][0]

        try:
            percentageWeight = float(eval(input("Enter your percent achieved (e.g. 100.0, 6/8 * 100) here: ")))
        except SyntaxError:
            percentageWeight = self.courseItemsMatrix2[oldItemName][oldItemType][1]

        return itemType, itemName, percentAchieved, percentageWeight

    # adds course item information entry to course items matrix
    def addCourseItem(self, itemType, itemName, percentAchieved=0.00, percentageWeight=0.00):
        self.courseItemsMatrix.append([itemType, itemName, percentAchieved, percentageWeight])

        if itemType not in self.courseItemTypes:
            self.courseItemTypes.append(itemType)

    # adds course item information entry to reformatted course items matrix
    def addCourseItem2(self, itemType, itemName, percentAchieved=0.00, percentWeight=0.00):
        if itemType not in self.courseItemsMatrix2:
            self.courseItemsMatrix2[itemType] = {}

        self.courseItemsMatrix2[itemType][itemName] = [percentAchieved, percentWeight]

    # edits course item information entry in course items matrix
    def editCourseItem(self, itemType, itemName, percentAchived, percentageWeight, itemIndex):
        self.courseItemsMatrix[itemIndex] = [itemType, itemName, percentAchived, percentageWeight]

        if itemType not in self.courseItemTypes:
            self.courseItemTypes.append(itemType)

        # deletes unused item types from course item types list
        for itemType in self.courseItemTypes:
            itemTypeCount = 0
            for item in self.courseItemsMatrix:
                if item[0] == itemType:
                    itemTypeCount += 1
            if itemTypeCount == 0:
                index = self.courseItemTypes.index(itemType)
                del self.courseItemTypes[index]

    # edits course item information entry in reformatted course items matrix
    def editCourseItem2(self, oldItemType, oldItemName, itemType, itemName, percentAchieved, percentageWeight):
        # checks if itemType does not current exist in the course items matrix (see if user changed itemType)
        if itemType not in self.courseItemsMatrix2:
            self.courseItemsMatrix2[itemType] = {}

            # deletes old entry from course items matrix
            del self.courseItemsMatrix2[oldItemType][oldItemName]

        # creates new entry in course items matrix with updated course item info
        self.courseItemsMatrix2[itemType][itemName] = [percentAchieved, percentageWeight]

        # deletes unused item types from reformatted course items info matrix
        for item in self.courseItemsMatrix2:
            if len(item) == 0:
                del self.courseItemsMatrix2[item]

    # deletes course item information entry from course items list
    def deleteCourseItem(self, itemType, itemName):
        for i in range(len(self.courseItemsMatrix)):
            if (self.courseItemsMatrix[i][0] == itemType) and (self.courseItemsMatrix[i][1] == itemName):
                del self.courseItemsMatrix[i]
                break

        # deletes unused item types from course item types list
        for itemType in self.courseItemTypes:
            itemTypeCount = 0
            for item in self.courseItemsMatrix:
                if item[0] == itemType:
                    itemTypeCount += 1
            if itemTypeCount == 0:
                index = self.courseItemTypes.index(itemType)
                del self.courseItemTypes[index]

    # deletes course item information entry from reformatted course items list
    def deleteCourseItem2(self, itemType, itemName):
        del self.courseItemsMatrix2[itemType][itemName]

        # deletes unused item types from course items matrix
        if len(self.courseItemsMatrix2[itemType]) == 0:
            del self.courseItemsMatrix2[itemType]

    # calculates weighted course average from all added course items and associated percentage weights (original format)
    def calcCourseAvg(self):
        self.coursePercentAchieved, self.coursePercentWeighted = 0, 0

        for courseItem in self.courseItemsMatrix:
            # percentage achieved * percentage weight of each item
            self.coursePercentAchieved += (courseItem[2] * courseItem[3])
            # percentage weight of each item
            self.coursePercentWeighted += courseItem[3]

        self.courseAvg = self.coursePercentAchieved / self.coursePercentWeighted

    # calculates weighted course average from all added course items and associated percentage weights (updated format)
    def calcCourseAvg2(self):
        self.coursePercentAchieved, self.coursePercentWeighted = 0, 0

        for courseType in self.courseItemsMatrix2:
            for courseItem in courseType:
                # percent achieved * percent weight per item
                self.coursePercentAchieved += courseItem[0] * courseItem[1]
                # percent weight per item
                self.coursePercentWeighted += courseItem[1]

        self.courseAvg = self.coursePercentAchieved / self.coursePercentWeighted

    # calculates course 12-point GPA (original data format)
    def calcCourse12pGPA(self):
        for p in range(13):
            if self.courseAvg >= self.percentGPA[p]:
                self.course12pGPA = self.gradeGPA[p]
                break

    # returns course average
    def getCourseAvg(self):
        return self.courseAvg

    # returns course 12p GPA
    def getCourse12pGPA(self):
        return self.course12pGPA

    # returns course code
    def getCourseCode(self):
        return self.courseCode

    # returns # of course credits
    def getCourseCredits(self):
        return self.courseCredits

    # returns course items types list
    def getCourseItemTypes(self):
        return self.courseItemTypes

    # returns course items matrix (original data formatting)
    def getCourseItemsMatrix(self):
        return self.courseItemsMatrix

    # returns course items matrix (updated formatting)
    def getCourseItemsMatrix2(self):
        return self.courseItemsMatrix2

    # returns percent achieved (so far)
    def getCoursePercentAchieved(self):
        return self.coursePercentAchieved

    # returns percent weight (so far)
    def getCoursePercentWeighted(self):
        return self.coursePercentWeighted

    # displays course profile overview with original data formatting
    def displayCourseProfile(self):
        print("Course Name:", self.courseName, "\nCourse Code: ", self.courseCode, "\nCourse Credits: ",
              self.courseCredits, "\n\nCourse Average: ", round(self.courseAvg, 3), "\nCourse Percent Achieved:",
              round(self.coursePercentAchieved, 3), "\nCourse Percent Weighted:", self.coursePercentWeighted,
              "\n\nCourse 12-Point GPA:", self.course12pGPA)

        print("Course Items:\n")

        for itemType in self.courseItemTypes:
            print(itemType.capitalize())
            for item in self.courseItemsMatrix:
                if item[0] == itemType:
                    print(item[1], "\tPercent Achieved: {0:<5}\t\tPercent Weight: {1}".format(round(item[2], 3),
                                                                                              item[3]))
            print("\n--------------------------------")

    # display course profile overview with updated data formatting
    def displayCourseProfile2(self):
        print("Course Name:", self.courseName, "\nCourse Code: ", self.courseCode, "\nCourse Credits: ",
              self.courseCredits, "\n\nCourse Average: ", round(self.courseAvg, 3), "\nCourse Percent Achieved:",
              round(self.coursePercentAchieved, 3), "\nCourse Percent Weighted:", self.coursePercentWeighted,
              "\n\nCourse 12-Point GPA:", self.course12pGPA)

        print("--------------------------------\nCourse Items:\n")

        for itemType in self.courseItemsMatrix2:
            print(itemType.capitalize())
            for itemName in self.courseItemsMatrix2[itemType]:
                print(itemName, "\tPercent Achieved: {0: <5}\t\tPercent Weight: {1}".format(
                    round(self.courseItemsMatrix2[itemType][itemName][0], 3),
                    self.courseItemsMatrix2[itemType][itemName][1]))
            print("\n--------------------------------")

    # updates/syncs data between data matrices (original and reformatted)
    def dataUpdateSync(self):
        for entry in self.courseItemsMatrix:
            # checks if item type exists in reformatted course item matrix
            if entry[0] not in self.courseItemsMatrix2:
                self.courseItemsMatrix2[entry[0]] = {}

            if entry[1] not in self.courseItemsMatrix2[entry[0]]:
                self.courseItemsMatrix2[entry[0]][entry[1]] = [entry[2], entry[3]]

