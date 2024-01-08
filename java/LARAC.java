public class LARAC {
	double[][] node_mat;
	double[][]  del_mat;
	double [][]  c_lambda;

	int thresh=0;
	int[] bestpath;
	int bestpath_len=0;
	int iteration=0;
	public LARAC(double[][] mat,double[][] del, int th, int maxtry)
	{
		node_mat=mat;
		del_mat=mat;
		thresh=th;
		iteration=maxtry;
	}
	public boolean solve(int src,int dst)
	{
		int[] rc;
		int[] rd;
		int[] r;
		int rclen=0;
		Dijkstra dij=new Dijkstra();
		dij.solve(node_mat, src, dst);
		rc=dij.bestpath;
		rclen=dij.pathlenght;
		if(fd(rc, dij.pathlenght)<=thresh)
		{
			bestpath=rc;
			bestpath_len=dij.pathlenght;
			return true;
		}
		else
		{
			dij.solve(del_mat, src, dst);
			rd=dij.bestpath;
			if(fd(rd, dij.pathlenght)>thresh) 
				return false;//no feasible solution
			else
			{
				int h=0;
				while(h<=iteration)
				{
					h++;
					double lambda=(fc(rc, dij.pathlenght)-fc(rd, dij.pathlenght))/(fd(rd, dij.pathlenght)-fd(rc, dij.pathlenght));
					for(int i=0; i<node_mat.length; i++)
						for(int j=0; j<del_mat.length; j++)
							c_lambda[i][j]=node_mat[i][j]+lambda*del_mat[i][j];
					
					dij.solve(c_lambda, 1, 15);
					r=dij.bestpath;
					if(flambda(r, dij.pathlenght)==flambda(rc, dij.pathlenght))
					{
						bestpath=rd;
					    bestpath_len=dij.pathlenght;
					    return true;
					}
					else if(fd(rc,rclen)<=thresh)
						rd=r;
					else
						rc=r;
				}
				return false;
			}
			
				
		}		
	       
	}
	public double fc(int[] p, int l_index)
    {
           double cost=0.0;
           for(int i=0; i<=l_index; i++)
                    cost+=node_mat[p[i]][p[i+1]];
           return cost;
     }
	public double fd(int[] p, int l_index)
    {
           double cost=0.0;
           for(int i=0; i<=l_index; i++)
                    cost+=del_mat[p[i]][p[i+1]];
           return cost;
     }
	public double flambda(int[] p, int l_index)
    {
           double cost=0.0;
           for(int i=0; i<=l_index; i++)
                    cost+=c_lambda[p[i]][p[i+1]];
           return cost;
     }
}