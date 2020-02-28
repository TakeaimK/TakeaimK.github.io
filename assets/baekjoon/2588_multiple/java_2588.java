import java.util.Scanner;

public class java_2588 {    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
       
        int num1 = scan.nextInt();
        String num2 = scan.next();

        System.out.println(num1*Character.getNumericValue(num2.charAt(2)));
        System.out.println(num1*Character.getNumericValue(num2.charAt(1)));
        System.out.println(num1*Character.getNumericValue(num2.charAt(0)));
        System.out.println(num1*Integer.parseInt(num2));
       
    }
    
}