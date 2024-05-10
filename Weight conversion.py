u=int(input("Entr your weight "))
z=input("k(g) or (l)bs")
if z=='k' or z=='K':
    w=u*2.205
    print ("weight in lbs=",w)
else:
    w=u/2.205
    print("weight in kg=",w)
