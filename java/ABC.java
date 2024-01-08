
//import java.lang.Math;
import java.util.Random;
public  class ABC {

        int M=500; // The rows and columns of Graph
        int EdgeNumber=M*(M-1)/2;
        boolean Find_Path=false;
         int  Best_Path_Len=0;
        int Source=0;
        int runtime=50;
        int Dest=19;
        long  INFINITY=999999999;
        int DELAY_THRESH=200;
        double[][] Graph;//=new double[M][M];
        double Edges[][]=new double[4][EdgeNumber]; // First and Second row is the indexes of edge and Third row indicates the edge cost, forth row indicates edge delay
        int NP=15; /* The number of colony size (employed bees+onlooker bees)*/
        int FoodNumber = NP/2; /*The number of food sources equals the half of the colony size*/
        int limit = 10;  /*A food source which could not be improved through "limit" trials is abandoned by its employed bee*/
        int maxCycle = 500; /*The number of cycles for foraging {a stopping criteria}*/
        double Global_MinCost=INFINITY;
        int tempfood_coefficient=50;
        double Global_MinPath[];
        double Foods[][];
        double TempFoods[][];
        double Fitness[];
        double Solution[];
        double BestSolution[];
        double prob[];
        public double trial[];
       int[] Best_Path;
        /*Extract Graph edges*/
        void Extract_Edges(double[][] G,double[][] delay)
        {
                int Edge_count=0;
                for(int i=0; i<G.length; i++)
                  {
                        for(int j=0; j<G.length; j++)
                          {
                             //  System.out.print(G[i][j]+"   ");
                                if(G[i][j]>0)
                                {
                                   Edges[0][Edge_count]=i;
                                   Edges[1][Edge_count]=j;
                                   Edges[2][Edge_count]=G[i][j]; // cost
                                   Edges[3][Edge_count]=delay[i][j];   //delay
                                   Edge_count++;
                                }
                            }
                         // System.out.println();
                          EdgeNumber=Edge_count;
                   }
                //System.out.println(EdgeNumber);

        }
        /*Path cost calculation*/
         double Path_Cost(double[]FoodRow)
         {
                double cost=0;
                for(int i=0; i<EdgeNumber; i++)
                        if((int)FoodRow[i]>=0)cost+=Edges[2][(int)FoodRow[i]]; // Third row indicates the edge cost
                return cost;
         }
        /*Path cost calculation*/
         double Path_Delay(double[] FoodRow)
         {
                double delay=0.0;
                for(int i=0; i<EdgeNumber; i++)
                        if((int)FoodRow[i]>=0){delay+=Edges[3][(int)FoodRow[i]];} // Third row indicates the edge cost
                return delay;
         }
        /*Fitness function*/
        double CalculateFitness(double[] FoodRow)
         {
                 double result=0, c=Path_Cost(FoodRow) , d=Path_Delay(FoodRow);
                 boolean find=false;
                 for(int i=0; i<EdgeNumber; i++)
                    if((int)FoodRow[i]>=0 && (int)Edges[1][(int)FoodRow[i]]==Dest){find=true; break;}
                 if(find)
                  {
                         if(d>DELAY_THRESH) result=INFINITY;
                         else
                                   result=c+1/d;
                }
                else
                        result=INFINITY;
                 return result;
         }

