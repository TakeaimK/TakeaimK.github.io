package main

import (
	"fmt"
	"sort"
)

type ByLength []string

func (s ByLength) Len() int {
	return len(s)
}
func (s ByLength) Swap(i, j int) {
	s[i], s[j] = s[j], s[i]
}
func (s ByLength) Less(i, j int) bool {
	return len(s[i]) < len(s[j])
}

func main() {

	var rng int
	fmt.Scan(&rng)

	arr := make([]string, rng)

	gg := true
	var tmps string
	for i := 0; i < rng; i++ {
		gg = true
		fmt.Scan(&tmps)
		for _, s := range arr {
			if tmps == s {
				gg = false
				break
			}
		}
		if gg {
			arr[i] = tmps
		}

	}
	//fmt.Println(arr)

	sort.Sort(ByLength(arr))

	for _, s := range arr {
		fmt.Printf("%s\n", s)
	}
}
