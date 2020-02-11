if __name__ == "__main__":

    many = input()
    

    for _ in range(int(many)):
        temp=0
        connected=0
        total=0
        string = input()
        for i in range(len(string)):
            if(string[i] == "O"):
                connected+=1
                temp+=connected
            else:
                total+=temp
                connected=0
                temp=0
        
        total+=temp
        print(total)
