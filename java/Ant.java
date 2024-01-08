
import java.util.Random;
public class Ant {
            public  double ALPHA = 1;
            public  double BETA = 1;
            public  double Q =1; // somewhere between 0 and 1
            public   double Rho=0.05;
            public   double INFINITY=999999999;
            public   int ITERATION=1000;
            public  double INITIAL_PHEROMONES = 0.0012; // can be anything
            public   int DELAY_THRESH=0;
            double[][] Node_Matrix;
            double[][] Delay_Matrix;
            double[][] invertedMatrix;
            double[][] pheromones;
            double best_cost=INFINITY;
            int best_delay;
            boolean findpath=false;
            int l_index=0;
           int []   Best_Path;
            int Ants_number=4;
            int  Dest=0,Src=0;
            static class ant {
                  int[] path;
                  double cost;
                  public ant(int[] x, double y) {
                   super();
                  this.path = x;
                  this.cost = y;
                  }
             }
            ant[] ant_matrix;
            public boolean find_path()
            {
                    return findpath;
            }
            public int[] Ant_Best_Path()
            {
                    return Best_Path;
            }
            public int Ant_Best_Path_Length()
            {
                    return l_index;
            }
            public Ant(double[][] mat,int iter,int ant_count,double[][] del,int dt)
            {
               Ants_number=ant_count;
               ITERATION=iter;
               best_cost=INFINITY;
               DELAY_THRESH=dt;
               best_delay=dt;//delay between first switch and source+delay between last switch and dest
               Node_Matrix=Init_Node_Matrix(mat);
               Delay_Matrix=Init_Delay_Matrix(del);
               invertedMatrix=invertMatrix();
               pheromones=initializePheromones();
               InitAnts(Ants_number);
               Best_Path=new int[Node_Matrix.length];
               // start();
            }
            public  double[][] Init_Node_Matrix(double[][] m)
            {
                    double[][] Node_Matrix = new double[m.length][];
                    for(int i = 0; i< m.length; i++){
                     Node_Matrix [i] = new double[m[i].length];
                     for (int j = 0; j < m[i].length; j++)
                     {
                               if(m[i][j]!=0)
                                      Node_Matrix[i][j] = m[i][j];
                                else
                                       Node_Matrix[i][j]=INFINITY;
//System.out.print(Node_Matrix[i][j]+"       ");
                     }
//System.out.println("       ");
                    }
                    return Node_Matrix;
            }
            public  double[][] Init_Delay_Matrix(double[][] m)
            {
                    double[][] Delay_Matrix = new double[m.length][];
                    for(int i = 0; i< m.length; i++){
                           Delay_Matrix [i] = new double[m[i].length];
                     for (int j = 0; j < m[i].length; j++)
                     {
                               if(m[i][j]!=0)
                                               Delay_Matrix[i][j] = m[i][j];
                                else
                                         Delay_Matrix[i][j]=0;
                     }
                    }
                    return Delay_Matrix;
            }
         public double[][] invertMatrix() {
                        double[][] invertedMatrix = new double[ Node_Matrix.length][ Node_Matrix.length];
                        for (int i = 0; i <  Node_Matrix.length; i++) {
                              for (int j = 0; j <  Node_Matrix.length; j++) {
                                       invertedMatrix[i][j] = (double)(1/Node_Matrix[i][j]);
//System.out.print(invertedMatrix[i][j]+"       ");
                              }
//System.out.println(" ");
                        }
               return invertedMatrix;
             }
         public double[][] initializePheromones() {
                        double[][] pheromones = new double[Node_Matrix.length][Node_Matrix.length];
                        int rows = Node_Matrix.length;
                        for (int columns = 0; columns < Node_Matrix.length; columns++) {
                                for (int i = 0; i < rows; i++) {
                                          pheromones[columns][i] = INITIAL_PHEROMONES;
//System.out.print( pheromones[columns][i]+" ");
                                 }
//System.out.println(" ");
                         }
                     return pheromones;
         }
        public void InitAnts(int numAnts)
         {
                    ant_matrix = new ant[numAnts];
                   int[] temp=new int[Node_Matrix.length];
                    for(int i=0; i<Node_Matrix.length;i++) temp[i]=-1;
                    for (int k = 0; k < numAnts; k++) {
                                 //ant_matrix[k].cost =0 ;
                                 ant_matrix[k]=new ant(temp,INFINITY);
                                 //System.out.println( ant_matrix[k].cost+"======= "+ ant_matrix[k].path[1]);
                                // ant_matrix[k].path =temp;
                         }
             }
         public void Evaporate(int last_index_)
         {
               for (int k = 0; k < Ants_number; k++){
                         if(ant_matrix[k].path[last_index_]==Dest)//last cell of path array
                                    for(int i=0; i<last_index_; i++){
                                            int p=ant_matrix[k].path[i];
                                            int q=ant_matrix[k].path[i+1];
                                             invertedMatrix[p][q]=(1-Rho)*invertedMatrix[p][q];
                                             //System.out.print( invertedMatrix[p][q]+" e ");
                                      }
                                           //System.out.println(" ");

               }
         }
         public void Update_Phromone(int last_index_)
         {
              for (int k = 0; k < Ants_number; k++){
                          if(ant_matrix[k].path[last_index_]==Dest)//last cell of path array
                                    for(int i=0; i<last_index_; i++){
                                            int p=ant_matrix[k].path[i];
                                           int q=ant_matrix[k].path[i+1];
                                            //System.out.print(invertedMatrix[p][q]+" p ");
                                             invertedMatrix[p][q]=invertedMatrix[p][q]+Q/ant_matrix[k].cost;
                                           //System.out.print(invertedMatrix[p][q]+"  ");
                                     }
                                           /////System.out.println();
                  }
         }
        public double Get_Cost(int[] p, int l_index)
        {
               double cost=0.0;
               for(int i=0; i<l_index; i++)
                        cost+=Node_Matrix[p[i]][p[i+1]];
               return cost;
         }
         public void start(int src,int dst)
         {
                        System.out.print("start has been called\n");
                        Src=src-1; //because the index of nodematrix begins from 0
                        Dest=dst-1; //because the index of nodematrix begins from 0
             int last_index_=0;
                  for(int i=0; i< ITERATION; i++){
                  for (int k = 0; k < Ants_number; k++){
                                ant_matrix[k].path[0]=Src;
                                last_index_=0;
                                    double max_prob=0;
                                    int index=0;
                                    boolean findpath_flag=true;
                              while(ant_matrix[k].path[last_index_]!=Dest){
                                 int q=ant_matrix[k].path[last_index_];
                                    index=RolletWheel(q);
                                 // System.out.println("index is="+index);
                                    if(index!=-1 && !Exist(ant_matrix[k].path,last_index_,index))
                                    {
                                            last_index_++;
                                            ant_matrix[k].path[last_index_]=index;
                                      // for(int h=0;h<=last_index_;h++)
                                          //System.out.println("ant_matrix[k].path[last_index_] is  ="+ant_matrix[k].path[h]);
                                     }
                                 else
                                    {
                                           //System.out.println("cant find path");
                                                 findpath_flag=false;
                                                 break;

                                      }
                              }
                                             //System.out.println("-------------");
                                     if(findpath_flag && Satisfy_Delay(ant_matrix[k].path, last_index_)){
                                    ant_matrix[k].cost=Get_Cost(ant_matrix[k].path,last_index_);
                                 Update_Phromone(last_index_);
                                 Evaporate(last_index_);
                                //System.out.println("cost is="+Get_Cost(ant_matrix[k].path,last_index_));
                                if(Get_Cost(ant_matrix[k].path,last_index_)<=this.best_cost || Get_total_delay(ant_matrix[k].path, last_index_)<=this.best_delay)
                                {
                                                       this.best_cost=Get_Cost(ant_matrix[k].path,last_index_);
                                                       this.best_delay=Get_total_delay(ant_matrix[k].path, last_index_);
                                                       Copy_Best_Path(ant_matrix[k].path,last_index_);
                                                       this.l_index=last_index_;
                                                       this.findpath=true;
                                }
                              }
               }
            }
             if(this.findpath)
                  {
                           System.out.println("best cost is="+this.best_cost);
                           System.out.println("the delay of path is="+(this.best_delay+100));
                           //because in my simulation the link between src node and first switch
                           //and the link between last switch and dest node is 50ms and is not considered in graph of swithes
                          for(int m=0; m<=l_index; m++)
                         {
                               System.out.print((Best_Path[m]+1)+"-->");
                          }
                        System.out.println("\n***********************************");
              }
}
         public boolean Satisfy_Delay(int[] a,int l_index)
         {
             int total_delay=Get_total_delay(a, l_index);
             if(total_delay<=DELAY_THRESH)
                  return true;
             else
                 return false;
         }
         public int Get_total_delay(int[] a,int l_index)
         {
              int total_delay=0;
             for(int i=0; i<l_index; i++)
                      total_delay+=Delay_Matrix[a[i]][a[i+1]];
             return total_delay;
         }
         public void Copy_Best_Path(int[] a,int l_index)
         {
                   for(int i=0; i<Node_Matrix.length; i++)
                          this.Best_Path[i]=0;
                   for(int i=0; i<=l_index; i++)
                              this.Best_Path[i]=a[i];
         }
         public boolean Exist(int[] a,int l_index,int f)
         {
                  boolean flag=false;
                  for(int x=0; x<=l_index; x++)
                     if(a[x]==f) flag=true;
               return flag;
            }
         public int RolletWheel(int rowindex)
         {
                  Random r=new Random();
                  double Sum_Prob=0.0,sum=0.0,p=0.0, max_prob=0;
                  double s= r.nextDouble();
                        int ret=-1  ,temp_index=0;
                        boolean flag=true;
                        //System.out.println("random is"+s);
                                 for(int x=0; x<Node_Matrix.length; x++)
                                                             {
                                                               if(Node_Matrix[rowindex][x]!=INFINITY)
                                                 Sum_Prob+=Math.pow(invertedMatrix[rowindex][x],BETA)*Math.pow(pheromones[rowindex][x],ALPHA);
                                                               }
                  for(int x=0; x<Node_Matrix.length; x++){
                                      if(Node_Matrix[rowindex][x]!=INFINITY)
                                 p=Math.pow(invertedMatrix[rowindex][x],BETA)*Math.pow(pheromones[rowindex][x],ALPHA);
                                                 else
                                                                   p=0;
                                                 //System.out.println("prob is "+p);

                                                                sum+=p/Sum_Prob;
                                                                if(p>max_prob){max_prob=p; temp_index=x;}
                                                                                           if((sum>s)&&(flag)){
                                                                                                flag=false;
                                                                                                ret=x;
                                                                //System.out.println("sum is "+sum+" index is "+x);
                                                                                              }
                                          }
                  if(flag)
                  {
                        //  ret=temp_index;System.out.println("MAX IS USED");
                  }//when the rolletwheel can't find the index
                   return ret;
         }
}
