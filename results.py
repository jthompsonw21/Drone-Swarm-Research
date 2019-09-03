import sys
filename = sys.argv[-1]
file1 = open(filename, 'r') 

bluesmall = 0
bluebig = 0
redsmall = 0
redbig = 0
winner = ""
ties = 0
for line in file1:
  winner, num = line.split()
  if (winner == "Red"):
    if int(num) < 3:
      redsmall += 1
    else:
      redbig += 1
  elif (winner == "Blue"):
    if int(num) < 3:
      bluesmall += 1
    else:
      bluebig += 1
  else:
    ties += 1

file1.close()
print "Tie"
print ties
print "Blue wins 3+"
print bluebig
print "Blue wins 0-2"
print bluesmall
print "Red wins 0-2"
print redsmall
print "Red wins 3+"
print redbig
