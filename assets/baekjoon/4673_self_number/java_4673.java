

public class java_4673{    // 채점 시 Class 명을 'Main'으로 변경

    private static int non_self_number(int num) {
        int total = num;
        if (num >= 10000) {
            total += num / 10000;
            num %= 10000;
        }
        if (num >= 1000) {
            total += num / 1000;
            num %= 1000;
        }
        if (num >= 100) {
            total += num / 100;
            num %= 100;
        }
        if (num >= 10) {
            total += num / 10;
            num %= 10;
        }
        total += num;
        return total;
    }

    public static void main(String[] args) {

        int arr[] = new int[100000];

        for (int i = 1; i < 10001; i++) {
            arr[non_self_number(i)] = 1;
            if(arr[i]==0){
                System.out.println(i);
            }
        }
    }
    
}