def myfunction1(n):
    if(n>0):
        return
    
    print("Coding")
    myfunction1(n/2)
    myfunction1(n/3)
#recurrence relation
#T(n)=T(n/2)+T(n/3)+O(1)