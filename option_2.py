# An introductory/draft program to practice CSP solving using python-constraint for course scheduling

# Import constraint
from constraint import *

# Declare a dictionary to hold the variables and domains of faculty, courses, classrooms, days and times
varDomainDict = {"professor" : ["Tim", "Fred"], "course" : ["CMSC471", "CMSC478", "CMSC473", "CMSC491"],
                        "classroom" : ["ILSB116A", "ILSB233"], "day" : ["Mon", "Wed", "Tue", "Thu"],
                        "time" : ["10:00", "11:30", "2:30", "4:00"]}

# Create a constraint satisfaction problem
csp = Problem()

# Add the dict key, value as Variable and their domains to problem
for key, value in varDomainDict.items():
    csp.addVariable(key, value)

### START CODE HERE ###
# Functions to implement constraints - NO PARTIAL CREDIT: You must implement everything correctly!
# You must use implies function for all constraints.
# /---------------------------------------------------------------

# Function implies takes P and Q, if P => Q is true, it returns true - Hint: Use implication elimination
def implies(p, q):
    if (( not p) or q):
        return True

# Tim does not teach on Mon and Wed - This constraint is provided to help you write others
def dayConstraint(professor, day):
    if implies(professor == "Tim", (day != "Mon" and day != "Wed")):
        return True

# Tim teaches only at 4:00 AND Fred does not teach at 10:00
def timeConstraint(professor, time):
    if (implies(professor == "Tim" , time == "4:00" ) and implies(professor == "Fred", time != "10:00")): 
        return True
    
# ILSB233 is not available on Wed AND ILSB116A is not available on Mon
def classroomConstraint(classroom, day):
    if (implies( classroom  == "ILSB233", day != "Wed") and implies(classroom == "ILSB116A", day !="Mon")):
        return True
    
# Fred doesn't teach CMSC473 AND Tim doesn't teach CMSC478
def courseConstraint(professor, course):
    if ( implies(professor == "Fred", course != "CMSC473") and implies(professor == "Tim", course != "CMSC478")):
        return True

# /---------------------------------------------------------------

# addConstraint dayConstraint - This one is provided to help you write others.
csp.addConstraint(dayConstraint, ['professor', 'day'])

# Add all other three constraints
csp.addConstraint(timeConstraint, ['professor', 'time'])
csp.addConstraint(classroomConstraint, ['classroom', 'day'])
csp.addConstraint(courseConstraint, ['professor', 'course'])

### END CODE HERE ###

# Get solutions and print it
solutions = csp.getSolutions()
print(len(solutions), "assignments found:")
print('\n'.join('{}: {}'.format(*k) for k in enumerate(solutions))) 
