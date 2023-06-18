import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('GraphLogger')
handler.setLevel(logging.INFO)

# Add the handler to the logger
logger.addHandler(handler)


class Pert:
    all_activities = {}
    critical_path = ""
    critical_path_time = 0

    def __init__(self, activity_dict = None, first_activity_name = None, last_activity_name = None):
        self.all_activities = activity_dict
        self.first_activity = first_activity_name
        self.last_activity = last_activity_name
        self.circles = ""

    def add_activity(self, activity):
        logger.info('Function add_activity has start')
        self.all_activities[activity.name] = activity
        if len(self.all_activities) > 1:
            self.find_critical_path()
            self.check_validate_circles()
        logger.info('Function add_activity has finish')

    def connect_activity(self, activity_connect_to, activity):
        logger.info('Function connect_activity has start')
        self.all_activities[activity_connect_to.name].links[activity.name] = activity
        self.all_activities[activity.name].fathers[activity_connect_to.name] = activity_connect_to
        self.check_validate_circles()
        if len(self.all_activities[self.last_activity].fathers) > 0  and len(self.circles) == 0 :
            self.find_critical_path()
            self.check_validate_circles()
        logger.info('Function connect_activity has finish')

    def remove_activity(self, activity_name):
        logger.info('Function remove_activity has start')
        if activity_name in self.all_activities:
            for activity in self.all_activities:
                if activity_name in self.all_activities[activity].links:
                    del self.all_activities[activity].links[activity_name]
                if activity_name in self.all_activities[activity].fathers:
                    del self.all_activities[activity].fathers[activity_name]
            del self.all_activities[activity_name]
            self.find_critical_path()
        logger.info('Function remove_activity has finish')

    def isolate_activity(self, activities=None):
        first_list = {}

        # First we collect all the activities without links
        for activity in activities:
            if activity != self.last_activity and activity != self.first_activity:
                if len(activities[activity].links) == 0:
                    first_list[activity] = activities[activity]

        temp_list = {}
        for activity in activities:
            if activity != self.last_activity and activity != self.first_activity:
                for link in activities:
                    if activity in activities[link].links:
                        temp_list[activity] = activities[activity]

        for activity in activities:
            if activity != self.last_activity and activity != self.first_activity and activity not in temp_list:
                first_list[activity] = activities[activity]

        if len(first_list) == 0:
            print("*There is no isolate activities*")
        else:
            for isolate_activity in first_list:
                print("Activity ",isolate_activity)

    def check_validate_circles(self, current_activity = None, visited_items = {}):
        logger.debug('Function check_validate_circles has start')
        if len(visited_items) == 0:
            self.circles = ""
            temp_dict = {}
            temp_dict[self.first_activity] = self.all_activities[self.first_activity]
            self.check_validate_circles(temp_dict[self.first_activity],temp_dict)
        else:
            count = 0
            for link in current_activity.links:
                if link in visited_items:
                    for item_to_print in visited_items:
                        if self.all_activities[link] != visited_items[item_to_print]:
                            count += 1
                        else:
                            break
                    i = 0
                    for activity in visited_items:
                        if i >= count:
                            self.circles += visited_items[activity].name
                        i += 1
                    self.circles += ""
                else:
                    visited_items2 = visited_items.copy()
                    visited_items2[link] = current_activity.links[link]
                    self.check_validate_circles(visited_items2[link],visited_items2)
        logger.debug('Function check_validate_circles has finish')

    def validate_circles(self, current_activity = None, visited_items = {}):
        logger.debug('Function validate_circles has start')
        if len(visited_items) == 0:
            self.circles = ""
            temp_dict = {}
            temp_dict[self.first_activity] = self.all_activities[self.first_activity]
            self.validate_circles(temp_dict[self.first_activity],temp_dict)
        else:
            count = 0
            for link in current_activity.links:
                if link in visited_items:
                    for item_to_print in visited_items:
                        if self.all_activities[link] != visited_items[item_to_print]:
                            count += 1
                        else:
                            break
                    i = 0
                    for activity in visited_items:
                        if i >= count:
                            print(visited_items[activity].name)
                            self.circles += visited_items[activity].name
                        i += 1
                    self.circles += ""
                    print("***")
                else:
                    visited_items2 = visited_items.copy()
                    visited_items2[link] = current_activity.links[link]
                    self.validate_circles(visited_items2[link],visited_items2)
        logger.debug('Function validate_circles has finish')

    def __str__(self):
        logger.info('Function __str__ has start')
        str = "STR:\n"
        for activity in self.all_activities:
            str += "Activity %s:\n\t\tname:%s\n\t\tduration:%s" % \
                   (self.all_activities[activity].name,self.all_activities[activity].name, self.all_activities[activity].duration)
            str += "\n\t\tearly start:%s " % self.all_activities[activity].ES
            str += "\n\t\tlast start:%s" % self.all_activities[activity].LS
            str += "\n\t\tearly final:%s" % self.all_activities[activity].EF
            str += "\n\t\tlast final:%s" % self.all_activities[activity].LF
            str += "\n\t\tslack time:%s" % self.all_activities[activity].slack_time
            str += "\n\t\tlinks:"
            for link in self.all_activities[activity].links:
                str += " '%s' " % (link)
            str += "\n\t\tprevious:"
            for father in self.all_activities[activity].fathers:
                str += "'%s' " % self.all_activities[activity].fathers[father].name
            str += "\n"
        logger.info('Function __str__ has finish')
        return str

    def find_critical_path(self,current_activity=None, visited_items={}, max_duration = 0, sum_of_durations = None):
        logger.debug('Function find_critical_path has start')
        if len(visited_items) == 0:
            temp_dict = {}
            max_duration1 = 0
            sum_of_durations = []
            temp_dict[self.first_activity] = self.all_activities[self.first_activity]
            self.find_critical_path(temp_dict[self.first_activity], temp_dict, max_duration1,sum_of_durations)
            self.critical_path_time = sum_of_durations[0]

        else:
            max_duration += current_activity.duration
            if current_activity.name == self.last_activity:
                if len(sum_of_durations) == 0:
                    sum_of_durations.append(max_duration)
                    path1 = ""
                    for name in visited_items:
                        path1 += "'%s' " % visited_items[name].name
                    self.critical_path = path1
                else:
                    if sum_of_durations[0] < max_duration:
                        sum_of_durations.pop(0)
                        sum_of_durations.append(max_duration)
                        path1 = ""
                        for name in visited_items:
                            path1 += "'%s' " % visited_items[name].name
                        self.critical_path = path1

            for link in current_activity.links:
                if current_activity.links[link] in visited_items:
                    self.find_critical_path(visited_items2[link], visited_items2, max_duration, sum_of_durations)
                else:
                    visited_items2 = visited_items.copy()
                    visited_items2[link] = current_activity.links[link]
                    self.find_critical_path(visited_items2[link], visited_items2, max_duration, sum_of_durations)
        logger.debug('Function find_critical_path has finish')

    def define_ES_and_EF(self):
        logger.debug('Function define_ES_and_EF has start')
        # Define all the first and all the last, and early_start + early_final for each activity
        for activity in self.all_activities:
            if self.all_activities[activity].name == self.first_activity:
                self.all_activities[activity].ES = 0
                self.all_activities[activity].EF = self.all_activities[activity].duration
                self.all_activities[activity].LS = 0
                self.all_activities[activity].LF = self.all_activities[activity].duration
            elif self.all_activities[activity].name == self.last_activity:
                self.all_activities[activity].ES = self.critical_path_time - self.all_activities[activity].duration
                self.all_activities[activity].LS = self.critical_path_time - self.all_activities[activity].duration
                self.all_activities[activity].EF = self.critical_path_time
                self.all_activities[activity].LF = self.critical_path_time
            else:
                max_EF = 0
                for father in self.all_activities[activity].fathers:
                    if len(self.all_activities[activity].fathers) == 1:
                        self.all_activities[activity].ES = self.all_activities[activity].fathers[father].EF
                        self.all_activities[activity].EF =\
                            self.all_activities[activity].ES + self.all_activities[activity].duration
                    else:
                        if self.all_activities[activity].fathers[father].EF > max_EF:
                            max_EF = self.all_activities[activity].fathers[father].EF
                            self.all_activities[activity].ES = max_EF
                            self.all_activities[activity].EF =\
                                self.all_activities[activity].ES + self.all_activities[activity].duration
        logger.debug('Function define_ES_and_EF has finish')

    # Define last_start + last_final for each activity
    def define_LS_and_LF(self, last_activity = None):
        logger.debug('Function define_LS_and_LF has start')
        if last_activity == self.first_activity:
            pass
        else:
            min_LS = []
            for father in self.all_activities[last_activity].fathers:
                if self.all_activities[father].LF != None:
                    if self.all_activities[father].LF > self.all_activities[last_activity].LS:
                        self.all_activities[father].LF = self.all_activities[last_activity].LS
                        self.all_activities[father].LS = self.all_activities[father].LF - self.all_activities[father].duration

                else:
                    self.all_activities[father].LF = self.all_activities[last_activity].LS
                    self.all_activities[father].LS = self.all_activities[father].LF - self.all_activities[father].duration
            for father in self.all_activities[last_activity].fathers:
                self.define_LS_and_LF(father)
        logger.debug('Function define_LS_and_LF has finish')


    def slack_time(self):
        logger.info('Function slack_time has start')
        for activity in self.all_activities:
            self.all_activities[activity].slack_time =\
                self.all_activities[activity].LF - self.all_activities[activity].EF
        logger.info('Function slack_time has finish')

    @property
    def project_duration(self):
        return "The duration of the project: %s" % self.critical_path_time


