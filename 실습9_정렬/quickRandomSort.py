def quickRandomSort(A,p:int,r:int):
    import random
    if p<r:
        q= random.randint(p, r)
        quickRandomSort(A,p,q-1)
        quickRandomSort(A,q+1,r)
def partition(A,p:int,r:int)->int:
    x=A[r]
    i=p-1
    stack=0
    for j in range(p,r):
        if A[j] < x:
            i+=1
            A[i],A[j]=A[j],A[i]

    A[i+1],A[r]=A[r],A[i+1]
    return i+1