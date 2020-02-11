import java.util.Scanner;

public class java_2920 {    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
        int arr[] = new int[8];
        boolean set = true;

        for(int i=0; i<8; i++){
            arr[i] = scan.nextInt();
        }
            
        if(arr[0] == 1){
            for(int i=0; i<8; i++){
                if(arr[i] != i+1){
                    System.out.println("mixed");
                    set=false;
                    break;
                }
            }
            if(set){
                System.out.println("ascending");
            }
            
        }
        else if(arr[0] == 8){
            for(int i=7; i>-1; i--){
                if(arr[7-i] != i+1){
                    System.out.println("mixed");
                    set=false;
                    break;
                }
            }
            if(set){
                System.out.println("descending");
            }
            
        }
        else{
            System.out.println("mixed");
        }
    }   
}