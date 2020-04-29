from numpy.random import randint
def uniquecolors(n):
    R = 200.0
    G = 0.0
    B = 0.0
    a = 1.0
    dx = 255.0/n
    RGBs = []
    
    for i in range(n):
        R, G, B = randint(low=0.0,high=255.0, size=3)
        A=a
        RGBs.append([R/255.0,G/255.0,B/255.0,A])
    return RGBs
