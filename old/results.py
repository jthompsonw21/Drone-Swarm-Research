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
    if int(num) < 4:
      redsmall += 1
    else:
      redbig += 1
  elif (winner == "Blue"):
    if int(num) < 4:
      bluesmall += 1
    else:
      bluebig += 1
  else:
    ties += 1

file1.close()
print "Tie"
print ties
print "Blue wins 0-3"
print bluesmall
print "Blue wins 4+"
print bluebig
print "Red wins 0-3"
print redsmall
print "Red wins 4+"
print redbig
