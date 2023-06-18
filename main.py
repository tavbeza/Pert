# Tav Beza

from activity import Activity
from pert import Pert

activities_dict = {"start" : Activity("start", 0), "A" : Activity("A", 4), "B" : Activity("B", 6), "C" : Activity("C", 5),
                   "E" : Activity("E", 2), "D" : Activity("D", 4), "F" : Activity("F", 2)
                    , "G": Activity("G", 5), "H": Activity("H", 8),"I": Activity("I", 5), "K": Activity("K", 6),
                   "end": Activity("end", 0)}

# Define new project/pert and cpm system
p = Pert(activities_dict, "start", "end")

# Connect all the activities
p.connect_activity(p.all_activities["start"], p.all_activities["A"])
p.connect_activity(p.all_activities["start"], p.all_activities["B"])
p.connect_activity(p.all_activities["start"], p.all_activities["C"])
p.connect_activity(p.all_activities["A"], p.all_activities["E"])
p.connect_activity(p.all_activities["B"], p.all_activities["E"])
p.connect_activity(p.all_activities["C"], p.all_activities["D"])
p.connect_activity(p.all_activities["D"], p.all_activities["K"])
p.connect_activity(p.all_activities["E"], p.all_activities["D"])
p.connect_activity(p.all_activities["E"], p.all_activities["F"])
p.connect_activity(p.all_activities["E"], p.all_activities["H"])
p.connect_activity(p.all_activities["E"], p.all_activities["G"])
p.connect_activity(p.all_activities["G"], p.all_activities["K"])
p.connect_activity(p.all_activities["G"], p.all_activities["I"])
p.connect_activity(p.all_activities["F"], p.all_activities["end"])
p.connect_activity(p.all_activities["H"], p.all_activities["end"])
p.connect_activity(p.all_activities["I"], p.all_activities["end"])
p.connect_activity(p.all_activities["K"], p.all_activities["end"])

# Print all the activities
for activity in p.all_activities:
    p.all_activities[activity].print_activity()
print("\n")

# Add new activity and connect to another exist activity
p.add_activity(Activity("R",9))
p.connect_activity(p.all_activities["C"], p.all_activities["R"])
# p.all_activities["C"].connect_activity(p.all_activities["R"])

# After we added an activity, print again
for activity in p.all_activities:
    p.all_activities[activity].print_activity()
print("\n")

# Print isolate activities
print("isolate activities:")
p.isolate_activity(p.all_activities)
print("\n")

# Check if there is a circle in the profect and print the circles
print("circle: \n")
p.connect_activity(p.all_activities["R"], p.all_activities["C"])
# p.all_activities["R"].connect_activity(p.all_activities["C"])
p.validate_circles()
print("\n")

# Print all the activities in the project with __str__ method
print("All the activities in the project:\n",p.__str__())

# Remove activity from the project
p.remove_activity("R")

# After the removal, print again
print("after removal: \n")
for activity in p.all_activities:
    p.all_activities[activity].print_activity()
print("\n")

# Print the critical path
p.find_critical_path()
print("The critical path:")
print("\tSum of durations: %s" % p.critical_path_time)
print("\tPath: %s" % p.critical_path)

# Check slack time
p.define_ES_and_EF()
p.define_LS_and_LF(p.last_activity)
p.slack_time()
print("\n\nafter slack time method\n\n")
print(p.__str__())
print("property:\n")
print(p.project_duration)



