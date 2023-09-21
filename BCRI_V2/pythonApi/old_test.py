# Test Script

import teamDataImport

data = teamDataImport.infoRequest(2019)
calc = teamDataImport.calcStats()

floridaAdv = data.getAdvStats("Florida")
clemsonAdv = data.getAdvStats("Clemson")
ohiostateAdv = data.getAdvStats("Ohio State")
bamaAdv = data.getAdvStats("Alabama")
riceAdv = data.getAdvStats("Rice")
massAdv = data.getAdvStats("UMass")

floridaAdvOff = data.getAdvOff(floridaAdv)
clemsonAdvOff = data.getAdvOff(clemsonAdv)
ohiostateAdvOff = data.getAdvOff(ohiostateAdv)
bamaAdvOff = data.getAdvOff(bamaAdv)
riceAdvOff = data.getAdvOff(riceAdv)
massAdvOff = data.getAdvOff(massAdv)

floridaDrives = data.getDriveStats("Florida")
clemsonDrives = data.getDriveStats("Clemson")
ohiostateDrives = data.getDriveStats("Ohio State")
bamaDrives = data.getDriveStats("Alabama")
riceDrives = data.getDriveStats("Rice")
massDrives = data.getDriveStats("UMass")

floridaOffRating = calc.calcOffRating(floridaAdvOff, floridaDrives, "Florida")
clemsonOffRating = calc.calcOffRating(clemsonAdvOff, clemsonDrives, "Clemson")
ohiostateOffRating = calc.calcOffRating(ohiostateAdvOff, ohiostateDrives, "Ohio State")
bamaOffRating = calc.calcOffRating(bamaAdvOff, bamaDrives, "Alabama")
riceOffRating = calc.calcOffRating(riceAdvOff, riceDrives, "Rice")
massOffRating = calc.calcOffRating(massAdvOff, massDrives, "UMass")

floridaAdvDef = data.getAdvDef(floridaAdv)
clemsonAdvDef = data.getAdvDef(clemsonAdv)
ohiostateAdvDef = data.getAdvDef(ohiostateAdv)
bamaAdvDef = data.getAdvDef(bamaAdv)
riceAdvDef = data.getAdvDef(riceAdv)
massAdvDef = data.getAdvDef(massAdv)

floridaDefRating = calc.calcDefRating(floridaAdvDef, floridaDrives, "Florida")
clemsonDefRating = calc.calcDefRating(clemsonAdvDef, clemsonDrives, "Clemson")
ohiostateDefRating = calc.calcDefRating(ohiostateAdvDef, ohiostateDrives, "Ohio State")
bamaDefRating = calc.calcDefRating(bamaAdvDef, bamaDrives, "Alabama")
riceDefRating = calc.calcDefRating(riceAdvDef, riceDrives, "Rice")
massDefRating = calc.calcDefRating(massAdvDef, massDrives, "UMass")


print("\nOffense")
print("Florida Offense: ", floridaOffRating)
print("Clemson Offense: ", clemsonOffRating)
print("Ohio State Offense: ", ohiostateOffRating)
print("Alabama Offense: ", bamaOffRating)
print("Rice Offense: ", riceOffRating)
print("UMass Offense: ", massOffRating)
print("\nDefense")
print("Florida Defense: ", floridaDefRating)
print("Clemson Defense: ", clemsonDefRating)
print("Ohio State Defense: ", ohiostateDefRating)
print("Alabama Defense: ", bamaDefRating)
print("Rice Defense: ", riceDefRating)
print("UMass Defense: ", massDefRating)
# print("\nOverall")
# print("Florida Overall: ", calc.calcTeamRating(floridaOffRating, floridaDefRating))
# print("Clemson Overall: ", calc.calcTeamRating(clemsonOffRating, clemsonDefRating))
# print("Ohio State Overall: ", calc.calcTeamRating(ohiostateOffRating, ohiostateDefRating))
# print("Alabama Overall: ", calc.calcTeamRating(bamaOffRating, bamaDefRating))
# print("Rice Overall: ", calc.calcTeamRating(riceOffRating, riceDefRating))
# print("UMass Overall: ", calc.calcTeamRating(massOffRating, massDefRating))








