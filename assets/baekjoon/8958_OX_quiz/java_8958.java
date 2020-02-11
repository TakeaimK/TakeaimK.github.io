import java.util.Scanner;

public class java_8958 {    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
        int many = 0;
        int total = 0;
        int temp= 0 ;
        int connected = 0;
        String str = "";

        many = scan.nextInt();

        for(int i=0; i<many; i++){
            str = scan.next();
            scan.nextLine();

            total=0;
            temp=0;
            connected=0;

            for(int j=0; j<str.length();j++){
                if(str.charAt(j) == 'O'){
                    connected++;
                    temp+=connected;
                }
                else{
                    total+=temp;
                    connected=temp=0;
                }
            }
            total+=temp;
            System.out.println(total);
            
            
            //scan.nextLine();
            
        }   
    }
}