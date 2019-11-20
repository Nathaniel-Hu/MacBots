"""
------------------------------------------------------------------------------------------------------------------------
Programmer(s): Nathaniel Hu
Program Library Version: 0.0.1 (Developmental)
Last Updated: November 13th, 2019
------------------------------------------------------------------------------------------------------------------------
Program Library Description
[insert program library description]
------------------------------------------------------------------------------------------------------------------------
"""

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

    # adds course item information entry to course items matrix
    def addCourseItem(self, itemType, itemName, percentAchieved, percentageWeight):
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
        for courseItem in self.courseItemsMatrix:
            self.coursePercentAchieved += (courseItem[2] * courseItem[3]) / 100.0
            self.coursePercentWeighted += courseItem[3]

        self.courseAvg = self.coursePercentAchieved / self.coursePercentWeighted

    # calculates course 12-point GPA
    def calcCourse12pGPA(self):
        for p in range(len(self.percentGPA)):
            if self.courseAvg >= self.percentGPA[p]:
                self.course12pGPA = self.gradeGPA[p]

    # displays course profile overview
    def displayCourseProfile(self):
        print("Course Name:", self.courseName, "\nCourse Code: ", self.courseCode, "\nCourse Credits: ",
              self.courseCredits, "\n\nCourse Average: ", self.courseAvg, "\nCourse Percent Achieved:",
              self.coursePercentAchieved, "\nCourse Percent Weighted:", self.coursePercentWeighted,
              "\n\nCourse 12-Point GPA:", self.course12pGPA)

        print("Course Items:\n")

        for itemType in self.courseItemTypes:
            print(itemType)
            for item in self.courseItemsMatrix:
                if item[0] == itemType:
                    print(item[1], "\tPercent Achieved:", item[2], "Percent Weight:", item[3])
            print("\n")


