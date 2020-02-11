if __name__ == "__main__":
    
    set=0
    dingdong = list(map(int, input().split()))
    if(dingdong[0]==1):
        for i in range(0, 8):
            if(dingdong[i]!=i+1):
                print("mixed")
                set=1
                break
        if(set==0):
            print("ascending")

    elif(dingdong[0]==8):
        for i in range(7, -1, -1):
            if(dingdong[7-i]!=i+1):
                print("mixed")
                set=1
                break
        if(set==0):
            print("descending")
    else:
        print("mixed")
        