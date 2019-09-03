from sim import main

blue_count = 0
red_count = 0
bluewin = False
for runs in range(100): 
  try:
    bluewin = main()
  except SystemExit:
    print "round over"
  if bluewin:
    blue_count += 1
  else:
    red_count += 1

print "Red = "
print red_count
print "Blue = "
print blue_count
