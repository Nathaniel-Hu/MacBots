"""
------------------------------------------------------------------------------------------------------------------------
Programmer(s): Nathaniel Hu
Program Version: 0.1.4 (Developmental)
Last Updated: December 30th, 2019
------------------------------------------------------------------------------------------------------------------------
Program Description
[insert program description]
------------------------------------------------------------------------------------------------------------------------
"""
from time import *
from pickle import *
from MacBotCourseProfileCreator import *
import os

# this controls program data updating/patching functions/mechanisms in the program
currentBotVersion = 1.3


class MacGradeBot:
    # instantiation of class into new student profile object
    def __init__(self, botVersion):
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
        # updated format data matrix
        self.courseInfo = {}

        # cumulative avg/GPA
        self.cumulativeAvg = float()
        self.cumulativeGPA = float()

        # user choices
        self.userChoices = ('display', 'add', 'edit', 'avg', 'gpa', 'save', 'quit')

        print("===================================== MacGradeBot Program ======================================" +
              "\nWelcome to the MacGradeBot Program.\n" +
              "\n---------------------------------------------------------------------------------")

        # takes in user choice (login or sign up); equipped with while loop exception handling
        userChoice = input("Would you like to login or sign up?" +
                           "\nPlease enter your choice (login/sign up) here: ").lower()

        while (userChoice != "login") and (userChoice != "sign up"):
            userChoice = input("--------------------------------\n" +
                               "Sorry, but that input was invalid . Please choose to login or sign up here: ").lower()

        # start signUp() method if user chooses to sign up
        if userChoice.lower() == 'sign up':
            self.signUp()
        # start login() method if user chooses to login
        else:
            self.login()

        # starts main method of user has signed up/logged in successfully
        self.main()

    # main method
    def main(self):
        print("----------------------------------------------------------------\n" +
              "Here is your current MacGradeBot student profile:\nCurrent Courses: ", self.courseNames, "\nCourse Info")

        indent = len(max(self.courseNames)) + 3

        for course in self.courseInfo:
            print(course + ":" + " "*(indent - len(course)) + str(self.courseInfo[course]))

        print("--------------------------------\nCurrent Cumulative Average:", self.cumulativeAvg,
              "\nCurrent Cumulative GPA:", self.cumulativeGPA)

        while True:
            print("===================================== MacGradeBot Program ======================================")
            userChoice = input("\nHello, would you like to display current courses (display), add/edit a course " +
                               "(add/edit), calculate your cumulative average (avg) or gpa (gpa), save your data " +
                               "(save) or quit (quit): ").lower()

            # exception handling for user choice inputs
            while userChoice not in self.userChoices:
                userChoice = input("--------------------------------\nSorry, but that input was invalid." +
                                   " Please input display/add/edit/avg/save/quit here: ").lower()

            # display current courses
            if userChoice == self.userChoices[0]:
                self.displayCourses()

            # adding a course
            elif userChoice == self.userChoices[1]:
                self.openCourseProfile(self.addCourse())

            # editing a course's info
            elif userChoice == self.userChoices[2]:
                self.openCourseProfile(self.editCourseInfo())

            # calculates course avg
            elif userChoice == self.userChoices[3]:
                self.calcCumulativeAvg()

            # calculates course GPA
            elif userChoice == self.userChoices[4]:
                self.calcCumlativeGPA()

            # saves all changes to course info for all existing course profiles
            elif userChoice == self.userChoices[5]:
                self.saveController()

            # quits the program (add option later asking if user wants to save edits or not)
            else:
                self.quit()

            # allows user to quit the program or to continue to use it; equipped with while loop exception handling
            userChoice = input("----------------------------------------------------------------\n" +
                               "Would you like to quit the MacGradeBot Program (yes/no): ").lower()

            while (userChoice != "yes") and (userChoice != "no"):
                userChoice = input("Sorry, but that was an invalid input. Would you like to quit (yes/no): ").lower()

            if userChoice == "no":
                pass
            else:
                self.quit()

    # sign up method
    def signUp(self):
        print("----------------------------------------------------------------")
        # takes user name, username (and implicitly save file name)
        self.name = input("Name: ")
        self.username = input("Username: ")
        self.saveFile = self.username

        print("----------------------------------------------------------------")
        # program attempts to create directory using save file name to store user data
        try:
            os.mkdir("{0}/{0}".format(self.saveFile))
        except OSError:
            print("Creation of the directory {0}/{0} has failed.".format(self.saveFile))
        else:
            print("Creation of the directory {0}/{0} was successful.".format(self.saveFile))

        print("----------------------------------------------------------------")
        # takes in user password and confirms it (using while loop exception handling)
        self.password = input("Password: ")
        self.passwordConfirm = input("Confirm Password: ")

        while self.password != self.passwordConfirm:
            print("Please re-confirm your password.")
            self.passwordConfirm = input("Confirm Password: ")

        print("----------------------------------------------------------------")
        # takes in user email and confirms it (sing while loop exception handling)
        self.email = input("Email: ").lower()
        self.emailConfirm = input("Confirm Email: ").lower()

        while self.email != self.emailConfirm:
            print("Please re-confirm your email.").lower()
            self.emailConfirm = input("Confirm Email: ").lower()

    # login method
    def login(self):
        while True:
            print("----------------------------------------------------------------")
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
        print("----------------------------------------------------------------\n" +
              "Here are all of your current courses:\n--------------------------------")
        for course in self.courseNames:
            print(self.courseInfo[course].courseCode, course)
        print("--------------------------------")

    # method adds course + course info (creates/adds new course profile) to student profile
    def addCourse(self):
        print("----------------------------------------------------------------")
        # gets user inputted information
        courseName = input("Enter your course name (e.g. ENG COMP) here: ").upper()

        while courseName in self.courseNames:
            courseName = input("Sorry, but that course name has already been taken. Please re-enter your course name" +
                               " (e.g. ENG COMP) here: ").upper()

        courseCode = input("Enter the course code for {} here: ".format(courseName)).upper()

        # while loop to take in # of credits for course; equipped with exception handling for ValueErrors (e.g. floats)
        while True:
            try:
                courseCredits = int(input("Enter the # of credits (e.g. 3, 4) for {} here: ".format(courseName)))
                break
            except ValueError:
                print("Sorry, but the # of credits for {} must be entered in as an integer value.".format(courseName))

        # appends course name to courseNames; creates new course profile object (class instance)
        self.courseNames.append(courseName)
        self.courseInfo[courseName] = MacBotCourseProfileCreator(courseName, courseCode, courseCredits)

        return courseName

    # allows user to update course grades (labs, assignments, midterm tests and exams, etc.)
    def editCourseInfo(self):
        print("----------------------------------------------------------------")
        # gets user inputted information
        courseName = input("Enter the name of the course that you would like to edit here: ").upper()

        return courseName

    # opens course profile
    def openCourseProfile(self, courseName):
        # references course profile creator main method
        self.courseInfo[courseName].courseProfileMain()

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
        print("----------------------------------------------------------------" +
              "\nYour overall cumulative average is:", self.cumulativeAvg)

    # calculates cumulative GPA
    def calcCumlativeGPA(self):
        gpaSum = float()
        creditsSum = int()

        # goes through each course, sums gpa times course credits, and course credits
        for courseName in self.courseNames:
            gpaSum += self.courseInfo[courseName].course12pGPA * self.courseInfo[courseName].courseCredits
            creditsSum += self.courseInfo[courseName].courseCredits

        # calculates cumulative GPA (12-point) and displays to user
        self.cumulativeGPA = round(gpaSum / creditsSum, 2)
        print("----------------------------------------------------------------" +
              "\nYour overall cumulative GPA is:", self.cumulativeGPA)

    # saves user profile (binary and text files) for later patched program versions
    def saveToFile(self):
        userSaveBinary = [self.name, self.username, self.passwordConfirm, self.emailConfirm, self.saveFile,
                          self.courseNames, self.courseInfo, self.cumulativeAvg, self.cumulativeGPA, self.botVersion]

        # user save (binary file; .dat)
        with open('{0}/{0}_MGBSX.dat'.format(self.saveFile), 'wb') as binarySave:
            dump(userSaveBinary, binarySave)

        # user save (text file; .txt)
        textSave = open('{0}/{0}_MGBSX.txt'.format(self.saveFile), 'w')

        text = "======================================= MacGradeBot ======================================\n" + \
               "Current Version: " + str(self.botVersion) + \
               "\n------------------------------------------------------------------------------------------" + \
               "\nName: " + self.name + "\nUsername: " + self.username + "\nPassword: " + self.passwordConfirm + \
               "\nEmail: " + self.emailConfirm + "\nCumulative Average: " + str(self.cumulativeAvg) + \
               "\nCumulative GPA: " + str(self.cumulativeGPA) + \
               "\n------------------------------------------------------------------------------------------" + \
               "\n\n" + "Course Name: [# Credits, Average, 12-Point GPA]\n--------------------------------"
        textSave.write(text)
        textSave.close()

        # user save (text file; .txt)
        textSave = open('{0}/{0}_MGBSX.txt'.format(self.saveFile), 'a')
        courses = self.courseInfo

        for course in courses:
            textSave.write("\n{0} {1}:\t".format(course, courses[course].courseCode))
            textSave.write("Course Credits: {0}\tCourse Average: {1:<5}\tCourse 12p GPA: {2:<4}".format(
                courses[course].courseCredits, round(courses[course].courseAvg, 3), courses[course].course12pGPA))
        textSave.close()

    # save controller method
    def saveController(self):
        print("--------------------------------\nSaving Student Profile...")
        self.saveToFile()

    # opens user profile (binary file)
    def openSaveFile(self, user):
        # for earlier developmental versions
        if self.botVersion == 1.0:
            # open user save (binary file; .dat)
            with open('{0}/{0}_MGBSXC.dat'.format(user), 'rb') as save:
                # unpacks save tuple into multiple parameter entries
                self.loadSaveData(*load(save))
        # for later patched versions
        else:
            try:
                # open user save (binary file; .dat)
                with open('{0}/{0}_MGBSX.dat'.format(user), 'rb') as save:
                    # unpacks save tuple into multiple parameter entries
                    self.loadSaveData2(*load(save))
            # for later patched versions opening older files
            except FileNotFoundError:
                with open('{0}/{0}_MGBSXC.dat'.format(user), 'rb') as save:
                    # unpacks save tuple into multiple parameter entries
                    self.loadSaveData(*load(save))

    # loads binary file save data into class attributes (from _MGBSXC.dat save files)
    # FIXME remove this section for later versions of this code
    def loadSaveData(self, name, username, passwordConfirm, emailConfirm, saveFile, courseNames, courseInfo,
                     courseInfo2, cumulativeAvg, botVersion):  # note: courseInfo data is not used (is trashed)

        self.updateCourseProfiles(courseInfo2)

        if botVersion > self.botVersion:
            self.botVersion = botVersion

        # transfer save data into class attributes
        self.name, self.username, self.passwordConfirm, self.emailConfirm, self.saveFile, self.courseNames, \
            self.cumulativeAvg = name, username, passwordConfirm, emailConfirm, saveFile, courseNames, cumulativeAvg

        # calculates GPA (since there is no previously calculated cumulative GPA value to import from save file)
        self.calcCumlativeGPA()

    # loads binary file save data into class attributes (for _MGBSX.dat save files)
    def loadSaveData2(self, name, username, passwordConfirm, emailConfirm, saveFile, courseNames, courseInfo,
                      cumulativeAvg, cumulativeGPA, botVersion):

        if botVersion > self.botVersion:
            self.botVersion = botVersion

        # transfer save data into class attributes
        self.name, self.username, self.passwordConfirm, self.emailConfirm, self.saveFile, self.courseNames, \
            self.courseInfo, self.cumulativeAvg, self.cumulativeGPA = name, username, passwordConfirm, emailConfirm, \
            saveFile, courseNames, courseInfo, cumulativeAvg, cumulativeGPA

    # takes data from old class instance and creates new updated class instance with same data
    def updateCourseProfile(self, courseName, courseInfoMatrix):
        # old class instance --> self.courseInfo[courseName]
        courseCode = courseInfoMatrix[courseName].getCourseCode()
        courseCredits = courseInfoMatrix[courseName].getCourseCredits()

        self.courseInfo[courseName] = MacBotCourseProfileCreator(courseName, courseCode, courseCredits)

        # checks if courseItemsMatrix2 is filled
        if courseInfoMatrix[courseName].courseItemsMatrix2:
            # transferring old data over to new class object
            self.courseInfo[courseName].courseItemsMatrix = courseInfoMatrix[courseName].courseItemsMatrix2
        # assumes courseItemsMatrix2 is empty
        else:
            self.updateCourseProfileInfo(courseName, courseInfoMatrix[courseName].courseItemsMatrix)

        self.courseInfo[courseName].courseAvg = courseInfoMatrix[courseName].getCourseAvg()
        self.courseInfo[courseName].coursePercentAchieved = courseInfoMatrix[courseName].getCoursePercentAchieved()
        self.courseInfo[courseName].coursePercentWeighted = courseInfoMatrix[courseName].getCoursePercentWeighted()
        self.courseInfo[courseName].course12pGPA = courseInfoMatrix[courseName].getCourse12pGPA()

    # takes data from old class instances and reformat the data (original to updated data format)
    def updateCourseProfileInfo(self, oldCourseName, oldCourseItemsMatrix):
        for courseItem in oldCourseItemsMatrix:
            # creates new dictionary for new item type
            if courseItem[0] not in self.courseInfo[oldCourseName].courseItemsMatrix:
                self.courseInfo[oldCourseName].courseItemsMatrix[courseItem[0]] = {}

            # adds new item entry to course profile item info matrix (with reformatted data)
            self.courseInfo[oldCourseName].courseItemsMatrix[courseItem[0]][courseItem[1]] = [courseItem[2],
                                                                                              [courseItem[3]]]

    # takes data from old class instances and creates new updated class instances with same data
    # FIXME update this later to only transfer each data entry's info rather than entire matrix
    def updateCourseProfiles(self, oldCourseInfoMatrix):
        for course in oldCourseInfoMatrix:
            # update course profile only it has not already been updated
            if course not in self.courseInfo:
                self.updateCourseProfile(course, oldCourseInfoMatrix)

    # quit method
    def quit(self):
        self.saveController()
        print("--------------------------------\nShutting Down Program...")
        quit()


# import management code
if __name__ == "__main__":
    MacUser = MacGradeBot(currentBotVersion)
else:
    pass
