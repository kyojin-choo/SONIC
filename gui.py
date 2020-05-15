# gui.py - GUI-fied version of Schedule Optimizer for Near Ideal Classes)\
#
# Author(s): Daniel Choo
# Date:      05/13/20
# URL:       https://www.github.com/kyoogoo/SONIC

import os
import sys
from constraint import *
from ortools.sat.python import cp_model
from Program_Files import parse_excel

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen


# Global Variables
global SUBJECTS
global COURSE_NUMS
global COURSE_TITLES
global VERSIONS
global SECTIONS
global INSTRUCTOR_REAL_NAMES
global TIMES
global CAPACITIES
global CLASSROOMS
global CLASSROOM_CAPACITIES


class Class:
    """ Class():
        Class Object - stores all of the relevant data to class.

        Input(s):     None [None]
        Return(s):    None [None]
    """
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
        self.course_info = (subject + " " + number + " " + title + self.version + " " + '\nSection: ' + str(section) + "\nInstructor: " + instructor)


class Classroom:
    """ Classroom():
        Classroom Object - stores all of the relevant data to classrooms.

        Input(s):     None [None]
        Return(s):    None [None]
    """
    def __init__(self, room, capacity):
        self.room = room
        self.capacity = capacity
        self.classes_in_classroom = []


class Time:
    """ Time():
        Time Object - stores all of the relevant data in respect to time.

        Input(s):     None [None]
        Return(s):    None [None]
    """
    def __init__(self, time):
        self.classes_at_time = []
        self.actual_time = time


class WelcomeScreen(Screen):
    """ WelcomeScreen():
        Handled in SONIC.kv

        Input(s):     None [None]
        Return(s):    None [None]
    """
    pass


class MenuScreen(Screen):
    """ MenuScreen():
        Handled in SONIC.kv

        Input(s):     None [None]
        Return(s):    None [None]
    """
    pass


class ClassroomParser(Screen):
    """ ClassroomParser():
        The screen that is shown following clicking 'parse .xlsx (Classroom)'

        Input(s):     Screen [Kivy Screen Object]
        Return(s):    None [None]
    """

    def __init__(self, **kwargs):
        """ __init__(**kwargs)):
            ClassroomParser() bootstrapper.

            Input(s):     **kwargs [args]
            Return(s):    None [None]
        """
        super(ClassroomParser, self).__init__(**kwargs)

        # Initializing variables.
        self.counter = 0

        # Initializing our screen layout.
        self.inside = FloatLayout()
        with self.inside.canvas.before:
            Color(0.525, 0.576, 0.671, 1)
            self.rect = Rectangle(size=self.inside.size, pos=self.inside.pos)

        # Inside the FloatLayout
        self.add_widget(Label(text='Loading .xlsx (Classroom)', bold=True, font_size=56,
                              size_hint=(0.2, 0.2), pos=(625, 575)))

        self.user_input = TextInput(multiline=False, cursor_blink=True,
                                    write_tab=False, size_hint=(0.5, None),
                                    pos_hint={"center_x":0.5,"center_y":0.5},
                                    height=50, hint_text="Please input file path here.",
                                    hint_text_color=(0.43921568627, 0.42352941176, 0.38039215686, 0.5),
                                    foreground_color=(0.53725490196, 0.61960784313, 0.54509803921, 1))

        # TextInput Actions
        self.user_input.bind(text=self.on_text)
        self.user_input.bind(on_text_validate=self.validation)
        self.inside.add_widget(self.user_input)

        # Adding Interior Layout
        self.add_widget(self.inside)

        # Labels (text in GUI)
        self.error_label = Label(text="",
                                 color=(0.761, 0.231, 0.133, 1),
                                 size_hint=(0.2, 0.2), pos=(625, 350))
        self.add_widget(self.error_label)

        # Button Functionality
        self.cont = Button(text="Continue", font_size=28,
                           background_color=(0.46666666666, 0.86666666666, 0.46666666666, 0.85),
                           color=(0.74117647058, 0.83137254902, 0.90588235294, 1),
                           size_hint=(0.1, 0.075), pos=(1000, 150))

        self.cont.bind(on_release=self.validation)
        self.add_widget(self.cont)

    def on_text(self, instance, value):
        """ on_text(self, instance, value):
            Debugging purposes; prints out the value to the terminal.

            Input(s):     Instance (Kivy TextInput Object), Value [instance.text]
            Return(s):    None [None]
        """
        print('The widget', instance, 'have:', value)

    def validation(self, instance):
        """ validation(self, instance):
            Checking whether or not the user's input is correct or not.
            Cases:
                1. If the extension is not .xlsx:
                   Warn the user that the extension is incorrect.

                2. If the path does not exist:
                   Warn the user that the path does not exist.

                3. If the path does exist:
                   Open the file and show a progress bar to show progress.

            Input(s):     value (Kivy TextInput Object)
            Return(s):    None [None]
        """
        # Make sure we're getting new data.
        check = self.user_input.text

        # If the last five values are not .xlsx, say improper file type.
        if check[-5:] != ".xlsx":
            self.error_label.text = "That is not the correct file type. Try again."

        # If the file/path does not exist, say the path does not exist.
        elif not os.path.exists(check):
            self.error_label.text = "That file/path does not exist. Try again."

        # If the path exists, then start the excel scraping process.
        else:
            global CLASSROOMS, CLASSROOM_CAPACITIES

            # If it already exists.
            if self.counter >= 1:
                del CLASSROOMS, CLASSROOM_CAPACITIES

            self.error_label.text = ""
            CLASSROOMS, CLASSROOM_CAPACITIES = parse_excel.load_classrooms_hardcoded(check)
            self.counter+=1 
            sm.current = "Menu"


