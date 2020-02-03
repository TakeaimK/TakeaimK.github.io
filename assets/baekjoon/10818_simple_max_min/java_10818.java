import java.util.Scanner;

public class java_10818{    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        int num = scan.nextInt();
        scan.nextLine();
        int max = -1000001;
        int min = 1000001;
        int temp;

        for(int i=0; i<num; i++){
            temp = scan.nextInt();
            if(temp>max){
                max = temp;
            }
            if(temp<min){
                min = temp;
            }
        }
        System.out.println(min + " " + max);

    }
    
}