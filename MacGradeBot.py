"""
------------------------------------------------------------------------------------------------------------------------
Programmer(s): Nathaniel Hu
Program Version: 0.0.1 (Developmental)
Last Updated: November 13th, 2019
------------------------------------------------------------------------------------------------------------------------
Program Description
[insert program description]
------------------------------------------------------------------------------------------------------------------------
"""
from time import *
from pickle import *


class MacGradeBot:
    # instantiation of class into new student profile object
    def __init__(self):
        # student user profile information
        self.name = str()
        self.username = str()
        self.password = str()
        self.passwordConfirm = str()
        self.email = str()
        self.emailConfirm = str()
        self.saveFile = str()

        # student course + course information + cumulative average
        self.courses = []
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
        userChoices = ['add', 'edit', "avg"]

        print("Here is your current MacGradeBot student profile:\n" + str(self.courses) + "\n" + str(self.courseInfo) +
              "\n" + str(self.cumulativeAvg))

        while True:
            userChoice = input("Hello, would you like to add/edit a course (add/edit), or calculate your cumulative " +
                               "average (avg): ")

            while userChoice not in userChoices:
                userChoice = input("Please input add/edit here: ")

            # adding a course
            if userChoice == userChoices[0]:
                course = input("Enter your course name here (e.g. ENG 1D04): ")
                grade = float(input("12-Point Grade for {}: ".format(course)))
                credits = int(input("# of credits for {}: ".format(course)))
                self.addCourse(course, [grade, credits])
            # editing a course's info
            elif userChoice == userChoices[1]:
                course = input("Enter the course you would like to edit here: ")
                grade = float(input("Edited 12-Point Grade for {}: ".format(course)))
                credits = int(input("Edited # of credits for {}: ".format(course)))
                self.editCourseInfo(course, [grade, credits])
            else:
                self.calcCumulativeAvg()

            userChoice = input("Would you like to quit (yes/no): ")

            if userChoice == "no":
                pass
            else:
                print("saving student profile")
                self.saveToFile()

                print("shutting down")
                break

    # sign up method
    def signUp(self):
        self.name = input("Name: ")

        self.saveFile = self.name

        self.username = input("Username: ")

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
            user = input("Name: ")
            self.password = input("Password: ")

            # open user save (binary file; .dat)
            with open('{}.dat'.format(user), 'rb') as save:
                self.name, self.username, self.passwordConfirm, self.emailConfirm, self.saveFile, self.courses, \
                    self.courseInfo, self.cumulativeAvg = load(save)

            if user == self.name:
                while True:
                    if self.password == self.passwordConfirm:
                        break
                    else:
                        self.password = input("Re-enter your password here: ")
                break
            else:
                pass

    # method adds course + course info to student profile
    def addCourse(self, course, courseInfo):
        self.courses.append(course)
        self.courseInfo[course] = courseInfo

    # method updates course info for given course in student profile
    def editCourseInfo(self, course, courseInfo):
        self.courseInfo[course] = courseInfo

    # calculates cumulative average
    def calcCumulativeAvg(self):
        averageSum = float()
        creditsSum = int()
        for course in self.courses:
            averageSum += self.courseInfo[course][0] * self.courseInfo[course][1]
            creditsSum += self.courseInfo[course][1]

        self.cumulativeAvg = round(averageSum / creditsSum, 2)

    # saves user profile (binary and text files)
    def saveToFile(self):
        userSaveBinary = [self.name, self.username, self.passwordConfirm, self.emailConfirm, self.saveFile,
                          self.courses, self.courseInfo, self.cumulativeAvg]

        # user save (binary file; .dat)
        with open('{}.dat'.format(self.saveFile), 'wb') as binarySave:
            dump(userSaveBinary, binarySave)

        textSave = open('{}.txt'.format(self.saveFile), 'w')

        text = "======================================= MacGradeBot ======================================\n" + \
               "\n------------------------------------------------------------------------------------------" + \
               "\nName: " + self.name + "\nUsername: " + self.username + "\nPassword: " + self.passwordConfirm + \
               "\nEmail: " + self.emailConfirm + "\nCumulative Average: " + str(self.cumulativeAvg) + \
               "\n------------------------------------------------------------------------------------------" + \
               "\n\n" + "Course Name: [12-Point GPA, # Credits]\n--------------------------------"
        textSave.write(text)
        textSave.close()

        # user save (text file; .txt)
        textSave = open('{}.txt'.format(self.saveFile), 'a')
        for course in self.courses:
            textSave.write("\n{}:\t".format(course))
            textSave.write(str(self.courseInfo[course]))
        textSave.close()


if __name__ == "__main__":
    MacUser = MacGradeBot()
else:
    pass
