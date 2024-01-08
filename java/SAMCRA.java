import java.util.*;
public class SAMCRA{
	public int node_number;
	public double[] constraints;
	public int const_num;
	public boolean findpath=false;
	int source;
	int destination;
    double[][] Node_Matrix;
    double[][] Delay_Matrix;
    int[] BestPath;
    int BestPathLenght=0;
    double BestPathCost=0;
    double INFINITY=999999999;
    double iteration=0;
    static class q_element {
        int parent_id;
        int parent_id_index;
        double score;
        boolean gray;
    }
    
    LinkedList<q_element>[]  node_queue;
    
    public SAMCRA(double[][] mat,double[][] del,double[] constr,int numconst,int maxtry)
    {
    	constraints=constr;
    	const_num=numconst;
    	node_number=mat.length;
    	Node_Matrix=mat;
    	Delay_Matrix=del;
    	iteration=maxtry;
    	
    }
    public void solve(int src,int dst)
    {
    	node_queue= new LinkedList[node_number];
    	q_element qe;
    	src=src-1;
    	dst=dst-1;
    	int endvalue=1;
    	double lastscore=0;
    	for(int i=0; i<node_number; i++)
    		node_queue[i]=new LinkedList<q_element>();
    	//source node
		qe=new q_element();
		qe.parent_id=-1;
		qe.parent_id_index=-1;
		qe.score=0;
		qe.gray=true;
    	node_queue[src].add(qe);
    	int adjnode=0;
    	int candid_node=src;
    	int h=0;
    	while(h<=iteration)
    	{
    		int neighbor_number=0;
    		for(int i=0; i<Node_Matrix.length; i++)
	    		if(Node_Matrix[candid_node][i]!=0)//adjacency
	    		{
	    			neighbor_number++;
	    		}
    		double[] tempscore=new double[neighbor_number];
    		int[] tempindex=new int[neighbor_number];
    		int[] tempid=new int[neighbor_number];
    		int[] tempid_index=new int[neighbor_number];
    		int k=0;
    		boolean flag=false;
		    	for(int i=0; i<node_number; i++)
		    		if(Node_Matrix[candid_node][i]!=0 && !Is_Loop(node_queue[candid_node],i))//adjacency
		    		{
		    			adjnode=i;
						double max=0.0;
						double score1=Node_Matrix[candid_node][adjnode];///constraints[0];//cost
						double score2=Delay_Matrix[candid_node][adjnode];///constraints[1];//delay
						//max=score1>score2?score1:score2;
						max=score2;
					
						
						qe=new q_element();
						qe.parent_id=candid_node;
						tempid[k]=qe.parent_id;
						//find last index of this parent
						int temp_pid_index=0;
						for(int t=0; t<node_queue[i].size(); t++)
							if(node_queue[i].get(t).parent_id==candid_node)
								temp_pid_index=node_queue[i].get(t).parent_id_index;
						
						qe.parent_id_index=temp_pid_index+1;
						tempid_index[k]=qe.parent_id_index;
						qe.gray=false;

						double tempeval=Path_Length(node_queue, src,qe.parent_id,qe.parent_id_index);
						//tempeval=lastscore;
			    		//System.out.println("max="+max+" tempeval="+(tempeval)+" cons="+constraints[1]);

						if(/*(max+tempeval)<=constraints[0] &&*/ (max+tempeval)<=constraints[1])
						{		
							tempscore[k]=max+tempeval;
							tempindex[k]=i;
							qe.score=max+tempeval;	
							node_queue[i].add(qe);
						    	
				    		//System.out.println("qe.parent_id="+qe.parent_id+"  qe.parent_id_index="+qe.parent_id_index);

								flag=true;
								
							//	System.out.println("candid="+candid_node+"  index="+tempindex[k]+"  score="+tempscore[k]);
										k++;
						}		
		    		}
		    	
		    	double min=tempscore[0];
		    	int min_index=tempindex[0];
		    	int min_pid=tempindex[0];
		    	int min_pidindex=tempindex[0];
		    	if(flag)
		    	{
					   
		    		min=tempscore[0];
			    	min_index=tempindex[0];
			    	min_pid=tempindex[0];
			    	min_pidindex=tempindex[0];
					    	for(int i=0; i<k; i++)
					    	{
					   // 		System.out.println("tempindex="+tempindex[i]);
					    		if(min>=tempscore[i] )
					    		{
					    			min=tempscore[i];
					    			min_index=tempindex[i];
					    			min_pid=tempid[i];
					    			min_pidindex=tempid_index[i];
					    		}
					    	}
		    	}
		    	else {min=INFINITY;} //if there is no adjacent node, the minimum score should be select from gray nodes 
		    	//search for other none gray node
		    	for(int i=0; i<node_number; i++)
		    	{
		    		for(int j=0; j<node_queue[i].size(); j++)
		    		{
		    			if(node_queue[i].get(j).gray==false)
		    			{
		    				if(node_queue[i].get(j).score<=min)
		    				{
		    					min=node_queue[i].get(j).score;
		    					min_index=i;
				    			min_pid=node_queue[i].get(j).parent_id;
				    			min_pidindex=node_queue[i].get(j).parent_id_index;
		    				}
		    			}
		    		}
		    	}
		    	
		    	if(min==0 || min==INFINITY) //there is no solution
		    	{
		    		findpath=false;
		    		break;
		    	}
					    	 //mark as a gray node
					 		qe=new q_element();
							qe.parent_id=min_pid;
							qe.parent_id_index=min_pidindex;
							qe.score=min;
							qe.gray=true;
							for(int i=0;i<node_queue[min_index].size(); i++)
								if(node_queue[min_index].get(i).parent_id==qe.parent_id && node_queue[min_index].get(i).parent_id_index==qe.parent_id_index )
								{
									node_queue[min_index].remove(i);
									node_queue[min_index].add(i,qe);
								}		    	
							
						   	if(candid_node==dst )
						   		{
						   			BestPath=new int[node_number];
						   		  BestPath=Show_Path(node_queue,src, dst);
						   		  
						   		  for(int i=0; i<BestPathLenght; i++)
						   			System.out.print((BestPath[i]+1)+"->");
						   		  
						   		  
						   		System.out.println("\ncost is=" +BestPathCost);
						   		findpath=true;
						   		break;
						   		}
						  // 	lastscore=min;
					    	 candid_node=min_index;
					    //	 show_linklist();
					    	 h++;
					    	 findpath=false;
					    	 
    	}
     }
    public int[] Show_Path(LinkedList<q_element>[] nodeq,int src,int dst)
    {
    	int[] tpath=new int[node_number];
    	int[] path=new int[node_number];
    	int lenp=0;
    	int pid=0;
    	int pid_index=0;
    	double cost=0;
		tpath[lenp++]=dst;
    	for(int i=0; i<nodeq[dst].size(); i++)
    	{
    		if(nodeq[dst].get(i).gray==true)
    		{
    			pid=nodeq[dst].get(i).parent_id;
    			pid_index=nodeq[dst].get(i).parent_id_index;
    		//	System.out.println("precost="+nodeq[dst].get(i).score);
    		}
    	}
		tpath[lenp++]=pid;
	//	cost+=Node_Matrix[dst][pid];
		//System.out.println("pidt="+dst+","+pid+"="+Node_Matrix[dst][pid]);
    	while(pid!=src)
    	{
	    	if(pid_index>=-1)
	    	{	    		
	    		int pidt=pid;
	    		pid=nodeq[pid].get(pid_index-1).parent_id;
	    		tpath[lenp++]=pid;
	    		//cost+=Node_Matrix[pidt][pid];
	    		//System.out.println("pidt="+pidt+","+pid+"="+Node_Matrix[pidt][pid]);
	    		pid_index=nodeq[pidt].get(pid_index-1).parent_id_index;
	    	}
    	}
    	int k=0; //because tpath is reverse path
    	for(int i=lenp-1; i>=0; i--)
    	{
    		path[k++]=tpath[i];
    	}
    	
         for(int i=0; i<lenp-1; i++)
                  cost+=Node_Matrix[path[i]][path[i+1]];
         
    	BestPathCost=cost;
    	BestPathLenght=lenp;
    	return path;
    	
    }
    public double Path_Length(LinkedList<q_element>[] nodeq,int src,int parent_id,int paid_index)
    {
    	double len=0;
    	int pid=parent_id;
    	int pid_index=paid_index;
    	if(pid!=src && pid_index>=-1)
    	{
    		//System.out.println("pid="+pid+"  pidindex="+pid_index+" cost="+nodeq[pid].get(pid_index-1).score);
    		len+=nodeq[pid].get(pid_index-1).score;
    		int pidt=pid;
    		pid=nodeq[pid].get(pid_index-1).parent_id;
    		pid_index=nodeq[pidt].get(pid_index-1).parent_id_index;
    	}
    	return len;
    }
    public boolean Is_Loop(LinkedList<q_element> nodeq, int nodeid)
    {
    	boolean isloop=false;
    	for(int i=0; i< nodeq.size(); i++)
    	{
    		if(nodeq.get(i).parent_id==nodeid)
    		{
    			isloop=true;
    		}
    	}
    	return isloop;
    }
    public void show_linklist()
    {
    	for(int j=0; j<node_number; j++){
		for(int i=0;i<node_queue[j].size(); i++)
			
			{
				System.out.println("node="+j+"  parent="+node_queue[j].get(i).parent_id+"  pindex="+node_queue[j].get(i).parent_id_index+" score="+node_queue[j].get(i).score+"  size="+node_queue[j].size()+ "  gray="+node_queue[j].get(i).gray);
			}
    	}
    }
    public static void main(String[] args) {
    	
       	double[][]  MainGraph={
    			{0,4,2,0,0,0,0,0},
    			{4,0,0,2,3,0,0,0},
    			{2,0,0,0,5,0,7,0},
    			{0,2,0,0,0,5,0,0},
    			{0,3,5,0,0,3,2,0},
    			{0,0,0,5,3,0,0,2},
    			{0,0,7,0,2,0,0,3},
    			{0,0,0,0,0,2,3,0}};
       	double[][]  MainGraph2={
       			{0,4,2,0,0,0,0,0},
    			{4,0,0,2,3,0,0,0},
    			{2,0,0,0,5,0,7,0},
    			{0,2,0,0,0,5,0,0},
    			{0,3,5,0,0,3,2,0},
    			{0,0,0,5,3,0,0,2},
    			{0,0,7,0,2,0,0,3},
    			{0,0,0,0,0,2,3,0}};
       	
       	double[][]  MainGraph3={
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
    	

    	
    	double[] cons={1,3};
    	
    SAMCRA sam=new SAMCRA(MainGraph3,MainGraph3,cons,2,1000);
    //long startTime = System.nanoTime();
    sam.solve(1,15);
    //long endTime = System.nanoTime();
    //long duration_ant = (endTime - startTime);
   // System.out.println("time="+duration_ant/1000000);
    /*	 q_element s;
        LinkedList<q_element> linklist=new LinkedList<q_element>(); 
         s =new q_element();
        s.gray=true;
        s.score=0.522;
        s.parent_id=1;
        s.parent_id_index=1;
linklist.add(s);
q_element q =new q_element();
q.gray=true;
q.score=220.522;
q.parent_id=1;
q.parent_id_index=1;
linklist.add(q);
s =new q_element();
s.gray=true;
s.score=66;
s.parent_id=1;
s.parent_id_index=1;
linklist.add(s);
System.out.println(linklist.get(0).score+";;;;;"+linklist.get(1).score+";;"+linklist.get(2).score+"--"+linklist.size()+";;"+linklist);*/
    	
    	
    }
}