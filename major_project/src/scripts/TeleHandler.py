import common


class TeleHandler():

    def handle(self, data):
        if common.priorityLevel > 1:
            common.priorityLevel = 1
        common.rate.sleep()
        if common.priorityLevel == 1:
            common.priorityLevel = 5
