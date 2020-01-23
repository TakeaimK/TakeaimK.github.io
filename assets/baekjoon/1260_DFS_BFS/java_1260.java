import java.util.*;

public class java_1260 {    // 채점 시 Class 명을 'Main'으로 변경
    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
        int N = scan.nextInt();     //node num
        int M = scan.nextInt();     //edge num
        int V = scan.nextInt();     //start node
        scan.nextLine();
        
        int[][] matrix = new int[N+1][N+1];
        for(int i=0; i<M; i++){
            int a = scan.nextInt();
            int b = scan.nextInt();
            scan.nextLine();
            matrix[a][b]=1;
            matrix[b][a]=1;
        }
        boolean[] visited = new boolean[N+1];
        Arrays.fill(visited, false);
        Sub cls = new Sub();
        cls.dfs(matrix, visited, V, N);
        Arrays.fill(visited, false);
        System.out.println();
        cls.bfs(matrix, visited, V, N);

    }
    
}

class Sub{
    void dfs(int[][] matrix, boolean[] visited, int now, int N){
        visited[now] = true;
        System.out.print(now + " ");
        for(int i=1; i<=N; i++){
            if(matrix[now][i]!=0 && !visited[i]){
                dfs(matrix, visited, i, N);
            }
        }
    }


    void bfs(int[][] matrix, boolean[] visited, int now, int N){
            
        Queue<Integer> queue = new LinkedList<>();
        queue.add(now); 
        visited[now] = true; //방문한 위치는 알아야하니까, 그것을 체크하기 위해서 visit가 필요. 
        while(!queue.isEmpty()){ 
            int temp = queue.remove(); //첫번째 방문한 위치는 빼주기로 한다. 
            System.out.print(temp+" ");
            for(int k =1; k<=N; k++){ 
                if(matrix[temp][k]==1 && visited[k]==false){ 
                    queue.offer(k);
                    visited[k] = true; //true라면 방문 
                } 
            } 
        }

    }
}