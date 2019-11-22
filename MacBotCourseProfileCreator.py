"""
------------------------------------------------------------------------------------------------------------------------
Programmer(s): Nathaniel Hu
Program Library Version: 0.0.2 (Developmental)
Last Updated: November 13th, 2019
------------------------------------------------------------------------------------------------------------------------
Program Library Description
[insert program library description]
------------------------------------------------------------------------------------------------------------------------
"""
# from pickle import *


# creates and manages profiles for each course added to MacGradeBot
class MacBotCourseProfileCreator:
    def __init__(self, courseName, courseCode, courseCredits):
        self.courseName = courseName
        self.courseCode = courseCode
        self.courseCredits = courseCredits
        # e.g. "Assignments", "Minor Assignments", "Major Assignments", "Projects", "Midterm Tests", "Final Exam"
        self.courseItemTypes = []
        # ["itemType", "itemName", "percent achieved", "percentage weight"]
        self.courseItemsMatrix = []
        self.courseAvg = float()
        self.coursePercentAchieved = float()
        self.coursePercentWeighted = float()
        self.course12pGPA = float()
        # percentage to 12-point GPA converter information
        self.percentGPA = [90.0, 85.0, 80.0, 77.0, 73.0, 70.0, 67.0, 63.0, 60.0, 57.0, 53.0, 50.0, 0.0]
        self.gradeGPA = [12.0, 11.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0]
        # user choices (for use by courseProfileMain method)
        self.userChoices = ['add', 'edit', 'avg', 'gpa', 'display', 'exit']

    # main method controlling class instance
    def courseProfileMain(self):
        while True:
            print("Welcome to the MacBot Course Profile Creator for {}!".format(self.courseName))
            userChoice = input("Would you like to add, edit, average, calculate gpa, display course profile or exit?: ")

            # adds new item to course item matrix
            if userChoice == self.userChoices[0]:
                itemType, itemName, percentAchieved, percentageWeight = self.inputCourseItemInfo()
                self.addCourseItem(itemType, itemName, percentAchieved, percentageWeight)

            # edits given item in course item matrix
            elif userChoice == self.userChoices[1]:
                for i in range(len(self.courseItemsMatrix)):
                    print('Index #: {} '.format(i), self.courseItemsMatrix[i])

                itemIndex = int(input("Input the index # of the item you would like to edit here: "))
                itemType, itemName, percentAchieved, percentageWeight = self.inputCourseItemInfo()

                self.editCourseItem(itemType, itemName, percentAchieved, percentageWeight, itemIndex)

            elif userChoice == self.userChoices[2]:
                self.calcCourseAvg()

            elif userChoice == self.userChoices[3]:
                self.calcCourse12pGPA()

            elif userChoice == self.userChoices[4]:
                self.displayCourseProfile()

            else:
                print("exiting course profile for course", self.courseName)
                break

    # allows user to input item for given course item
    def inputCourseItemInfo(self):
        itemType = input("Enter the item type (e.g. minor assignment, midterm) here: ").lower()
        itemName = input("Enter the name of the item (e.g. minor assignment #1) here: ").lower().capitalize()
        percentAchieved = float(eval(input("Enter your percent achieved (e.g. 100.0, 6/8 * 100) here: ")))
        percentageWeight = float(input("Enter the percentage weight of {} here: ".format(itemName)))
        return itemType, itemName, percentAchieved, percentageWeight

    # adds course item information entry to course items matrix
    def addCourseItem(self, itemType, itemName, percentAchieved=0.00, percentageWeight=0.00):
        self.courseItemsMatrix.append([itemType, itemName, percentAchieved, percentageWeight])

        if itemType not in self.courseItemTypes:
            self.courseItemTypes.append(itemType)

    # edits course item information entry in course items matrix
    def editCourseItem(self, itemType, itemName, percentAchived, percentageWeight, itemIndex):
        self.courseItemsMatrix[itemIndex] = [itemType, itemName, percentAchived, percentageWeight]

        if itemType not in self.courseItemTypes:
            self.courseItemTypes.append(itemType)

    # calculated weighted course average from all added course items and associated percentage weights
    def calcCourseAvg(self):
        self.coursePercentAchieved, self.coursePercentWeighted = 0, 0

        for courseItem in self.courseItemsMatrix:
            self.coursePercentAchieved += (courseItem[2] * courseItem[3]) / 100
            self.coursePercentWeighted += courseItem[3]

        self.courseAvg = self.coursePercentAchieved / self.coursePercentWeighted * 100

    # calculates course 12-point GPA
    def calcCourse12pGPA(self):
        for p in range(13):
            if self.courseAvg >= self.percentGPA[p]:
                self.course12pGPA = self.gradeGPA[p]
                break

    # returns course average
    def courseAvg(self):
        return self.courseAvg

    # returns # of course credits
    def courseCredits(self):
        return self.courseCredits

    # displays course profile overview
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

    # # loads course profile info from user save (.dat file)
    # def loadCourseProfile(self, saveUsername, courseName):
    #     with open('{0}/{1}.dat'.format(saveUsername, courseName), 'rb') as courseSave:
    #         self.courseName, self.courseCode, self.courseCredits, self.courseItemTypes, self.courseItemsMatrix, \
    #             self.courseAvg, self.coursePercentAchieved, self.coursePercentWeighted, \
    #             self.course12pGPA = load(courseSave)
    #
    # # saves course profile info into user save (.dat file) and user text save (.txt file); overwrites existing file(s)
    # def saveCourseProfile(self, saveUsername):
    #     courseSaveBinary = [self.courseName, self.courseCode, self.courseCredits, self.courseItemTypes,
    #                         self.courseItemsMatrix, self.courseAvg, self.coursePercentAchieved,
    #                         self.coursePercentWeighted, self.course12pGPA]
    #
    #     # course profile save (binary file; .dat)
    #     with open('{0}/{1}.dat'.format(saveUsername, self.courseName), 'wb') as binarySave:
    #         dump(courseSaveBinary, binarySave)
