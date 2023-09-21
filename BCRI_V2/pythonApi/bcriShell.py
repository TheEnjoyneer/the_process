# bcriShell.py
# Christopher Brant
# Fall of 2019
# BCRI Interactive Shell V1

import teamDataImport, datetime, os
from cmd import Cmd

default_userTeam = "Florida"
startup_string = '\nWelcome to the Brant Composite Ratings Index interactive shell.\n'
startup_string += 'Try using the command "lc" to list all possible commands.\n'
startup_string += 'For an individual command, try using "help <command>"\n'
startup_string += 'Try "help" without an argument for more info.\n'
now = datetime.datetime.now()

class MyPrompt(Cmd):
	prompt = '$ '

	def do_init(self, inp):
		print(startup_string)
		self.currentYear = now.year
		self.userTeam = default_userTeam
		self.prompt = 'BCRI-' + str(self.currentYear) + '-' + self.userTeam + '$ '
		self.dataInterface = teamDataImport.infoRequest(self.currentYear)
		self.calcInterface = teamDataImport.calcStats()
		self.teamInfo = self.dataInterface.teamInfo()
		self.teamNames = self.dataInterface.teamNames(self.teamInfo)
		self.conferences = self.dataInterface.conferences()


	# sy will set the year to get stats from and set the prompt
	def do_syear(self, inp):
		args = inp.split()
		if len(args) != 1:
			print("Invalid command syntax. Try again.")
		# Set new year and get new interface and team names for that year
		self.currentYear = int(args[0])
		self.prompt = 'BCRI-' + str(self.currentYear) + '-' + self.userTeam + '$ '
		self.dataInterface = teamDataImport.infoRequest(self.currentYear)
		self.teamInfo = self.dataInterface.teamInfo()
		self.teamNames = self.dataInterface.teamNames(self.teamInfo)
		self.conferences = self.dataInterface.conferences()


	# st will set the user team that will highlight in ratings and be seen in the prompt
	def do_steam(self, inp):
		args = inp.split()
		if len(args) != 1:
			print("Invalid command syntax. Try again.")
		elif args[0] not in self.teamNames:
			print("Given team name not found in database.")
		# Set new team and prompt
		self.userTeam = args[0]
		self.prompt = 'BCRI-' + str(self.currentYear) + '-' + self.userTeam + '$ '


	# print team names
	def do_pteams(self, inp):
		argsLen = inp.split()
		args = inp
		if len(argsLen) == 0:
			print("")
			print(*self.teamNames, sep="\n")
			print("")
		elif len(argsLen) >= 1:
			if args in self.conferences:
				confSchools = self.dataInterface.confTeams(self.teamInfo, args)
				print("\n" + args + " Teams")
				print("-------------")
				print(*confSchools, sep="\n")
				print("")
			else:
				print("Conference List:")
				print(*self.conferences, sep=", ")
				command = raw_input("Enter a conference from the list: ")
				if command not in self.conferences:
					print("Invalid response. Ending command.")
					return
				else:
					confSchools = self.dataInterface.confTeams(self.teamInfo, command)
					print("\n" + command + " Teams")
					print("-------------")
					print(*confSchools, sep="\n")
					print("")
		else:
			print("Invalid command syntax. Try again.")


	# print conference names
	def do_pconf(self, inp):
		print("\nAll Conferences, both current and historical")
		print("-------------")
		print(*self.conferences, sep="\n")
		print("")


	# show betting trends
	def do_btrends(self, inp):
		args = inp.split()
		if len(args) < 2:
			print("Invalid command syntax. Try again.")
		else:
			if args[0] not in self.teamNames:
				print("Given team name not found in database.")
				return
			elif args[1] != "home" and args[1] != "away" and args[1] != "overall":
				print("Incorrect second argument. Try again.")
				return

			if args[1] == "home":
				trends = self.dataInterface.getTeamBetData(args[0])
				trends = self.calcInterface.calcHomeBetTrends(trends, args[0])
			elif args[1] == "away":
				trends = self.dataInterface.getTeamBetData(args[0])
				trends = self.calcInterface.calcAwayBetTrends(trends, args[0])
			elif args[1] == "overall":
				data = self.dataInterface.getTeamBetData(args[0])
				home = self.calcInterface.calcHomeBetTrends(data, args[0])
				away = self.calcInterface.calcAwayBetTrends(data, args[0])
				trends = self.calcInterface.calcBetTrends(home, away)

			try:
				print("\nAgainst the Spread")
				print("------------------")
				print(str(trends["SpreadWins"]) + "-" + str(trends["SpreadLosses"]) + "-" + str(trends["SpreadTies"]))
				print("")
				print("Over/Under Total")
				print("----------------")
				print("Overs: " + str(trends["TotalOvers"]))
				print("Unders: " + str(trends["TotalUnders"]))
				print("Ties: " + str(trends["TotalTies"]))
				print("")
			except NameError:
				print("Problem. Oof")


	# show full betting stats
	def do_bstats(self, inp):
		return


	# show betting trends for a matchup
	def do_mtrends(self, inp):
		return


	# show full betting stats for a matchup
	def do_mstats(self, inp):
		return


	# clear screen
	def do_clear(self, inp):
		os.system('clear')


	# emptyline
	def emptyline(self):
		pass


    # exits the shell
	def do_exit(self, inp):
		print("\nThank you for using the BCRI interactive shell.")
		print("                            - The Enjoyneer\n")
		return True


# Helper functions here
def teamHomeBetStats(teamName):
	return

def teamAwayBetStats(teamName):
	return

def teamBetStats(teamName):
	return

def matchupTrends(team1, team2):
	return

def matchupBetStats(team1, team2):
	return




# Main function for the shell
if __name__ == '__main__':
	# Run the main command prompt loop
	shell = MyPrompt()
	shell.do_init("")
	shell.cmdloop()






