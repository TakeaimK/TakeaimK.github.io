if __name__ == "__main__":
    
    while True:
        try:
            a, b = map(int, input().split())
            print(a+b)
        except:
            break


def eof():    ##여러가지 풀이법
    # 풀이1 (출처: https://home-body.tistory.com/258)
    while True:
        try:
            a, b = map(int, input().split())
            print(a+b)
        except:
            break
        
        
        
    # 풀이2 (출처 : https://hwiyong.tistory.com/m/208?category=844316 )
    import sys
    
    for line in sys.stdin:
        a, b = map(int, line.split())
        print(a + b)
    
    
    
    
    # 풀이3 (출처 : https://sinb57.tistory.com/entry/Python-3-10951-A-B-4 )
    try:
        while 1:
            a,b = map(int, input().split())
            print(a+b)
    except:
        exit()
    