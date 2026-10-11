import math
def mw(a,b):
    U=sum((x>y)+0.5*(x==y) for x in a for y in b); n1,n2=len(a),len(b)
    mu=n1*n2/2; sd=(n1*n2*(n1+n2+1)/12)**.5; z=(U-mu)/sd
    return round(z,2), math.erfc(abs(z)/2**.5)