class CatalogParser(Screen):
    """ CatalogParser():
        The screen that is shown following clicking 'parse .xlsx (Catalog)'

        Input(s):     Screen [Kivy Screen Object]
        Return(s):    None [None]
    """
    def __init__(self, **kwargs):
        """ __init__(**kwargs)):
            ClassParser() bootstrapper.

            Input(s):     **kwargs [args]
            Return(s):    None [None]
        """
        super(CatalogParser, self).__init__(**kwargs)

        # Initializing variables.
        self.counter = 0

        # Initializing our screen layout.
        self.inside = FloatLayout()
        with self.inside.canvas.before:
            Color(0.525, 0.576, 0.671, 1)
            self.rect = Rectangle(size=self.inside.size, pos=self.inside.pos)

        # Inside the screen layout.
        self.add_widget(Label(text='Loading .xlsx (Catalog)', bold=True, font_size=56,
                              size_hint=(0.2, 0.2), pos=(625, 575)))

        self.user_input = TextInput(multiline=False, cursor_blink=True,
                                    write_tab=False, size_hint=(0.5, None),
                                    pos_hint={"center_x":0.5,"center_y":0.5},
                                    height=50, hint_text="Please input file path here.",
                                    hint_text_color=(0.43921568627, 0.42352941176, 0.38039215686, 0.5),
                                    foreground_color=(0.53725490196, 0.61960784313, 0.54509803921, 1))

        # TextInput Actions
        self.user_input.bind(text=self.on_text)
        self.user_input.bind(on_text_validate=self.validation)
        self.inside.add_widget(self.user_input)

        # Adding Interior Layout
        self.add_widget(self.inside)

        # Labels (text in GUI)
        self.error_label = Label(text="",
                                 color=(0.761, 0.231, 0.133, 1),
                                 size_hint=(0.2, 0.2), pos=(625, 350))
        self.add_widget(self.error_label)

        # Button Functionality
        self.cont = Button(text="Continue", font_size=28,
                           background_color=(0.46666666666, 0.86666666666, 0.46666666666, 0.85),
                           color=(0.74117647058, 0.83137254902, 0.90588235294, 1),
                           size_hint=(0.1, 0.075), pos=(1000, 150))

        self.cont.bind(on_release=self.validation)
        self.add_widget(self.cont)

    def on_text(self, instance, value):
        """ on_text(self, instance, value):
            Debugging purposes; prints out the value to the terminal.

            Input(s):     Instance (Kivy TextInput Object), Value [instance.text]
            Return(s):    None [None]
        """
        print('The widget', instance, 'have:', value)

    def validation(self, value):
        """ validation(self, value):
            Checking whether or not the user's input is correct or not.
            Cases:
                1. If the extension is not .xlsx:
                   Warn the user that the extension is incorrect.

                2. If the path does not exist:
                   Warn the user that the path does not exist.

                3. If the path does exist:
                   Open the file and show a progress bar to show progress.

            Input(s):     value (Kivy TextInput Object)
            Return(s):    None [None]
        """
        # Initialize our check variable.
        check = self.user_input.text

        # If the last five values are not .xlsx, say improper file type.
        if check[-5:] != ".xlsx":
            self.error_label.text = "That is not the correct file type. Try again."

        # If the file/path does not exist, say the path does not exist.
        elif not os.path.exists(check):
            self.error_label.text = "That file/path does not exist. Try again."

        # If the path exists, then start the excel scraping process.
        else:
            # Time to change our globals.
            global SUBJECTS, COURSE_NUMS, COURSE_TITLES
            global VERSIONS, SECTIONS, INSTRUCTOR_REAL_NAMES
            global TIMES, CAPACITIES

            # Gotta make sure we're getting new input!
            if self.counter >= 1:
                del SUBJECTS, COURSE_NUMS, COURSE_TITLES, VERSIONS, SECTIONS, INSTRUCTOR_REAL_NAMES, TIMES, CAPACITIES

            self.error_label.text = ""
            SUBJECTS, COURSE_NUMS, COURSE_TITLES, VERSIONS, SECTIONS, INSTRUCTOR_REAL_NAMES, TIMES, CAPACITIES = parse_excel.load_schedule_hardcoded(check)
            self.counter+=1 
            sm.current = "Menu"


