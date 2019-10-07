import sim

blue_count = 0
red_count = 0
bluewin = False
for runs in range(100):
  print "round " + str(runs)
  try:
    bluewin = sim.main()
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
