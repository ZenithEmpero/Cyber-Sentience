import math as m

c1 = (10, 0)
c2 = (0, -10)
dif = (c1[0] - c2[0], c1[1] - c2[1])
angle = m.atan2(dif[1], dif[0])
print(m.degrees(angle))