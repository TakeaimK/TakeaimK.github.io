import java.util.Scanner;

public class java_2739{    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        int num = scan.nextInt();
        for(int i=1; i<10; i++){
            System.out.println(num+" * "+i+" = "+(num*i));
        }
    }
    
}