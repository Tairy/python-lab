import os
ups = []
for i in range(0, 255):
  host = "10.0.10." + str(i)
  response = os.system("ping -c 1 " + host)

  if response == 0:
    ups.append(host)
    print host, 'is up!'
  else:
    print host, 'is down!'

print ups