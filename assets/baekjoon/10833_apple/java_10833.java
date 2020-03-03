import java.util.Scanner;

public class java_10833 { // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        int num = scan.nextInt();
        int a, b;
        int ans = 0;

        for (int i = 0; i < num; i++) {
            a = scan.nextInt();
            b = scan.nextInt();
            ans += b % a;
            scan.nextLine();
        }

        System.out.println(ans);

    }

}