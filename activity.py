class Activity:
    links = {}
    fathers = {}

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.links = {}
        self.fathers = {}
        self.ES = None
        self.LS = None
        self.EF = None
        self.LF = None
        self.slack_time = None

    '''def connect_activity(self, activity):
        self.links[activity.name] = activity
        activity.fathers[self.name] = self'''


    def print_activity(self):
        print(self.name, " --> ", self.duration, " days")
        print("connect to: ", self.links.keys())
        print("previous:\t", self.fathers.keys(),"\n")
        print("early start: %s" % self.ES,"\tlast start: %s" % self.LF)
        print("early final: %s" % self.ES,"\tlast final: %s" % self.LF)
        print("slack time: %s" % self.slack_time)


