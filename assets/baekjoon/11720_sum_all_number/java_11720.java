import java.util.Scanner;

public class java_11720{    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        int i = scan.nextInt();
        String str = scan.next();

        int temp=0;

        for(int j=0; j<i; j++){
            temp += Character.getNumericValue(str.charAt(j)); 
        }

        System.out.println(temp);
    }
    
}