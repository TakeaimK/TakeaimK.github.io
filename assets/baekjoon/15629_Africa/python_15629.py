def trip():

    cost = 0
    goSA = False
    goZam = False
    goZim = False
    num = int(input())

    for _ in range(num):
        country = input()

        if country == "botswana" :
            cost = cost+0
        if country == "ethiopia" :
            cost = cost+50
        if country == "kenya" :
            cost = cost+50
        if country == "tanzania" :
            cost = cost+50
        if country == "south-africa" :
            goSA = True
            cost = cost+0
        if country == "namibia" :
            if(goSA):
                cost+=40
            else:
                cost = cost+140
        if country == "zambia" :
            goZam = True
            if(goZim):
                cost = cost+20
            else:
                cost = cost+50
        if country == "zimbabwe" :
            goZim = True
            if(goZam):
                cost = cost+0
            else:
                cost = cost+30
        
        if country != "zambia" and country != "zimbabwe":
            goZam = False
            goZim = False
    return cost
        


if __name__ == "__main__":

    answer = 0

    answer = trip()

    print(answer)
    