class OptScreen(Screen):
    """ OptScreen():
        The screen that is shown following clicking 'Optimize Schedule'

        Input(s):     Screen [Kivy Screen Object]
        Return(s):    None [None]
    """
    def __init__(self, **kwargs):
        """ __init__(**kwargs)):
            OptScreen() bootstrapper.

            Input(s):     **kwargs [args]
            Return(s):    None [None]
        """
        super(OptScreen, self).__init__(**kwargs)

        # Labels (text in GUI)
        self.output = Label(text="No Schedule",
                            color=(0.0, 0.0, 0.0, 1),
                            size_hint=(0.2, 0.2), pos=(625, 500))

#        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Initializing FloatLayout Screen
#        self.inside = FloatLayout()
#        with self.inside.canvas.before:
#            Color(0.525, 0.576, 0.671, 1)
#           self.rect = Rectangle(size=self.inside.size, pos=self.inside.pos)

        self.add_widget(self.output)
#        self.root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
#        self.root.add_widget(layout)

        # Button functionality
        self.cont = Button(text="Start Optimize", font_size=28,
                           background_color=(0.46666666666, 0.86666666666, 0.46666666666, 0.85),
                           color=(0.74117647058, 0.83137254902, 0.90588235294, 1),
                           size_hint=(0.15, 0.075), pos=(1000, 150))

        self.cont.bind(on_release=self.optimize)
        self.add_widget(self.cont)


    def print_schedule(self, schedule):
        """ print_schedule(self, schedule): [from main.py]
            Outputs an organized schedule by time; includes all the classes
            and all of their locations by time. Essentially prints final
            schedule.

            Input(s):    schedule [dict]
            Return(s):   class_str [str]
        """
        class_str = ""

        print("Schedule by Sonic Scheduler:\n")
        for k, v in schedule.items():
            print("**********************************************")
            print("Classes at time: ", k)
            class_str += ("\nClasses at time: " + str(k) + "\n-------------------------")
            print("**********************************************")
            for i in range(len(v)):
                if i % 2 == 0:
                    print("\nLocation: ", v[i])
                    class_str += ("\n\nLocation: " + v[i])
                else:
                    print("Class: ", v[i])
                    class_str += ("\nClass: " + v[i])

            print("\n")
            class_str += "\n"

        return class_str

    def print_conflicts(self, not_scheduled):
        """ print_conflicts(self, not_scheduled):
            Loops and prints out all the error messages for each class that could
            not be scheduled properly.

            Input(s):    not_scheduled [list]
            Output(s):   conflict_str [None]
        """
        conflict_str = ""

        if not not_scheduled:
            print("**********************************************")
            print("All classes were successfully scheduled")
            conflict_str += "\nAll classes were successfully scheduled!"
        else:
            print("----------------------------------------------\n")
            print("NOTICE: The following class(es) could not be scheduled\n")
            conflict_str += "\nNOTICE: The following class(es) could not be scheduled\n\n"
            for s in not_scheduled:
                print(s)
                print("----------------------------------------------\n")
                conflict_str += (s + "\n")

        return conflict_str

    def determine_unique_timeslots(self, classtimes):
        """ determine_unique_timeslots(self, classtimes)
            Takes in a list of classtimes and count how many times are actually
            unique in the list, and add each unique time to a list

            Input(s):    classtimes [List]
            Return(s):   timeslots  [List]
        """
        # Initializing list
        timeslots = []

        for time in classtimes:
            # lower fixes MW230 mw230 from being different
            if time.lower() not in timeslots:
                timeslots.append(time)

        return timeslots

    def optimizer(self, l, t):
        """ optimizer(self, l, t):
            See main.py for further elaboration.

            Input(s):    l, t [lists]
            Output(s):   problem.getSolutions() [constraints]
        """
        problem = Problem()
        problem.addVariable(t, l)
        return problem.getSolutions()

    def optimize(self, ignore):
        """ optimize(self):
            Creating an optimized class schedule. (Taken from main.py)

            Input(s):    Ignore (Kivy Object): We dont need to worry about this
            Return(s):   None [None]
        """
        # Checking before we continue
        if len(SUBJECTS) <= 0:
            print("here sub")
            sys.exit(0)

        if len(CLASSROOMS) <= 0:
            print("here class")
            sys.exit(0)

        # Instantating variables.
        classes = []
        rooms = []
        list_of_times = []
        num_courses = len(SUBJECTS)
        num_classrooms = len(CLASSROOMS)
        unique_times = self.determine_unique_timeslots(TIMES)
        num_classtimes = len(unique_times)

        """
            These 3 loops take the data read in and create objects that are put into their respective lists
            that are used through out the code
            1. classes
            2. classrooms
            3. times
        """

        for i in range(num_courses):
            _class = Class(SUBJECTS[i], COURSE_NUMS[i], COURSE_TITLES[i], SECTIONS[i], INSTRUCTOR_REAL_NAMES[i], TIMES[i], CAPACITIES[i], VERSIONS[i])
            classes.append(_class)

        for i in range(num_classrooms):
            room = Classroom(CLASSROOMS[i], CLASSROOM_CAPACITIES[i])
            rooms.append(room)

        for t in unique_times:
            time_instance = Time(t)
            list_of_times.append(time_instance)

        # Add classes that fit into classroom to that classroom's list
        for r in range(num_classrooms):
            for c in range(num_courses):
                if rooms[r].capacity >= classes[c].capacity:
                    rooms[r].classes_in_classroom.append(classes[c])

        # Add classes at that time to that time's list
        for t in range(num_classtimes):
            for c in range(num_courses):
                if list_of_times[t].actual_time == classes[c].time:
                    list_of_times[t].classes_at_time.append(classes[c])

        """
            Generates time constraints using python constraint
        """
        time_solutions = []
        for t in list_of_times:
            l = []
            for c in t.classes_at_time:
                l.append(c.course_info)
            for s in range(len(l)):
                solution = self.optimizer([l[s]], t.actual_time)
                time_solutions.append(solution)

        """
            Generates room constraints using python constraint
        """
        room_solutions = []
        for r in rooms:
            rt = []
            for c in r.classes_in_classroom:
                rt.append(c.course_info)
            for j in range(len(rt)):
                solution = self.optimizer([rt[j]], r.room)
                room_solutions.append(solution)

        """
            Rearrange data structure recieved from python constraint to retrieve schedule
        """
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
            Format schedule from constraints
        """
        schedule = {}
        count = 0
        not_scheduled = []
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

                    """
                    handles the case where all of the possible buildings the current class can be scheduled into
                    are full
                    """
                    if conflict == True:
                        error_msg = "All possible classrooms filled at timeslot: " + time + "\n" + course_info
                        not_scheduled.append(error_msg)
                else:
                    temp.append(building)
                    temp.append(course_info)
                    schedule[time] = temp
            else:
                schedule[time] = [building, course_info]

        # Print to the console for verification
        schedule = self.print_schedule(schedule)
        conflict = self.print_conflicts(not_scheduled)
        self.output.text = schedule + "\n" + conflict
        print(self.output)


class ScreenManagement(ScreenManager):
    """ ScreenManagement():
        Handles all of the screen movement.

        Input(s):    ScreenManager [Kivy ScreenManager Object]
        Output(s):   None [None]
    """
    pass


# Load in those files
Builder.load_file("SONIC.kv")

# Initializing our screen manager.
sm = ScreenManager()
sm.add_widget(WelcomeScreen(name='Welcome'))
sm.add_widget(MenuScreen(name='Menu'))
sm.add_widget(ClassroomParser(name='ClassroomParser'))
sm.add_widget(CatalogParser(name='CatalogParser'))
sm.add_widget(OptScreen(name='Optimize'))


class SonicApp(App):
    """ class SONIC_GUI(App):
        GUI class for SONIC

        Input(s):     App  [Kivy App Class]
        Return(s):    None [None]
    """
    def build(self):
        # Name of our GUI
        self.title = "S O N I C"
        return sm


# Execute GUI
if __name__ == "__main__":
    SonicApp().run()
