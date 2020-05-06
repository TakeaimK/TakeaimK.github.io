package main

import(
    "fmt"
)

func main(){
    
    var arr [4]int

    for i:=0; i<4; i++{
        fmt.Scan(&arr[i])
    }
    

    arr[2] = arr[2]-arr[0]
    arr[3] = arr[3]-arr[1]

    ans := arr[0]

    for i:=1; i<4; i++{
        if arr[i]<ans{
            ans = arr[i]
        }
    }
    fmt.Println(ans)
}