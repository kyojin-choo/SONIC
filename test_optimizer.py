from constraint import *

test1 = [1, 2, 3]
test2 = [1, 2, 3]

def capacity_constraint(classs, room):
    if classes[classs]  <= rooms[room]:
        return True
    return False

def optimizer(num_courses, num_classrooms):
    problem = Problem()
    problem.addVariable("c", range(num_courses))
    problem.addVariable("r", range(num_classrooms))
    problem.addConstraint(capacity_constraint, ['c', 'r'])
    solutions = problem.getSolutions()
    print(solutions)

    for i in range(len(solutions)):
        print(solutions[i]["c"].title, end=" in ")
        print(solutions[i]["r"].room)
        #print("Test1 at index", solutions[i]["c"], " Test2 at index", solutions[i]["r"])

    print(len(solutions))
