"""
------------------------------------------------------------------------------------------------------------------------
Programmer(s): Nathaniel Hu
Program Version: 0.1.0 (Developmental)
Last Updated: December 16th, 2019
------------------------------------------------------------------------------------------------------------------------
Program Description
[insert program description]
------------------------------------------------------------------------------------------------------------------------
"""
# this controls program data updating/patching functions/mechanisms in the program
currentBotVersion = 0.1

from time import *
from pickle import *

from MacBotCourseProfileCreator import *


class MacGradeBot:
    # instantiation of class into new student profile object
    def __init__(self, botVersion=0.0):
        # student user profile information
        self.name = str()
        self.username = str()
        self.password = str()
        self.passwordConfirm = str()
        self.email = str()
        self.emailConfirm = str()
        self.saveFile = str()
        self.botVersion = botVersion

        # student course + course information (course profiles) dictionary + cumulative average
        self.courseNames = []
        # original format data matrix
        self.courseInfo = {}
        # updated format data matrix
        self.courseInfo2 = {}
        self.cumulativeAvg = float()

        userChoice = input("Login or Sign Up: ")
        if userChoice.lower() == 'sign up':
            # start signUp() method
            self.signUp()
        else:
            self.login()

        self.main()

    # main method
    def main(self):
        userChoices = ['display', 'add', 'edit', 'avg', 'save', 'quit']

        print("Checking data...")

        # allows user to decide whether they would like to update their data or not
        if len(self.courseInfo) > len(self.courseInfo2):
            update = input("Your data is not completely updated. Would you like to update all of your course " +
                           "information?\nPlease input yes or no here: ").lower()

            while (update != "yes") and (update != "no"):
                update = input("Please re-enter a valid input (yes/no) here: ").lower()

            if update == "yes":
                self.updateCourseProfiles()

        print("Here is your current MacGradeBot student profile:\n", str(self.courseNames), "\n", str(self.courseInfo),
              "\n", str(self.cumulativeAvg))

        while True:
            print("MacGradeBot Program")
            userChoice = input("Hello, would you like to display current courses (display), add/edit a course " +
                               "(add/edit), calculate your cumulative average (avg), save your data (save) or quit " +
                               "(quit): ")

            # exception handling for user choice inputs
            while userChoice not in userChoices:
                userChoice = input("Please input display/add/edit/avg/save/quit here: ")

            # display current courses
            if userChoice == userChoices[0]:
                self.displayCourses()

            # adding a course
            elif userChoice == userChoices[1]:
                self.openCourseProfile(self.addCourse())

            # editing a course's info
            elif userChoice == userChoices[2]:
                self.openCourseProfile(self.editCourseInfo())

            # calculates course avg
            elif userChoice == userChoices[3]:
                self.calcCumulativeAvg()

            elif userChoice == userChoices[4]:
                self.saveController()

            # quits the program (add option later asking if user wants to save edits or not)
            else:
                self.quit()

            userChoice = input("Would you like to quit (yes/no): ")

            if userChoice == "no":
                pass
            else:
                self.quit()

    # sign up method
    def signUp(self):
        self.name = input("Name: ")

        self.username = input("Username: ")

        self.saveFile = self.username

        self.password = input("Password: ")
        self.passwordConfirm = input("Confirm Password: ")

        while self.password != self.passwordConfirm:
            print("Please re-confirm your password.")
            self.passwordConfirm = input("Confirm Password: ")

        self.email = input("Email: ")
        self.emailConfirm = input("Confirm Email: ")

        while self.email != self.emailConfirm:
            print("Please re-confirm your email.")
            self.emailConfirm = input("Confirm Email: ")

    # login method
    def login(self):
        while True:
            user = input("Username: ")
            self.password = input("Password: ")

            try:
                self.openSaveFile(user)
            except FileNotFoundError:
                print("Sorry, but that user does not exist.")
                continue

            # compares username to see if username is correct (this is redundant) FIXME
            if user == self.username:
                while True:
                    # tests if password is correct
                    if self.password == self.passwordConfirm:
                        break
                    else:
                        self.password = input("Re-enter your password here: ")
                break
            else:
                pass

    # method displays all current courses in student profile
    def displayCourses(self):
        print("Here are all of your current courses:\n--------------------------------")
        for course in self.courseNames:
            print(self.courseInfo[course].courseCode, course)
        print("--------------------------------")

    # method adds course + course info (creates/adds new course profile) to student profile
    def addCourse(self):
        # gets user inputted information
        courseName = input("Enter your course name (e.g. ENG COMP) here: ").upper()

        while courseName in self.courseNames:
            courseName = input("Sorry, but that course name has already been taken. Please re-enter your course name" +
                               " (e.g. ENG COMP) here: ").upper()

        courseCode = input("Enter the course code for {} here: ".format(courseName))
        courseCredits = int(input("Enter the # of credits for {} here: ".format(courseName)))

        # appends course name to courseNames; creates new course profile object (class instance)
        self.courseNames.append(courseName)
        self.courseInfo[courseName] = MacBotCourseProfileCreator(courseName, courseCode, courseCredits)

        return courseName

    # allows user to update course grades (labs, assignments, midterm tests and exams, etc.)
    def editCourseInfo(self):
        # gets user inputted information
        courseName = input("Enter the name of the course that you would like to edit here: ").upper()

        # safeguard code to update outdated data into reformatted data
        try:
            if self.courseInfo[courseName].courseItemsMatrix2:
                print(self.courseInfo[courseName].courseItemsMatrix2)
        except AttributeError:
            self.updateCourseProfile(courseName)

        return courseName

    # opens course profile
    def openCourseProfile(self, courseName):
        # references course profile creator main method
        self.courseInfo2[courseName].courseProfileMain()

    # calculates cumulative average
    def calcCumulativeAvg(self):
        averageSum = float()
        creditsSum = int()

        # goes through each course, sums average times course credits, and course credits
        for courseName in self.courseNames:
            averageSum += self.courseInfo[courseName].courseAvg * self.courseInfo[courseName].courseCredits
            creditsSum += self.courseInfo[courseName].courseCredits

        # calculates cumulative average (percentage) and displays to user
        self.cumulativeAvg = round(averageSum / creditsSum, 2)
        print("Your overall cumulative average is:", self.cumulativeAvg)

    # saves user profile (binary and text files) for earlier program versions
    def saveToFile(self):
        userSaveBinary = [self.name, self.username, self.passwordConfirm, self.emailConfirm, self.saveFile,
                          self.courseNames, self.courseInfo, self.cumulativeAvg]

        # user save (binary file; .dat)
        with open('{0}/{0}_MGBS.dat'.format(self.saveFile), 'wb') as binarySave:
            dump(userSaveBinary, binarySave)

        # user save (text file; .txt)
        textSave = open('{0}/{0}_MGBS.txt'.format(self.saveFile), 'w')

        text = "======================================= MacGradeBot ======================================\n" + \
               str(self.botVersion) + \
               "\n------------------------------------------------------------------------------------------" + \
               "\nName: " + self.name + "\nUsername: " + self.username + "\nPassword: " + self.passwordConfirm + \
               "\nEmail: " + self.emailConfirm + "\nCumulative Average: " + str(self.cumulativeAvg) + \
               "\n------------------------------------------------------------------------------------------" + \
               "\n\n" + "Course Name: [# Credits, Average, 12-Point GPA]\n--------------------------------"
        textSave.write(text)
        textSave.close()

        # user save (text file; .txt)
        textSave = open('{0}/{0}_MGBS.txt'.format(self.saveFile), 'a')
        for course in self.courseNames:
            courseInfo = self.courseInfo[course]
            textSave.write("\n{0} {1}:\t".format(course, courseInfo.courseCode))
            textSave.write("Course Credits: {0}\tCourse Average: {1:<5}\tCourse 12p GPA: {2:<4}".format(
                courseInfo.courseCredits, round(courseInfo.courseAvg, 3), courseInfo.course12pGPA))
        textSave.close()

    # saves user profile (binary and text files) for later patched program versions
    def saveToFile1(self):
        userSaveBinary = [self.name, self.username, self.passwordConfirm, self.emailConfirm, self.saveFile,
                          self.courseNames, self.courseInfo, self.courseInfo2, self.cumulativeAvg, self.botVersion]

        # user save (binary file; .dat)
        with open('{0}/{0}_MGBSXC.dat'.format(self.saveFile), 'wb') as binarySave:
            dump(userSaveBinary, binarySave)

        # user save (text file; .txt)
        textSave = open('{0}/{0}_MGBSXC.txt'.format(self.saveFile), 'w')

        text = "======================================= MacGradeBot ======================================\n" + \
               str(self.botVersion) + \
               "\n------------------------------------------------------------------------------------------" + \
               "\nName: " + self.name + "\nUsername: " + self.username + "\nPassword: " + self.passwordConfirm + \
               "\nEmail: " + self.emailConfirm + "\nCumulative Average: " + str(self.cumulativeAvg) + \
               "\n------------------------------------------------------------------------------------------" + \
               "\n\n" + "Course Name: [# Credits, Average, 12-Point GPA]\n--------------------------------" + \
               str(self.botVersion)
        textSave.write(text)
        textSave.close()

        # user save (text file; .txt)
        textSave = open('{0}/{0}_MGBSXC.txt'.format(self.saveFile), 'a')
        courses = self.courseInfo2

        for course in courses:
            textSave.write("\n{0} {1}:\t".format(course, courses[course].courseCode))
            textSave.write("Course Credits: {0}\tCourse Average: {1:<5}\tCourse 12p GPA: {2:<4}".format(
                courses[course].courseCredits, round(courses[course].courseAvg, 3), courses[course].course12pGPA))
        textSave.close()

    # save controller method
    def saveController(self):
        print("saving student profile")
        self.saveToFile()

        if self.botVersion > 0.0:
            self.saveToFile1()

    # opens user profile (binary file)
    def openSaveFile(self, user):
        # for earlier developmental versions
        if self.botVersion == 0.0:
            # open user save (binary file; .dat)
            with open('{0}/{0}_MGBS.dat'.format(user), 'rb') as save:
                # unpacks save tuple into multiple parameter entries
                self.loadSaveData(*load(save))
        # for later patched versions
        else:
            try:
                # open user save (binary file; .dat)
                with open('{0}/{0}_MGBSXC.dat'.format(user), 'rb') as save:
                    # unpacks save tuple into multiple parameter entries
                    self.loadSaveData2(*load(save))
            # for later patched versions opening older files
            except FileNotFoundError:
                with open('{0}/{0}_MGBS.dat'.format(user), 'rb') as save:
                    # unpacks save tuple into multiple parameter entries
                    self.loadSaveData(*load(save))

    # loads binary file save data into class attributes (from older files pre 0.0.6)
    def loadSaveData(self, name, username, passwordConfirm, emailConfirm, saveFile, courseNames, courseInfo,
                     cumulativeAvg, botVersion=0.0):

        if botVersion == 0.0:
            botVersion = currentBotVersion

        self.name, self.username, self.passwordConfirm, self.emailConfirm, self.saveFile, self.courseNames, \
        self.courseInfo, self.cumulativeAvg, self.botVersion = name, username, passwordConfirm, emailConfirm, \
            saveFile, courseNames, courseInfo, cumulativeAvg, botVersion

    # loads binary file save data into class attributes (for convertible files 0.0.6)
    def loadSaveData2(self, name, username, passwordConfirm, emailConfirm, saveFile, courseNames, courseInfo,
                     courseInfo2, cumulativeAvg, botVersion):

        self.name, self.username, self.passwordConfirm, self.emailConfirm, self.saveFile, self.courseNames, \
        self.courseInfo, self.courseInfo2, self.cumulativeAvg, self.botVersion = name, username, passwordConfirm, \
            emailConfirm, saveFile, courseNames, courseInfo, courseInfo2, cumulativeAvg, botVersion

    # takes data from old class instance and creates new updated class instance with same data
    def updateCourseProfile(self, courseName):
        # old class instance --> self.courseInfo[courseName]
        courseCode = self.courseInfo[courseName].getCourseCode()
        courseCredits = self.courseInfo[courseName].getCourseCredits()

        self.courseInfo2[courseName] = MacBotCourseProfileCreator(courseName, courseCode, courseCredits)

        # transferring old data over to new class object
        self.courseInfo2[courseName].courseItemTypes = self.courseInfo[courseName].getCourseItemTypes()
        self.courseInfo2[courseName].courseItemsMatrix = self.courseInfo[courseName].getCourseItemsMatrix()

        self.courseInfo2[courseName].courseAvg = self.courseInfo[courseName].getCourseAvg()
        self.courseInfo2[courseName].coursePercentAchieved = self.courseInfo[courseName].getCoursePercentAchieved()
        self.courseInfo2[courseName].coursePercentWeighted = self.courseInfo[courseName].getCoursePercentWeighted()
        self.courseInfo2[courseName].course12pGPA = self.courseInfo[courseName].getCourse12pGPA()

    # takes data from old class instances and creates new updated class instances with same data
    def updateCourseProfiles(self):
        for course in self.courseNames:
            # update course profile only it has not already been updated
            if course not in self.courseInfo2:
                self.updateCourseProfile(course)

    # quit method
    def quit(self):
        self.saveController()
        print("shutting down")
        quit()


# import management code
if __name__ == "__main__":
    MacUser = MacGradeBot(currentBotVersion)
else:
    pass
