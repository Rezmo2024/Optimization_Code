import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

/**
 *
 * @author REZMO
 */
public class Algorithms_Evaluator {

    /**
     * @param args the command line arguments
         */
    public double[][] MainGraph;    
    public static void main(String[] args) throws IOException {
   /*FuzzyEvaluator gg=new FuzzyEvaluator();
   gg.solve();;*/
           // TODO code application logic here
    	double[][]  MainGraph={
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
	  
    	double[][]  MainGraph2={
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0},
    			{0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0},
    			{0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0,0,1},
    			{0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0},
    			{0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0},
    			{0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0},
    			{0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0},
    			{0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
    			{0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0},
    			{0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
    			{0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0},
    			{0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0},
    			{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0},
    			{0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0},
    			{1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0},
    			{0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0},
    			{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0},
    			{0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0},
    			{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0},
    			{0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0},
    			{0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}};

    	  int[][]  SharedLinkGraph={
    			    {11,14},
    			    {12,14}}; // these two edge are shared risk links and (13,14) are seperate link
      
      
     /* double[][]  MainGraph2={
    		  {100000,6,5,100000,100000,100000,100000},
    		  {100000,100000,2,3,7,100000,100000},
    		  {100000,100000,100000,9,4,100000,100000},
    		  {100000,100000,100000,100000,5,2,3},
    		  {100000,100000,100000,100000,100000,8,1},
    		  {100000,100000,100000,100000,100000,100000,100000},
    		  {100000,100000,100000,100000,100000,100000,100000},
    };*/

      long startTime = System.nanoTime();
      long endTime=System.nanoTime();
    	 // for(int w=0;w<500;w++){
    	  
    		  
      Algorithms_Evaluator TO=new Algorithms_Evaluator();
      double[][] TempGraph2=TO.Graph_Weights(MainGraph);
      Random_Matrix ranmat=new Random_Matrix();
      int mat_size=30;
      int delay_thresh=200;
      
      BufferedWriter output = null;
      File file = new File("Execution_time.txt");
     try {
            output = new BufferedWriter(new FileWriter(file,true));
            long tot_time;
            output.append("ABC"+"\t"+"ANT"+"\t"+"CSP"+"\t"+"LARAC"+"\t"+"SRLG"+"\t"+"SAMCRA"+"\n");
          } catch ( IOException e ) {
                             e.printStackTrace();
                  } 
output.close();
     for(int w=2; w<50; w++)
     {
         mat_size=w*10;
         output = new BufferedWriter(new FileWriter(file,true));
         double[][] TempGraph1=TO.Graph_Weights(ranmat.Create_Matrix(mat_size, 0, 2));
      Random r=new Random();
      int src=r.nextInt(mat_size-1) + 1, dst=r.nextInt(mat_size-1) + 1;
      Dijkstra di=new Dijkstra();
        di.solve(TempGraph1,src,dst);
        int[] h=new int[di.pathlenght];
        h=di.bestpath;
        if(h.length<=1)continue;   // if the matrix has not soultion then return else run the below algorithms
        
                        // double[][] TempGraph=MainGraph;
                        //TO.Show_Graph(TempGraph1);
                        startTime = System.nanoTime();
                        Ant a=new Ant(TempGraph1,100,5,TempGraph1,delay_thresh);
                         a.start(src,dst);
                         long duration_ant =-1;
                         if(a.findpath)
                                 {

                         int[] q=new int[a.l_index+1];
                         q=a.Ant_Best_Path();
                          endTime = System.nanoTime();
                           duration_ant =(endTime - startTime);
                         for(int i=0; i<=a.l_index; i++)
                                 System.out.print((q[i]+1)+"**>");

                                 }
                         else {
                                 System.out.print("there is no feasible solution aco");
                         System.out.println();
                         duration_ant =-1;}



                         startTime = System.nanoTime();
                         long duration_abc=-1;
                       /* ABC b=new ABC(TempGraph1,20,10,TempGraph1,delay_thresh);
                       b.start(src,dst); 
                        if(b.Find_Path)
                            {

                        int[] p=new int[b.Best_Path_Len];
                        p=b.Best_Path;
                        endTime = System.nanoTime();
                         duration_abc= (endTime - startTime);
                        for(int i=0; i<b.Best_Path_Len; i++)
                         System.out.print((p[i]+1)+"->");

                            }
                        else {
                            System.out.print("there is no feasible solution abc");
                        System.out.println();
                        duration_abc=-1;}*/





                        startTime = System.nanoTime();
                        LARAC  la=new LARAC(TempGraph1, TempGraph1, delay_thresh,1000);
                        boolean res=false;
                       res=la.solve(src,dst);
                        long duration_larac =-1;
                        if(res)
                        {
                            int[] m=new int[la.bestpath_len];
                            m=la.bestpath;
                            endTime = System.nanoTime();
                             duration_larac =(endTime - startTime);
                            for(int i=0; i<=la.bestpath_len; i++)
                                 System.out.print((m[i]+1)+"=>"); 


                        }
                        else{
                            System.out.print("there is no feasible solution larac");
                            duration_larac =-1;}




                         startTime = System.nanoTime();
                         CSP csp=new CSP(TempGraph1, TempGraph1, delay_thresh,src,dst);
                         csp.Solve();
                         long duration_csp =-1;
                         if(csp.findpath){
                             endTime = System.nanoTime();
                           duration_csp =(endTime - startTime);
                         }
                         else{
                            System.out.print("there is no feasible solution csp");
                            duration_csp =-1;}

                         startTime = System.nanoTime();
                         SRLG srlg=new SRLG(TempGraph1,SharedLinkGraph,src,dst,2,1);
                         srlg.Solve();
                         long duration_SRLG =-1;
                         int[] fp=new int[srlg.first_path_len];
                         int[] sp=new int[srlg.second_path_len];
                         fp=srlg.first_path;
                         sp=srlg.second_path;
                         if(fp.length>=2 && sp.length>=2)
                         {
                             endTime = System.nanoTime();
                             duration_SRLG = (endTime - startTime);
                         for(int i=0; i<=srlg.first_path_len; i++)
                                 System.out.print((fp[i]+1)+"->");
                         System.out.println();
                         for(int i=0; i<=srlg.second_path_len; i++)
                                 System.out.print((sp[i]+1)+"->");
                         System.out.println();
                         }
                         else{ duration_SRLG = -1;
                         System.out.println();}





                         startTime = System.nanoTime();
                         double[] cons={1,delay_thresh};//constraint
                        SAMCRA sam=new SAMCRA(TempGraph1,TempGraph1,cons,2,1000);
                        sam.solve(src,dst);
                        long duration_sam =-1;
                        if(sam.findpath)
                        {
                            int[] m=new int[sam.BestPathLenght];
                            m=sam.BestPath;
                               endTime = System.nanoTime();
                               duration_sam =(endTime - startTime);
                            for(int i=0; i<sam.BestPathLenght; i++)
                                 System.out.print((m[i]+1)+"->"); 
                       }
                        else{
                            System.out.print("there is no feasible solution for SAMCRA");
                        duration_sam =-1;}

                        output.append(duration_abc+"\t"+duration_ant+"\t"+duration_csp+"\t"+duration_larac+"\t"+duration_SRLG+"\t"+duration_sam+"\n");
                         
                         System.out.println();     
                         System.out.println("Duration For ABC=  "+duration_abc/1000000);
                         System.out.println("Duration For ANT=  "+duration_ant/1000000);
                        System.out.println("Duration For Classic=  "+duration_csp/1000000);
                        //System.out.println("Duration For Classic(DCLC)=  "+duration_dclc/1000000);
                         System.out.println("Duration For Classic(SRLG)=  "+duration_SRLG/1000000);
                         System.out.println("Duration For LARAC=  "+duration_larac/1000000);
                        System.out.println("Duration For SAMCRA=  "+duration_sam/1000000);
                        System.out.println("iteration="+w);

/*
                         double[][] cost_matrix=TO.Graph_FuzzyWeights(TempGraph1, TempGraph1);
                         Dijkstra d1=new Dijkstra();
                         d1.solve(cost_matrix,src,dst);
                         int[] q1=new int[d1.pathlenght];
                         q1=d1.bestpath;
                         for(int i=0; i<=d1.pathlenght; i++)
                                 System.out.print((q1[i]+1)+"->"); 

                         System.out.println();
                         Dijkstra d2=new Dijkstra();
                         d2.solve(cost_matrix,src,dst);
                         int[] q2=new int[d2.pathlenght];
                         q2=d2.bestpath;
                         for(int i=0; i<=d2.pathlenght; i++)
                                 System.out.print((q2[i]+1)+"->"); */
                       //
                       //TO.Show_Graph(cost_matrix);
                        output.close();
    }
    
    }
    public void Show_Graph(double[][] m)
    {
        for(int i=0; i<m.length; i++)
        {
            for(int j=0;j<m.length;j++)
               System.out.print(m[i][j]+"  ");
         System.out.println();
        }
    }
    double [][] Graph_Weights(double[][] m)
    {
        double[][] Node_Matrix = new double[m.length][];
        for(int i = 0; i< m.length; i++){
         Node_Matrix [i] = new double[m[i].length];
         Random r=new Random();
         for (int j = 0; j < m[i].length; j++)
         {
              double s= r.nextDouble()*100;
              if(m[i][j]!=0)
                          Node_Matrix[i][j] =s ;
//System.out.print(Node_Matrix[i][j]+"       ");
         }
    }
        return Node_Matrix;
    }
    
    double [][] Graph_FuzzyWeights(double[][] m,double[][] n, int q)
    {
        double[][] Node_Matrix = new double[m.length][];
        if(q==2){
        FuzzyT2 f=new FuzzyT2(50,2000,5,100);
        for(int i = 0; i< m.length; i++){
         Node_Matrix [i] = new double[m[i].length];
         for (int j = 0; j < m[i].length; j++)
         {
              if(m[i][j]!=0)
                          Node_Matrix[i][j] =f.Get_Cost((int)m[i][j], (int)n[i][j]) ;
         }
        }
        }
        else
        {
         FuzzyT1 f=new FuzzyT1(50, 2000);
        for(int i = 0; i< m.length; i++){
         Node_Matrix [i] = new double[m[i].length];
         for (int j = 0; j < m[i].length; j++)
         {
              if(m[i][j]!=0)
                          Node_Matrix[i][j] =f.Get_Cost(m[i][j], n[i][j]) ;
         }
                }
    }
        return Node_Matrix;
    }
}
    
