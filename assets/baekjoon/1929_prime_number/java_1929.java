import java.util.Scanner;
import java.math.*;

public class java_1929 {    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
        int start = scan.nextInt();
        int end = scan.nextInt();
        boolean set;

        for(int i=start; i<=end; i++){
            set=true;
            for (int j=2; j<=Math.floor(Math.sqrt(i)); j++){
                if(i%j == 0){
                    set=false;
                    break;
                }
            }
            if(set && i>1){
                System.out.println(i);
            }
        }  
    }
}