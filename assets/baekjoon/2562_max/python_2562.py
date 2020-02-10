if __name__ == "__main__":
    
    maxnum=-1
    where=0

    for i in range(9):
        num = input()
        if(int(num)>int(maxnum)):
            maxnum=num
            where=i+1
    
    print(maxnum)
    print(where)
        

