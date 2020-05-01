#file for OR-Tools

from __future__ import print_function
from ortools.sat.python import cp_model

class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, shifts, num_courses, num_buildings, num_timeslots, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_courses = num_courses
        self._num_buildings = num_buildings
        self._num_timeslots = num_timeslots
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print("Solution %i" % self._solution_count)
            for b in range(self._num_buildings):
                print("Day %i" % b)
                for c in range(self._num_courses):
                    is_working = False
                    for t in range(self._num_timeslots):
                        if self.Value(self._shifts[(c, b, t)]):
                            is_working = True
                            print(" Course %i works timeslots %i" % (c, t))
                    if not is_working:
                        print(" Course {} does not work" .format(c))
            print()
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count

def main():
    # data
    num_courses = 81
    num_timeslots = 15
    num_buildings = 12
    all_courses = range(num_courses)
    all_timeslots = range(num_timeslots)
    all_buildings = range(num_buildings)
    model = cp_model.CpModel()

    # Creates shift variables
    # shifts[(c, b, t)]: courses 'c', buildings 'b', timeslot 't'
    shifts = {}
    for c in all_courses:
        for b in all_buildings:
            for t in all_timeslots:
                shifts[(c, b, t)] = model.NewBoolVar("shift_c%ib%it%i" % (c, b, t))

#########################adding constraints to the model#########################
    for b in all_buildings:
        for t in all_timeslots:
            model.Add(sum(shifts[(c, b, t)] for c in all_courses) == 1)

    for c in all_courses:
        for b in all_buildings:
            model.Add(sum(shifts[(c, b, t)] for t in all_timeslots) <= 1)


    min_shifts_per_nurse = (num_timeslots * num_buildings) // num_courses
    max_shifts_per_nurse = min_shifts_per_nurse + 1
    for c in all_courses:
        num_shifts_worked = sum(
            shifts[(c, b, t)] for b in all_buildings for t in all_timeslots)
        model.Add(min_shifts_per_nurse <= num_shifts_worked)
        model.Add(num_shifts_worked <= max_shifts_per_nurse)
##################################################################################

    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    a_few_solutions = range(5)
    solution_printer = NursesPartialSolutionPrinter(shifts, num_courses,
                                                    num_buildings, num_timeslots,
                                                    a_few_solutions)
    solver.parameters.max_time_in_seconds = 45.0
    solver.SearchForAllSolutions(model, solution_printer)

    print()
    print('Statistics')
    print('  - conflicts : %i' % solver.NumConflicts())
    print('  - branches : %i' % solver.NumBranches())
    print('  - wall time : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())

if __name__ == '__main__':
    main()
