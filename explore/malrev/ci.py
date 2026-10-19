import sys, math
def wilson(k,n,z=1.96):
    if n==0: return (0,0,0)
    p=k/n; d=1+z*z/n
    c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return (round(100*p,1), round(100*(c-h),1), round(100*(c+h),1))
# args: label k n  (repeatable in triples)
a=sys.argv[1:]
for i in range(0,len(a),3):
    lab,k,n=a[i],int(a[i+1]),int(a[i+2]); p,lo,hi=wilson(k,n)
    print(f"{lab:28s} {k}/{n}  {p:5.1f}%  95% CI [{lo:.1f}, {hi:.1f}]")
