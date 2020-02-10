import java.util.Scanner;

public class java_10951 {    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
        int a,b;

        while(scan.hasNextInt()){
            a = scan.nextInt();
            b= scan.nextInt();
            System.out.println(a+b);
            //scan.nextLine();
        }
        
    }
    
}