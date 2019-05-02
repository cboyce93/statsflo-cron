class Player:

    def __init__(self, kwargs):
        # convert dict to object vars
        for key, val in kwargs.items():
            exec('self.'+key + '=val')

        self.team_id = self.currentTeam['id']

        # Corsi - Any shot attempt (goals, shots on net, misses and blocks) outside of the shootout.
        self.all_CF = 0
        self.all_CA = 0
        self.all_CFP = 0

        # Fenwick - any unblocked shot attempt (goals, shots on net and misses) outside of the shootout.
        self.all_FF = 0
        self.all_FA = 0
        self.all_FFP = 0

        # Shots - any shot attempt on net (goals and shots on net) outside of the shootout.
        self.all_SF = 0
        self.all_SA = 0
        self.all_SFP = 0

        # Goals - any goal, outside of the shootout.
        self.all_GF = 0
        self.all_GA = 0
        self.all_GFP = 0

    def update_corsi(self, play):
        """
        Update the Corsi stats for Player

        :param play: Shot attempt Play obj
        """
        for_team = play.team['id']

        # determine if CF or CA
        if self.team_id == for_team:
            self.all_CF += 1
        else:
            self.all_CA += 1
        self.all_CFP = self.all_CF * 100 / float(self.all_CF + self.all_CA)

    def update_fenwick(self, play):
        """
        Update the Fenwick stats for Player

        :param play: Unblocked shot attempt Play obj
        """
        for_team = play.team['id']

        # determine if FF or FA
        if self.team_id == for_team:
            self.all_FF += 1
        else:
            self.all_FA += 1
        self.all_FFP = self.all_FF * 100 / float(self.all_FF + self.all_FA)

    def update_shots(self, play):
        """
        Update the Shots stats for Player

        :param play: Shot attempt Play obj
        """
        for_team = play.team['id']

        # determine if SF or SA
        if self.team_id == for_team:
            self.all_SF += 1
        else:
            self.all_SA += 1
        self.all_SFP = self.all_SF * 100 / float(self.all_SF + self.all_SA)

    def update_goals(self, play):
        """
        Update the Goals stats for Player

        :param play: Shot attempt Play obj
        """
        for_team = play.team['id']

        # determine if GF or GA
        if self.team_id == for_team:
            self.all_GF += 1
        else:
            self.all_GA += 1
        self.all_GFP = self.all_GF * 100 / float(self.all_GF + self.all_GA)

    def __str__(self):
        return self.fullName
