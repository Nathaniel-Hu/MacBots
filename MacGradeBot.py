"""
------------------------------------------------------------------------------------------------------------------------
Programmer(s): Nathaniel Hu
Program Version: 0.0.4 (Developmental)
Last Updated: November 13th, 2019
------------------------------------------------------------------------------------------------------------------------
Program Description
[insert program description]
------------------------------------------------------------------------------------------------------------------------
"""
# this controls program data updating/patching functions/mechanisms in the program
currentBotVersion = 0.0

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
        self.courseInfo = {}
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
        userChoices = ['add', 'edit', 'avg', 'quit']

        print("Here is your current MacGradeBot student profile:\n", str(self.courseNames), "\n", str(self.courseInfo),
              "\n", str(self.cumulativeAvg))

        while True:
            print("MacGradeBot Program")
            userChoice = input("Hello, would you like to add/edit a course (add/edit), calculate your cumulative " +
                               "average (avg), or quit (quit): ")

            while userChoice not in userChoices:
                userChoice = input("Please input add/edit here: ")

            # adding a course
            if userChoice == userChoices[0]:
                self.addCourse()

            # editing a course's info
            elif userChoice == userChoices[1]:
                self.editCourseInfo()

            # calculates course avg
            elif userChoice == userChoices[2]:
                self.calcCumulativeAvg()

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

    # method adds course + course info (creates/adds new course profile) to student profile
    def addCourse(self):
        # gets user inputted information
        courseName = input("Enter your course name (e.g. ENG COMP) here: ").upper()
        courseCode = input("Enter the course code for {} here: ".format(courseName))
        courseCredits = int(input("Enter the # of credits for {} here: ".format(courseName)))

        # appends course name to courseNames; creates new course profile object (class instance)
        self.courseNames.append(courseName)
        self.courseInfo[courseName] = MacBotCourseProfileCreator(courseName, courseCode, courseCredits)

        # references course profile creator main method
        self.courseInfo[courseName].courseProfileMain()

    # allows user to update course grades (labs, assignments, midterm tests and exams, etc.)
    def editCourseInfo(self):
        # gets user inputted information
        courseName = input("Enter the name of the course that you would like to edit here: ").upper()
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
                          self.courseNames, self.courseInfo, self.cumulativeAvg, self.botVersion]

        # user save (binary file; .dat)
        with open('{0}/{0}_MGBSX.dat'.format(self.saveFile), 'wb') as binarySave:
            dump(userSaveBinary, binarySave)

        # user save (text file; .txt)
        textSave = open('{0}/{0}_MGBSX.txt'.format(self.saveFile), 'w')

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
        textSave = open('{0}/{0}_MGBSX.txt'.format(self.saveFile), 'a')
        for course in self.courseNames:
            courseInfo = self.courseInfo[course]
            textSave.write("\n{0} {1}:\t".format(course, courseInfo.courseCode))
            textSave.write("Course Credits: {0}\tCourse Average: {1:<5}\tCourse 12p GPA: {2:<4}".format(
                courseInfo.courseCredits, round(courseInfo.courseAvg, 3), courseInfo.course12pGPA))
        textSave.close()

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
                with open('{0}/{0}_MGBSX.dat'.format(user), 'rb') as save:
                    # unpacks save tuple into multiple parameter entries
                    self.loadSaveData(*load(save))
            # for later patched versions opening older files
            except FileNotFoundError:
                with open('{0}/{0}_MGBS.dat'.format(user), 'rb') as save:
                    # unpacks save tuple into multiple parameter entries
                    self.loadSaveData(*load(save))

    # loads binary file save data into class attributes
    def loadSaveData(self, name, username, passwordConfirm, emailConfirm, saveFile, courseNames, courseInfo,
                     cumulativeAvg, botVersion=0.0):

        if botVersion == 0.0:
            botVersion = currentBotVersion

        self.name, self.username, self.passwordConfirm, self.emailConfirm, self.saveFile, self.courseNames, \
        self.courseInfo, self.cumulativeAvg, self.botVersion = name, username, passwordConfirm, emailConfirm, \
                                                               saveFile, courseNames, courseInfo, cumulativeAvg, \
                                                               botVersion

    # quit method
    def quit(self):
        print("saving student profile")
        if self.botVersion == 0:
            self.saveToFile()
        else:
            self.saveToFile1()
        print("shutting down")
        quit()


# import management code
if __name__ == "__main__":
    MacUser = MacGradeBot(currentBotVersion)
else:
    pass