    boolean IsValid_Path(int src,int dst, int[] p)
        {
                boolean IsValid=false;
                for(int i=0; i<EdgeNumber-1; i++)
                         if(p[i]==dst) IsValid=true;
                if(p[0]!=src) IsValid=false;
                return IsValid;
        }
        void CalculateProbabilities()
        {
             int i;
             double maxfit;
             maxfit=CalculateFitness(Foods[0]);
          for (i=1;i<FoodNumber;i++)
                {
                            double f=CalculateFitness(Foods[i]);
                   if (f>maxfit)
                   maxfit=f;
                }
         for (i=0;i<FoodNumber;i++)
                {
                          double f=CalculateFitness(Foods[i]);
                 prob[i]=(f/maxfit);
                }
        }
                /*The best food source is memorized*/
        void MemorizeBestSource()
        {
           int i,j;
                for(i=0;i<FoodNumber;i++)
                {
                if (CalculateFitness(Foods[i])<=Global_MinCost)
                        {
                Global_MinCost=CalculateFitness(Foods[i]);
                for(j=0;j<EdgeNumber;j++)
                   Global_MinPath[j]=(int)Foods[i][j];
                }
                }
         }
        int[] Make_Path(double[] FoodRow)
        {
                int path[]=new int[EdgeNumber];
                for(int i=0; i<EdgeNumber; i++)
                {
                        path[i]=-1;
                }
                if ((int)FoodRow[0]>=0) {
                        path[0]=Source;
                                for(int i=0; i<EdgeNumber-1; i++)
                                {
                                        if((int)FoodRow[i]>=0)
                                        {
                                                path[i+1]=(int)Edges[1][(int)FoodRow[i]];
                                                if((int)Edges[1][(int)FoodRow[i]]==Dest)break;
                                        }
                                }
                }
                return path;
        }
        int Path_Len(int[] path)
         {
            int len=0;
            for(int i=0; i<EdgeNumber; i++)
                 if(path[i]!=-1) len++;
           return len;
         }
        /*All food sources are initialized */
        public double[] Init_Food(int i)
        {
                boolean find=false , loop=false , pair=false;
                boolean insert=false;
                int thresh=10,z=0;
                 Random q=new Random();
                 Random x=new Random();
                  double[] temp_food=new double[EdgeNumber];
                for(int t=0; t<EdgeNumber; t++)
                                {
                                        temp_food[t]=-1; //initialize
                                }
                                int tem=0;
                                int[] temp_src_neighbor=new int[EdgeNumber];
                                for(int t=0; t<EdgeNumber; t++)
                                {
                                        if(Edges[0][t]==Source)
                                        {
                                                temp_src_neighbor[tem]=t;// the edge which begins or ends at the source node
                                                tem++;
                                        }
                                }
                                int e=x.nextInt(tem);
                            temp_food[0]=temp_src_neighbor[e];
                                int r=(int)temp_food[0];
                                for(int k=1; k<EdgeNumber; k++)
                                {
                                        if(Edges[1][r]==Dest) break;
                                        int[] neighbor=new int[EdgeNumber];
                                        for(int t=0; t<EdgeNumber; t++)
                                        {
                                                neighbor[t]=-1; //initialize
                                        }
                                        int neighbor_count=0;
                                        for(int t=0; t<EdgeNumber; t++)
                                        {
                                          if(Edges[1][r]==Edges[0][t])
                                          {
                                                neighbor[neighbor_count]=t; //find neighbour
                                                neighbor_count++;
                                          }
                                        }
                                        insert=false;
                                         z=0;
                                        while(!insert && z<thresh)
                                        {
                                                        z++;
                                                  int h = q.nextInt(neighbor_count);
                                                  int ran=neighbor[h];
                                                  find=false;
                                                  pair=false;
                                                  loop=false;
                                                for (int m=0; m<k; m++)
                                                        if(ran==(int)temp_food[m]) find=true; // an Edge cannot be repeated twice in a food
                                                for (int m=0; m<k; m++)
                                                        if(Edges[0][ran]==Edges[1][(int)temp_food[m]] && Edges[1][ran]==Edges[0][(int)temp_food[m]]) pair=true; // an Edge should not be the pair of another edge in a food (i,j)=(j,i)
                                                for (int m=0; m<k; m++)
                                                   if( Edges[1][ran]==Edges[0][(int)temp_food[m]])
                                                         loop=true;// an Edge should not make a loop in a food
                                                   if(!find && !loop && !pair)
                                                   {
                                                                temp_food[k]=ran;
                                                                insert=true;
                                                                r=ran;
                                                        }
                                        }
                                        if(!insert) break;
                                }
           return temp_food;
        }
        public void Initial_Foods()
        {
                for(int i=0;i<FoodNumber*tempfood_coefficient;i++)
                {
                  double[] temp_food=new double[EdgeNumber];
                  temp_food=Init_Food(i);
                  for(int j=0; j<EdgeNumber; j++)
                     TempFoods[i][j]=temp_food[j];

                }
                        //copying unique solution from TempFoods to Foods matrix
                        for(int i=0; i<FoodNumber; i++)
                                for(int j=0; j<EdgeNumber; j++)
                                        Foods[i][j]=-1;
                        int t=0;
                        for(int i=0; i<FoodNumber*tempfood_coefficient; i++)
                        {
                                boolean ff=false,not_exist=true;
                                not_exist=true;
                                for(int j=0; j<FoodNumber; j++)
                                {
                                        ff=false;
                                        for(int k=0; k<EdgeNumber; k++)
                                           if(TempFoods[i][k]!=Foods[j][k]) ff=true;
                                                not_exist=not_exist&&ff;
                                }
                                if(not_exist)
                                           {
                                                for(int k=0; k<EdgeNumber; k++)
                                                        Foods[t][k]=TempFoods[i][k];
                                                        t=(++t)%FoodNumber;
                                                }
                        }
                        FoodNumber=t;
        for(int i=0; i<FoodNumber; i++)
                        {
                           trial[i]=0;
                           Fitness[i]= CalculateFitness(Foods[i]);
                         }
        }
void SendEmployedBees()
        {
                double Temp[][]=new double[FoodNumber][EdgeNumber];
                        for(int i=0; i<FoodNumber; i++)
                        for(int j=0; j<EdgeNumber; j++)
                        {
                            Temp[i][j]=Foods[i][j];
                                Foods[i][j]=-1;
                        }
                         int t=0;
                        boolean find=false;
                                Random q=new Random();

                for(int i=0; i<FoodNumber; i++)
                {
                        int r=q.nextInt(FoodNumber); // each employed bee choose a random food
                        for(int j=0; j<EdgeNumber; j++)
                        {
                            if(Temp[r][j]>=0 && Edges[1][(int)Temp[r][j]]==Dest) find=true;
                        }
                        if(find)
                        {
                                for(int j=0; j<EdgeNumber; j++)
                           {
                                        if(Temp[r][j]>=0)
                                        {
                                                           Foods[t][j]=Temp[r][j];
                                        }

                            }
                                     double fit=CalculateFitness(Foods[t]);
                 if(Fitness[t]<fit)
                                        {
                                                trial[t]=trial[t]+1;
                                                //System.out.println( "****************************prev="+Fitness[t]+" now="+fit);
                                        }
                                        else   trial[t]=0;
                                        t++;
                                        find=false;
                        }
                }
                FoodNumber=t;
        }
void SendOnlookerBees()
        {
        boolean find=false , loop=false , pair=false;
        boolean insert=false;
          int w=0;
          int thresh=9999,z=0;
          double[] temp=new double[EdgeNumber];
                  for(int t=0; t<EdgeNumber; t++)
                        {
                                temp[t]=-1; //initialize
                        }
           Random q=new Random();
           Random x=new Random();
           /*v_{ij}=x_{ij}+\phi_{ij}*(x_{kj}-x_{ij}) */
          while(w<FoodNumber)
          {
                double c=Math.random();
                        if(c<prob[w]){
                                        boolean f=true;
                                                int b=0, last_index=0;
                                                int r=0; int a=0;
                                                for(int i=0; i<EdgeNumber; i++)
                                                        if(Foods[w][i]==-1)
                                                        {
                                                           last_index=i;
                                                           break;
                                                        }
                        //System.out.println( "last index="+last_index);

                                                        if(last_index<2) last_index=2; //because next command needs positive parameters
                                                         b=q.nextInt(last_index-1);
                                                         r=(int)Foods[w][b];
                                                        //System.out.println( "nb="+r+"    "+Edges[0][r]+","+Edges[1][r]);
                                                 while(a<=b)
                                                 {
                                                         temp[a]=Foods[w][a];
                                                         a++;
                                                }
                                                 if(Foods[w][b]!=-1 && Edges[1][(int)Foods[w][b]]!=Dest)
                                                 {
                                                                 for(int k=b+1; k<EdgeNumber; k++)
                                                                        {
                                                                                                if(Edges[1][r]==Dest){break;}
                                                                                                int[] neighbor=new int[EdgeNumber];
                                                                                                for(int t=0; t<EdgeNumber; t++)
                                                                                                {
                                                                                                        neighbor[t]=-1; //initialize
                                                                                                }
                                                                                                int neighbor_count=0;
                                                                                                for(int t=0; t<EdgeNumber; t++)
                                                                                                {
                                                                                                  if(Edges[1][r]==Edges[0][t]) neighbor[neighbor_count++]=t; //find neighbour
                                                                                                }
                                                                                         //System.out.println( "before while="+r);
                                                                                                insert=false;
                                                                                                 z=0;
                                                                                                while(!insert && z<thresh)
                                                                                                {
                                                                                                                z++;
                                                                                                          int h = x.nextInt(neighbor_count);
                                                                                                          int ran=neighbor[h];
                                                                                                          find=false;
                                                                                                          pair=false;
                                                                                                          loop=false;
                                                                                                        for (int m=0; m<k; m++)
                                                                                                                if(ran==(int)temp[m]) find=true; // an Edge cannot be repeated twice in a food
                                                                                                        for (int m=0; m<k; m++)
                                                                                                                if(Edges[0][ran]==Edges[1][(int)temp[m]] && Edges[1][ran]==Edges[0][(int)temp[m]]) pair=true; // an Edge should not be the pair of another edge in a food (i,j)=(j,i)
                                                                                                        for (int m=0; m<k; m++)
                                                                                                                if( Edges[1][ran]==Edges[0][(int)temp[m]]) loop=true; // an Edge should not make a loop in a food
                                                                                                           if(!find && !loop && !pair)
                                                                                                           {
                                                                                                                        temp[k]=ran;
                                                                                                                        insert=true;
                                                                                                                        r=ran;
                                                                                                                }
                                                                                                }
                                                                        //        System.out.println( "after while="+insert);

                                                                                                if(!insert)
                                                                                                {
                                                                                        //        System.out.println( "not inserted="+insert);
                                                                                                        for(int t=0; t<EdgeNumber; t++)
                                                                                                        {
                                                                                                                temp[t]=-1; //reinitialize
                                                                                                        }
                                                                                                break;
                                                                                                }
                                                                        }
                                                 }
                                         double fit1=CalculateFitness(temp), fit2=CalculateFitness(Foods[w]);
                                         if(fit1<fit2)
                                         {
                                                for(int e=0; e < EdgeNumber; e++)
                                                {
                                                        if(temp[e]>=0)
                                                           Foods[w][e]=temp[e];
                                                 }
                                                 trial[w]=0;
                                         }
                                         else trial[w]=trial[w]+1;
                                 }
                        w++;
          }
        }
        void SendScoutBees()
        {
        int maxtrialindex,i;
        maxtrialindex=0;
        for (i=1;i<FoodNumber;i++)
                {
                 if (trial[i]>trial[maxtrialindex])
                 maxtrialindex=i;
                }
        if(trial[maxtrialindex]>=limit)
        {
                Init_Food(maxtrialindex);
        }
        }
        void Show_Path(int[] p)
        {
                for(int i=0;i<EdgeNumber; i++)
                                {
                                if(p[i]>=0)
                                  {
                                          System.out.print((p[i]+1)+"->");
                                  }
                                  }
                                  System.out.println("   Fitness is="+CalculateFitness(Global_MinPath)+"  Cost is="+Path_Cost(Global_MinPath)+"   Delay is="+(Path_Delay(Global_MinPath)+100));
        }
        public ABC(double[][] Graph,int mc,int run_count,double[][] Delay_Mat,int dl_thresh)
        {    
               runtime=run_count;
                M=Graph.length;
                EdgeNumber=M*M;//*(M-1)/2;//mesh unidirectional graph
                Edges=new double[4][EdgeNumber];
                NP=M;
                FoodNumber = NP/2;
                int tempfood_coefficient=50;
                Global_MinPath=new double[EdgeNumber];
                 Foods=new double[FoodNumber][EdgeNumber];
                 TempFoods=new double[FoodNumber*tempfood_coefficient][EdgeNumber];
                 Fitness=new double[FoodNumber];
                 Solution=new double[EdgeNumber];
                BestSolution=new double[EdgeNumber];
                 prob=new double[FoodNumber];
                 trial=new double[FoodNumber];
                DELAY_THRESH=dl_thresh;//+100;//delay between first switch and source+delay between last switch and dest
                Find_Path=false;
                maxCycle=mc;
                Extract_Edges(Graph,Delay_Mat);
        }
    public void start(int src,int dst)
        {
                Source=src-1;//because indexes begin from zero
                Dest=dst-1;
                double tempbest[]=new double[EdgeNumber];
                double temset_fitness=INFINITY;
                for(int run=0; run<runtime; run++)
                {
                                Initial_Foods();
                                MemorizeBestSource();
                                for (int iter=0;iter<maxCycle;iter++)
                                        {
                                                SendEmployedBees();
                                                CalculateProbabilities();
                                                SendOnlookerBees();
                                                MemorizeBestSource();
                                                SendScoutBees();
                                        }
                        int q[]=new int[EdgeNumber];
                   q=Make_Path(tempbest);
                   //Show_Path(q);
                                if(CalculateFitness(Global_MinPath)<temset_fitness)
                                {
                                   for(int j=0; j<EdgeNumber; j++)
                                                tempbest[j]=Global_MinPath[j];
                                        temset_fitness=CalculateFitness(tempbest);
                                }
                }
                        int p[]=new int[EdgeNumber];
                   p=Make_Path(tempbest);
                   if (IsValid_Path(Source,Dest,p))
                   {
                           System.out.println("--------------------------------------------------------------------------");
                           System.out.print("THE BEST PATH IS with len="+Path_Len(p)+"*** ");
                           Show_Path(p);
                           Find_Path=true;
                           Best_Path_Len=Path_Len(p);
                           Best_Path=new int[EdgeNumber];
                           for(int i=0; i<EdgeNumber; i++)
                                Best_Path[i]=p[i];
                       }


         }
       public int[] ABC_Best_Path()
        {
            return  Best_Path;
         }
        /* public static void main(String[] args) {
                        ABC a=new ABC();
        }*/
}
