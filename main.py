#Imports
import parse_excel
import optimizer

#Spreadsheet file names
schedule_file = "Spring 2020 Schedule.xlsx"
classroom_file = "ClassRoom.xlsx"


def determine_unique_timeslots(classtimes):
    timeslots = []
    
    for time in classtimes:
        if time not in timeslots:
            timeslots.append(time)
    
    return timeslots



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

    optimizer.optimizer(num_courses, num_classtimes, num_classrooms, subjects, course_nums, times,
                        course_titles, versions, sections, instructor_real_names, capacities, classrooms)

main()
