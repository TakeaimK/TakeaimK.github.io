import java.util.Scanner;

public class java_2562 {    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
        int max=1;
        int where=0;
        int num;

        for(int i=1; i<10; i++){
            num = scan.nextInt();
            //scan.nextLine();
            if(num>max){
                max=num;
                where=i;
            } 
        }
        System.out.println(max);
        System.out.println(where);
        
    }
    
}