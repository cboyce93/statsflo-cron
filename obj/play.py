import datetime

import pdb

class Play:

    def __init__(self, kwargs):
        # convert dict to object vars
        for key, val in kwargs.items():
            exec('self.' + key + '=val')

        min = int(self.about['periodTime'][:2])
        sec = int(self.about['periodTime'][3:])
        self.event_time = datetime.time(0, min, sec)
        self.players_on_ice = []

    def setPlayersOnIce(self, shifts):
        """
        find all playerIDs on ice @ time of Play
        """
        for shift in shifts:

            # is play in same period?
            if shift['period'] == self.about['period']:

                # create datetime object of shift start and end times
                # so we can compare easily to tell if player is on ice
                min = int(shift['startTime'][:2])
                sec = int(shift['startTime'][3:])
                shift_begin = datetime.time(0, min, sec)

                min = int(shift['endTime'][:2])
                sec = int(shift['endTime'][3:])
                shift_end = datetime.time(0, min, sec)

                # give count to player that was on ice leading to event
                # not player that just came on
                if self.event_time > shift_begin and self.event_time <= shift_end:
                    # player was on ice @ Play event time
                    self.players_on_ice.append((shift['playerId']))





