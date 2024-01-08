
import java.util.Random;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author REZMO
 */
public class FuzzyEvaluator {
      public  void solve()
    {
       Random_Matrix ranmat=new Random_Matrix();
       int src=1,dst=90;
       double[][] mat=ranmat.Create_Matrix(90,0, 80);
       double[][] main_mat=new double[90][90];
       for(int i=0; i<90; i++)
       for(int j=i+1; j<90; j++)
           if(mat[i][j]!=0){
               	Random r=new Random();

               int result = r.nextInt(8000-1) + 1;
				main_mat[i][j]=(double)result;
				main_mat[j][i]=(double)result;
           }
       for(int i=0; i<90; i++){
       for(int j=0; j<90; j++){
            main_mat[i][j]=/*mat[i][j]/80*/+(main_mat[i][j])/2000;
            System.out.print(main_mat[i][j]+" ");
       }
       System.out.println();
       }
       double[] cons={1,200};//constraint
                Algorithms_Evaluator f=new Algorithms_Evaluator();
/*
                         CSP csp=new CSP(main_mat,mat, 200,src,dst);
                         csp.Solve();
                         CSP csp1=new CSP(f.Graph_FuzzyWeights(main_mat,mat,1),mat, 200,src,dst);
                         csp1.Solve();
                         CSP csp2=new CSP(f.Graph_FuzzyWeights(main_mat,mat,2),mat, 200,src,dst);
                         csp2.Solve();*/


       
       

       SAMCRA sam=new SAMCRA(main_mat,mat,cons,2,1000);
                        sam.solve(src,dst);
                        long duration_sam =-1;
                        if(sam.findpath)
                        {
                            int[] m=new int[sam.BestPathLenght];
                            m=sam.BestPath;
                                    
                       }
                        else{
                            System.out.print("there is no feasible solution for SAMCRA");
                        duration_sam =-1;}
                        
       SAMCRA sam2=new SAMCRA(f.Graph_FuzzyWeights(main_mat,mat,1),mat,cons,2,1000);
sam2.solve(src, dst);
SAMCRA sam3=new SAMCRA(f.Graph_FuzzyWeights(main_mat,mat,2),mat,cons,2,1000);
sam3.solve(src, dst);


                        Ant a=new Ant(main_mat,100,5,mat,200);
                         a.start(src,dst);
                         Ant a1=new Ant(f.Graph_FuzzyWeights(main_mat,mat,1),100,5,mat,200);
                         a1.start(src,dst);
                         Ant a2=new Ant(f.Graph_FuzzyWeights(main_mat,mat,2),100,5,mat,200);
                         a1.start(src,dst);

        /*Dijkstra di=new Dijkstra();
        di.solve(main_mat,src,dst);
        int[] h=new int[di.pathlenght];
        h=di.bestpath;
        for(int i=0; i<di.pathlenght; i++)
            System.out.print((h[i]+1*/

    }
    
}
