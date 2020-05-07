#Imports
import parse_excel
import test_optimizer
from constraint import *

#Spreadsheet file names
schedule_file = "Spring 2020 Schedule.xlsx"
classroom_file = "ClassRoom.xlsx"
classes = []
rooms = []

class Class:
    def __init__(self, subject, number, title, section, instructor, time, capacity):
        self.subject = subject
        self.number = number
        self.title = title
        self.section = section
        self.instructor = instructor
        self.time = time
        self.capacity = capacity

    def printClass(c):
        print("%s %s at %s has capacity %i" % (c.subject, c.number, c.time, c.capacity))

class Classroom:
    def __init__(self, room, capacity):
        self.room = room
        self.capacity = capacity

    def printClassroom(c):
        print("%s has capacity %i" % (c.room, c.capacity))

def determine_unique_timeslots(classtimes):
    timeslots = []
    
    for time in classtimes:
        if time not in timeslots:
            timeslots.append(time)
    
    return timeslots


def capacity_constraint(classs, room):
    if classes[classs].capacity  <= rooms[room].capacity:
        return True
    return False

def optimizer(num_courses, num_classrooms):
    problem = Problem()
    problem.addVariable("c", range(num_courses))
    problem.addVariable("r", range(num_classrooms))
    problem.addConstraint(capacity_constraint, ['c', 'r'])
    solutions = problem.getSolutions()
    
    for i in range(len(solutions)):
        print(rooms[solutions[i]["r"]].room)
    print(len(solutions))


def main():

    #Get lists from schedule excel sheet
    subjects, course_nums, course_titles, versions, sections, instructor_real_names, times, capacities = parse_excel.load_schedule_hardcoded(schedule_file)

    #Get lists from classroom excel sheets
    classrooms, classroom_capacities = parse_excel.load_classrooms_hardcoded(classroom_file)
    
    
    #Use information from excel files for ortools optimization
    num_courses = len(subjects)
    
    unique_times = determine_unique_timeslots(times)
    num_classtimes = len(unique_times)
    
    num_classrooms = len(classrooms)

    for i in range(num_courses):
        _class = Class(subjects[i], course_nums[i], course_titles[i], sections[i], instructor_real_names[i], times[i], capacities[i])
        classes.append(_class)

    for i in range(num_classrooms):
        room = Classroom(classrooms[i], classroom_capacities[i])
        rooms.append(room)
    
    #test_optimizer.optimizer(num_courses, num_classrooms)
    optimizer(num_courses, num_classrooms)

main()
