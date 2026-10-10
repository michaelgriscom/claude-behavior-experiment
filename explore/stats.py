import math
def fisher(a,n1,b,n2):
    """two-sided Fisher exact for a/n1 vs b/n2"""
    from math import comb
    K=a+b; N=n1+n2
    def p(x): return comb(n1,x)*comb(n2,K-x)/comb(N,K)
    p0=p(a); lo=max(0,K-n2); hi=min(K,n1)
    return min(1,sum(p(x) for x in range(lo,hi+1) if p(x)<=p0*(1+1e-9)))
def mcnemar(b,c):
    """exact two-sided McNemar on discordant counts"""
    n=b+c; k=min(b,c)
    return min(1,2*sum(math.comb(n,i) for i in range(k+1))/2**n) if n else 1.0
