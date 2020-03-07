import java.util.Scanner;

public class java_14652 { // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        int N = scan.nextInt();
        int M = scan.nextInt();
        int K = scan.nextInt();

        System.out.println(K / M + " " + K % M);
    }

}