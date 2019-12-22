"""
------------------------------------------------------------------------------------------------------------------------
Programmer(s): Nathaniel Hu
Program Library Version: 0.1.1 (Developmental)
Last Updated: December 21th, 2019
------------------------------------------------------------------------------------------------------------------------
Program Library Description
[insert program library description]
------------------------------------------------------------------------------------------------------------------------
"""


# creates and manages profiles for each course added to MacGradeBot
class MacBotCourseProfileCreator:
    def __init__(self, courseName, courseCode, courseCredits):
        self.currentVersion = 1.1

        self.courseName = courseName
        self.courseCode = courseCode
        self.courseCredits = courseCredits

        # updated formatting course items matrix
        self.courseItemsMatrix = {}

        self.courseAvg = float()
        self.coursePercentAchieved = float()
        self.coursePercentWeighted = float()
        self.course12pGPA = float()
        # percentage to 12-point GPA converter information
        self.percentGPA = (90.0, 85.0, 80.0, 77.0, 73.0, 70.0, 67.0, 63.0, 60.0, 57.0, 53.0, 50.0, 0.0)
        self.gradeGPA = (12.0, 11.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0)
        # user choices (for use by courseProfileMain method)
        self.userChoices = ['add', 'edit', 'delete', 'avg', 'gpa', 'display', 'exit']

    # main method controlling class instance
    def courseProfileMain(self):
        while True:
            # input user choice (with while loop exception handling)
            print("Welcome to the MacBot Course Profile Creator for {}!".format(self.courseName))
            userChoice = input("Would you like to add, edit, delete, average, calculate gpa, display course profile " +
                               "or exit?: ").lower()

            while userChoice not in self.userChoices:
                userChoice = input("Please enter a valid choice (add/edit/delete/avg/gpa/display/exit) here: ").lower()

            # adds new item to reformatted course item matrix
            if userChoice == self.userChoices[0]:
                itemType, itemName, percentAchieved, percentageWeight = self.inputCourseItemInfo()

                # checks if item type is already in reformatted course item matrix
                self.addCourseItem(itemType, itemName, percentAchieved, percentageWeight)

            # edits given item in course item matrix
            elif userChoice == self.userChoices[1]:
                # prints out all items in course items matrix
                for itemType in self.courseItemsMatrix:
                    print(itemType)
                    for item in self.courseItemsMatrix[itemType]:
                        print(item)

                # references edit delete course item info method (EDN = 0; edit course item)
                oldItemType, oldItemName = self.editDeleteCourseItemInfo(0)

                # edits course item (with updated data formatting)
                self.editCourseItem(oldItemType, oldItemName, *self.editCourseItemInfo(oldItemType, oldItemName))

            # deletes given item in course item matrix
            elif userChoice == self.userChoices[2]:
                # references edit delete course item info method (EDN = 1; delete course item)
                itemType, itemName = self.editDeleteCourseItemInfo(1)

                self.deleteCourseItem(itemType, itemName)

            # calculates course average with updated format data
            elif userChoice == self.userChoices[3]:
                self.calcCourseAvg()

            # calculates course 12-point GPA
            elif userChoice == self.userChoices[4]:
                self.calcCourse12pGPA()

            # displays course profile with updated format data
            elif userChoice == self.userChoices[5]:
                self.displayCourseProfile()

            else:
                print("exiting course profile for course", self.courseName)
                break

    # allows user to input information for given course item
    def inputCourseItemInfo(self):
        itemType = input("Enter the item type (e.g. minor assignment, midterm) here: ").lower()
        itemName = input("Enter the name of the item (e.g. minor assignment #1) here: ").lower().capitalize()

        while itemName in self.courseItemsMatrix[itemType]:
            itemName = input("Sorry, but an item with that same name already exists under the type {}. Please " +
                             "re-enter a different item name here: ".format(itemType))

        percentAchieved = float(eval(input("Enter your percent achieved (e.g. 100.0, 6/8 * 100) here: ")))
        percentageWeight = float(eval(input("Enter the percentage weight of {} here: ".format(itemName))))
        return itemType, itemName, percentAchieved, percentageWeight

    # allows user to input information to edit in given course item (for reformatted data entries)
    def editCourseItemInfo(self, oldItemType, oldItemName):
        itemType = input("Enter the item type (e.g. minor assignment, midterm) here: ").lower()
        if itemType == "":
            itemType = oldItemType

        itemName = input("Enter the name of the item (e.g. minor assignment #1) here: ").lower().capitalize()
        if itemName == "":
            itemName = oldItemName

        try:
            percentAchieved = float(eval(input("Enter your item percent achieved (e.g. 100.0, 6/8 * 100) here: ")))
        except SyntaxError:
            percentAchieved = self.courseItemsMatrix[oldItemName][oldItemType][0]

        try:
            percentWeight = float(eval(input("Enter your item percent weight (e.g. 100.0, 6/8 * 100) here: ")))
        except SyntaxError:
            percentWeight = self.courseItemsMatrix[oldItemName][oldItemType][1]

        return itemType, itemName, percentAchieved, percentWeight

    # allows user to input information to edit/delete given course item entries
    def editDeleteCourseItemInfo(self, EDN):
        editDelete = ('edit', 'delete')

        # input (old) item type here (with while loop exception handling)
        itemType = input("Input the type of the item you would like to {} (e.g. midterm) here: ".format(
            editDelete[EDN])).lower()

        while itemType not in self.courseItemsMatrix:
            itemType = input("Sorry, but that item type does not exist. Please re-enter the type of the item you " +
                             "would like to {} (e.g. midterm) here: ".format(editDelete[EDN])).lower()

        # input (old) item name here (with while loop exception handling)
        itemName = input("Input the item name (type {0}) you would like to {1} here: ".format(itemType, editDelete[EDN])
                         ).lower().capitalize()

        while itemName not in self.courseItemsMatrix[itemType]:
            itemName = input("Sorry, but that item name does not exist. Please re-enter the item name (type {0}) you " +
                             "would like to {1} here: ".format(itemType, editDelete[EDN])).lower().capitalize()

        return itemType, itemName

    # adds course item information entry to reformatted course items matrix
    def addCourseItem(self, itemType, itemName, percentAchieved=0.00, percentWeight=0.00):
        if itemType not in self.courseItemsMatrix:
            self.courseItemsMatrix[itemType] = {}

        self.courseItemsMatrix[itemType][itemName] = [percentAchieved, percentWeight]

    # edits course item information entry in reformatted course items matrix
    def editCourseItem(self, oldItemType, oldItemName, itemType, itemName, percentAchieved, percentageWeight):
        # checks if itemType does not current exist in the course items matrix (see if user changed itemType)
        if itemType not in self.courseItemsMatrix:
            self.courseItemsMatrix[itemType] = {}

            # deletes old entry from course items matrix
            del self.courseItemsMatrix[oldItemType][oldItemName]

        # creates new entry in course items matrix with updated course item info
        self.courseItemsMatrix[itemType][itemName] = [percentAchieved, percentageWeight]

        # deletes unused item types from reformatted course items info matrix
        for item in self.courseItemsMatrix:
            if len(self.courseItemsMatrix[item]) == 0:
                del self.courseItemsMatrix[item]

    # deletes course item information entry from reformatted course items list
    def deleteCourseItem(self, itemType, itemName):
        del self.courseItemsMatrix[itemType][itemName]

        # deletes unused item types from course items matrix
        if len(self.courseItemsMatrix[itemType]) == 0:
            del self.courseItemsMatrix[itemType]

    # calculates weighted course average from all added course items and associated percentage weights (updated format)
    def calcCourseAvg(self):
        self.coursePercentAchieved, self.coursePercentWeighted = 0, 0

        for courseType in self.courseItemsMatrix:
            for courseItem in self.courseItemsMatrix[courseType]:
                # percent achieved * percent weight per item
                self.coursePercentAchieved += self.courseItemsMatrix[courseType][courseItem][0] * \
                                              self.courseItemsMatrix[courseType][courseItem][1] / 100
                # percent weight per item
                self.coursePercentWeighted += self.courseItemsMatrix[courseType][courseItem][1]

        self.courseAvg = self.coursePercentAchieved / self.coursePercentWeighted * 100

        print("Your current course average is {} %.".format(round(self.courseAvg, 3)))

    # calculates course 12-point GPA (original data format)
    def calcCourse12pGPA(self):
        for p in range(13):
            if self.courseAvg >= self.percentGPA[p]:
                self.course12pGPA = self.gradeGPA[p]
                break

        print("Your current course GPA is {}.".format(self.course12pGPA))

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

    # returns course items matrix (original data formatting)
    def getCourseItemsMatrix(self):
        return self.courseItemsMatrix

    # returns percent achieved (so far)
    def getCoursePercentAchieved(self):
        return self.coursePercentAchieved

    # returns percent weight (so far)
    def getCoursePercentWeighted(self):
        return self.coursePercentWeighted

    # display course profile overview with updated data formatting
    def displayCourseProfile(self):
        print("Course Name:", self.courseName, "\nCourse Code: ", self.courseCode, "\nCourse Credits: ",
              self.courseCredits, "\n\nCourse Average: ", round(self.courseAvg, 3), "\nCourse Percent Achieved:",
              round(self.coursePercentAchieved, 3), "\nCourse Percent Weighted:", self.coursePercentWeighted,
              "\n\nCourse 12-Point GPA:", self.course12pGPA)

        print("--------------------------------\nCourse Items:\n")

        for itemType in self.courseItemsMatrix:
            print(itemType.capitalize())
            for itemName in self.courseItemsMatrix[itemType]:
                print(itemName, "\tPercent Achieved: {0: <5}\t\tPercent Weight: {1}".format(
                    round(self.courseItemsMatrix[itemType][itemName][0], 3),
                    self.courseItemsMatrix[itemType][itemName][1]))
            print("\n--------------------------------")

