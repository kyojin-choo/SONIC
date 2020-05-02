#file for OR-Tools

from __future__ import print_function
from ortools.sat.python import cp_model

class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, classes, num_courses, num_classrooms, num_timeslots, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._classes = classes
        self._num_courses = num_courses
        self._num_classrooms = num_classrooms
        self._num_timeslots = num_timeslots
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print("Solution %i" % self._solution_count)
            for b in range(self._num_classrooms):
                print("Day %i" % b)
                for c in range(self._num_courses):
                    is_working = False
                    for t in range(self._num_timeslots):
                        if self.Value(self._classes[(c, b, t)]):
                            is_working = True
                            print(" Course %i works timeslots %i" % (c, t))
                    if not is_working:
                        print(" Course {} does not work" .format(c))
            print()
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count

def optimizer(num_courses, num_timeslots, num_classrooms, subjects, course_nums, times,
              course_titles, versions, sections, instructor_real_names, capacities, classrooms,
              classroom_capacities):
    # data
    #num_courses = 81
    #num_timeslots = 15
    #num_classrooms = 12
    all_courses = range(num_courses)
    all_timeslots = range(num_timeslots)
    all_classrooms = range(num_classrooms)
    model = cp_model.CpModel()

    # Creates shift variables
    # shifts[(c, b, t)]: courses 'c', buildings 'b', timeslot 't'
    classes = {}
    for b in all_classrooms:
        for c in all_courses:
            classes[(course_titles[c], capacities[c], times[c], classrooms[b])] = model.NewBoolVar("Class_%s, %i, %s, %s" % (course_titles[c], capacities[c], times[c], classrooms[b]))
#            print(classes)
            
    #adding constraints to the model
    for b in all_classrooms:
        for c in all_courses:
            model.Add(capacities[c] <= classroom_capacities[b])
#    for b in all_classrooms:
 #       for t in all_timeslots:
  #          model.Add(sum(shifts[(c, b, t)] for c in all_courses) == 1)

#    for c in all_courses:
 #       for b in all_classrooms:
  #          model.Add(sum(shifts[(c, b, t)] for t in all_timeslots) <= 1)

#    for c in all_courses:
 #       for b in all_classrooms:
  #          print("Class: ", capacities[c])
   #         print("ClassRoom: ", classroom_capacities[b])
    #        model.Add(capacities[c] <= classroom_capacities[b])


   # min_shifts_per_nurse = (num_timeslots * num_classrooms) // num_courses
   # max_shifts_per_nurse = min_shifts_per_nurse + 1
   # for c in all_courses:
    #    num_shifts_worked = sum(
     #       shifts[(c, b, t)] for b in all_classrooms for t in all_timeslots)
     #   model.Add(min_shifts_per_nurse <= num_shifts_worked)
      #  model.Add(num_shifts_worked <= max_shifts_per_nurse)
##################################################################################

    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    a_few_solutions = range(5)
    solution_printer = NursesPartialSolutionPrinter(classes, num_courses,
                                                    num_classrooms, num_timeslots,
                                                    a_few_solutions)
    solver.parameters.max_time_in_seconds = 45.0
    solver.SearchForAllSolutions(model, solution_printer)

    print()
    print('Statistics')
    print('  - conflicts : %i' % solver.NumConflicts())
    print('  - branches : %i' % solver.NumBranches())
    print('  - wall time : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())