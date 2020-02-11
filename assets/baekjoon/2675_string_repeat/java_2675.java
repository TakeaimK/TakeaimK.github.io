import java.util.Scanner;

public class java_2675 {    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
        int many = 0;
        int repeat = 0;
        String str = "";
        String newstr = "";

        many = scan.nextInt();

        for(int i=0; i<many; i++){
            repeat = scan.nextInt();
            str = scan.next();
            scan.nextLine();

            for(int j=0; j<str.length();j++){
                for(int k=0; k<repeat; k++){
                    newstr+=str.charAt(j);
                }
            }
            System.out.println(newstr);
            newstr = "";
            //scan.nextLine();
            
        }   
    }
}