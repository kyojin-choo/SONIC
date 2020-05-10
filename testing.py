#Imports
import parse_excel
from ortools.sat.python import cp_model
from constraint import *

#Spreadsheet file names
schedule_file = "Spring 2020 Schedule.xlsx"
classroom_file = "ClassRoom.xlsx"
classes = []
rooms = []
list_of_times = []
buildings = {}
#ite 227, eng 122, sher 151, sher 013, sher 014, sond 109
#meyer, math 106, bio 120, ilsb 233, ilsb 237, pub 105
distances = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

class Class:
    def __init__(self, subject, number, title, section, instructor, time, capacity, version):
        self.subject = subject
        self.number = number
        self.title = title
        self.section = section
        self.instructor = instructor
        self.time = time
        self.capacity = capacity
        self.version = str(version).lower()
        if version == None:
            self.version = ""
        self.course_info = (subject + " " + number + " " + title + self.version + " " + str(section) + " " + instructor)

class Classroom:
    def __init__(self, room, capacity):
        self.room = room
        self.capacity = capacity
        self.classes_in_classroom = []

class Time:
    def __init__(self, time):
        self.classes_at_time = []
        self.actual_time = time

def determine_unique_timeslots(classtimes):
    timeslots = []
    
    for time in classtimes:
        #.lower fixes MW230 mw230 from being different
        if time.lower() not in timeslots:
            timeslots.append(time)
    
    return timeslots

"""
optimizer

input: l, t
l: list of classes
t: time solutions

Description:
A series of single solution opimizations

Note: doing all optimizations at once caused slow runtime and may lead to memory errors
"""
def optimizer(l, t):
    problem = Problem()
    problem.addVariable(t, l)
    return problem.getSolutions()

def main():

    #Get lists from schedule excel sheet
    subjects, course_nums, course_titles, versions, sections, instructor_real_names, times, capacities = parse_excel.load_schedule_hardcoded(schedule_file)
    #Get lists from classroom excel sheets
    classrooms, classroom_capacities = parse_excel.load_classrooms_hardcoded(classroom_file)
    
    #Use information from excel files for ortools optimization
    num_courses = len(subjects)
    
    unique_times = determine_unique_timeslots(times)
    
    num_classrooms = len(classrooms)

    num_classtimes = len(unique_times)

    for i in range(num_courses):
        _class = Class(subjects[i], course_nums[i], course_titles[i], sections[i], instructor_real_names[i], times[i], capacities[i], versions[i])
        classes.append(_class)

    for i in range(num_classrooms):
        room = Classroom(classrooms[i], classroom_capacities[i])
        rooms.append(room)

    for t in unique_times:
        time_instance = Time(t)
        list_of_times.append(time_instance)

    for r in range(num_classrooms):
        for c in range(num_courses):
            if rooms[r].capacity >= classes[c].capacity:
                rooms[r].classes_in_classroom.append(classes[c])

    for t in range(num_classtimes):
        for c in range(num_courses):
            if list_of_times[t].actual_time == classes[c].time:
                list_of_times[t].classes_at_time.append(classes[c])

    time_solutions = []
    for t in list_of_times:
        l = []
        for c in t.classes_at_time:
            l.append(c.course_info)
        for i in range(len(l)):
            solution = optimizer([l[i]], t.actual_time)
            time_solutions.append(solution)

    room_solutions = []
    for r in rooms:
        rt = []
        for c in r.classes_in_classroom:
            rt.append(c.course_info)
        for j in range(len(rt)):
            solution = optimizer([rt[j]], r.room)
            room_solutions.append(solution)
    dicts = []
    for i in range(len(time_solutions)):
        for j in range(len(time_solutions[i])):
            dicts.append(time_solutions[i][j])

    for i in range(len(room_solutions)):
        for j in range(len(room_solutions[i])):
            dicts.append(room_solutions[i][j])

    lists = {}
    for d in dicts:
        (k, v), = d.items()
        if v in lists:
            temp = lists[v]
            temp.append(k)
            lists[v] = temp
        else:

            new_entry = [k]
            lists[v] = new_entry

    """
    TODO
    create schedule of classes,  
    """
    schedule = {}
    count = 0
    for k,v in lists.items():
        if(count == len(lists)-1):
            v.insert(0, "mw230")
        count += 1
        time = v[0]
        course_info = k
        possible_rooms = v[1:]
        building = v[-1]
        if time in schedule:
            temp = schedule[time]
            if building in temp:
                conflict = True
                for b in reversed(v[1:]):
                    if b not in temp:
                        conflict = False
                        temp.append(b)
                        temp.append(course_info)
                        schedule[time] = temp
                        break
                if conflict == True:
                    print("Error: The class", course_info, "could not be scheduled at the timeslot", time)
                    exit()
            else:
                temp.append(building)
                temp.append(course_info)
                schedule[time] = temp
        else:
            schedule[time] = [building, course_info]
    #print(schedule)
    #'''

    print("Schedule by Sonic Scheduler:\n")
    for k, v in schedule.items():
        print("**********************************************")
        print("Classes at time: ", k)
        print("**********************************************")
        for i in range(len(v)):
            if i % 2 == 0:
                print("\nBuilding: ", v[i])
            else:
                print("Class: ", v[i])
        print("\n")
    #'''    
    

main()
