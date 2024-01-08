import java.util.*;


/* One node in an adjacency list (one node in the shortest path table): */

class Node {
  public int label;   // this node's label (parent node in path tree)
  public double weight;  // weight of edge to this node (distance to start)

  public Node(int v, double w) { // Constructor:
    label = v;
    weight = w;
  }
}

///////////////////////////////////////////////////////////

public class Dijkstra {
  public static Scanner in;         // for standard input
  public static int n, m;           // n = #vertices, m = #edges
  public static LinkedList[] graph; // adjacency list representation
  public static int start,end;      // start and end points for shortest path
  public double[][] adj_matrix;
  public int[] bestpath;
 public int pathlenght;
  public Dijkstra()
  {

  }
  

  public void solve(double[][] mat,int src, int dst) {
	  
		 //adj_matrix=mat;
                adj_matrix = new double[mat.length][mat.length];
                 for(int i = 0; i< mat.length; i++){
                  for (int j = 0; j < mat.length; j++){
                          adj_matrix[i][j] = mat[i][j];}
                 }
		 n=adj_matrix.length;
		 m=adj_matrix.length;
		 start=src-1;
		 end=dst-1;
		 pathlenght=0;
		    bestpath=new int[n];
		    // Initialize adjacency list structure to empty lists:
		    graph = new LinkedList[n];
		    for (int i = 0; i < n; i++)
		      graph[i] = new LinkedList();

		    // Add each edge twice, once for each endpoint:
		    for (int i = 0; i < n; i++)
		    for (int j = i+1; j < m; j++) {
		    	if(adj_matrix[i][j]!=0){
		      graph[i].add(new Node(j,adj_matrix[i][j]));
		      graph[j].add(new Node(i,adj_matrix[i][j]));}
		    }
	  
	  
    boolean[] done = new boolean[n]; 
    Node[] table = new Node[n];
    for (int i = 0; i < n; i++) 
       table[i] = new Node(-1,Integer.MAX_VALUE); // no parent, infinite dist.

    table[start].weight = 0; // Initially, we only know how to get to "start"

    // Build up shortest paths by adding nearest uncompleted node:
    for (int count = 0; count < n; count++) {
      // find smallest distance among all nodes that aren't yet done:
      double min = Integer.MAX_VALUE;
      int minNode = -1;
      for (int i = 0; i < n; i++)
        if (!done[i] && table[i].weight < min) {
           min = table[i].weight;
           minNode = i;
        }

      done[minNode] = true; // we are now finished with this node

      // Update each neighbor's distance if minNode creates a shorter path:

      // Prepare to loop through the elements of minNode's adjacency list:
      ListIterator iter = graph[minNode].listIterator();
      while(iter.hasNext()) {
         Node nd = (Node)iter.next();
         int v = nd.label;
         double w = nd.weight;

         // See if it is shorter to go from start to minNode weightto v than
         // v's current recorded distance from start:
         if (!done[v] && table[minNode].weight + w < table[v].weight) {
           table[v].weight = table[minNode].weight + w;
           table[v].label = minNode;
         }
      }
    }
    
    int[] temppath=new int[n];
    int i=0;
    if(table[end].weight < Integer.MAX_VALUE)
    {
        int next = table[end].label;
        while (next >= 0) {
            temppath[i]=next;
            next = table[next].label;
            i++;
         }
    }
    	pathlenght=0;
        for (int j = i-1; j >= 0; j--) {
            bestpath[pathlenght]=temppath[j];
            pathlenght++;
        }
        bestpath[pathlenght]=end;
       /* for (int p=0; p<=pathlenght; p++) {
        	System.out.print((bestpath[p]+1)+"000>");
        }*/
  }

  // FOR DEBUGGING ONLY:
  public static void displayGraph() {
    for (int i = 0; i < n; i++) {
      System.out.print(i+": ");
      ListIterator nbrs = graph[i].listIterator(0);
      while (nbrs.hasNext()) {
         Node nd = (Node)nbrs.next();
         System.out.print(nd.label + "("+nd.weight+") ");
      }
      System.out.println();
    }
  }
 /* public static void main(String[] args) {
   // in = new Scanner(System.in);

    
    
    
    int[][]  MainGraph={
		    {0,1,0,0,0,0,1,0,0,0,0,0,0,0,0},
		    {1,0,1,0,0,0,1,0,0,0,0,0,0,0,0},
		    {0,1,0,1,0,0,0,1,0,0,0,0,0,0,0},
		    {0,0,1,0,1,0,0,1,0,0,0,0,0,0,0},
		    {0,0,0,1,0,1,0,0,1,0,0,0,0,0,0},
		    {0,0,0,0,1,0,0,0,1,0,0,0,0,0,0},
		    {1,1,0,0,0,0,0,0,0,1,0,1,0,0,0},
		    {0,0,1,1,0,0,0,0,0,1,1,1,0,1,0},
		    {0,0,0,0,1,1,0,0,0,0,1,0,0,1,0},
		    {0,0,0,0,0,0,1,1,0,0,0,1,1,0,0},
		    {0,0,0,0,0,0,0,1,1,0,0,0,1,1,0},
		    {0,0,0,0,0,0,1,1,0,1,0,0,0,0,1},
		    {0,0,0,0,0,0,0,0,0,1,1,0,0,0,1},
		    {0,0,0,0,0,0,0,1,1,0,1,0,0,0,1},
		    {0,0,0,0,0,0,0,0,0,0,0,1,1,1,0}};
    
    // Input the graph:
   // n = in.nextInt();
   // m = in.nextInt();
 n=MainGraph.length;
 m=MainGraph.length;
    // Initialize adjacency list structure to empty lists:
    graph = new LinkedList[n];
    for (int i = 0; i < n; i++)
      graph[i] = new LinkedList();

    // Add each edge twice, once for each endpoint:
    for (int i = 0; i < n; i++)
    for (int j = i+1; j < m; j++) {
     // int v1 = in.nextInt();
     // int v2 = in.nextInt();
     // int w = in.nextInt();
    	if(MainGraph[i][j]!=0){
      graph[i].add(new Node(j,MainGraph[i][j]));
      graph[j].add(new Node(i,MainGraph[i][j]));}
    }

    // Input starting and ending vertices:
    start = 0;//in.nextInt();
    end =14;// in.nextInt();

    // FOR DEBUGGING ONLY:
   // displayGraph();

    // Print shortest path from start to end:
    solve();
  }

*/

}
