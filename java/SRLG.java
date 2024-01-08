//import javax.print.attribute.standard.NumberOfDocuments;
import org.gnu.glpk.GLPK;
import org.gnu.glpk.GLPKConstants;
import org.gnu.glpk.SWIGTYPE_p_double;
import org.gnu.glpk.SWIGTYPE_p_int;
import org.gnu.glpk.glp_prob;
import org.gnu.glpk.glp_iocp;

public class SRLG {
	double[][] Node_Matrix;
    double INFINITY=99999999;
    int Variable_Count=0;
    int x[][][];
    int S[][][];
    int shr[][];
    int[] first_path;
    int[] second_path;
    int first_path_len=0, second_path_len=0;
    boolean findpath=false;
    int source=0, destination=0,numpaths=0, numgroups=0;
    public SRLG(double[][] mat,int[][] shared,int src,int dst, int K, int G)
    {
    	Node_Matrix=Init_Node_Matrix(mat);
    	Variable_Count=mat.length;
    	source=src-1;//begins from 0
    	destination=dst-1;
    	numpaths=K; // number of disjoint paths
    	numgroups=G;    	
    	shr=shared;
    	first_path=new int[mat.length];
    	second_path=new int[mat.length];
    }
    public void Solve()
    {
    	glp_prob lp;
        glp_iocp iocp;
        SWIGTYPE_p_int ind;
        SWIGTYPE_p_double val;
        int ret;
    //  Create problem    
        lp = GLPK.glp_create_prob();
        System.out.println("Problem created");
        GLPK.glp_set_prob_name(lp, "SRLG_PROBLEM");
        x=new int [Variable_Count][][];
        //define variables
    	for(int i=0; i<Variable_Count; i++)
    	{    	
    		x[i]=new int[Variable_Count][numpaths];
    		for(int j=0; j<Variable_Count; j++)
    		{
    			x[i][j]=new int[numpaths+1];
    			for(int k=1; k<=numpaths; k++)
        		{
    				if(i!=j)
	    			{
			    			x[i][j][k] = GLPK.glp_add_cols(lp, 1);
			    			String name1 = "x[" + i + "," + j +","+k+ "]";
			    			GLPK.glp_set_col_name(lp, x[i][j][k], name1);
			    			 GLPK.glp_set_col_kind(lp, x[i][j][k], GLPKConstants.GLP_BV);  
	    			}
        		}
    		}			
         }
    /*	S=new int[Variable_Count][][];
    	for(int i=0; i<Variable_Count; i++)
    	{    	
    		S[i]=new int[Variable_Count][numgroups];
    		for(int j=0; j<Variable_Count; j++)
    		{
    			S[i][j]=new int[numgroups+1];
    			for(int g=1; g<=numgroups; g++)
        		{
    				if(i!=j)
	    			{
			    			S[i][j][g] = GLPK.glp_add_cols(lp, 1);
			    			String name1 = "S[" + i + "," + j +","+g+ "]";
			    			GLPK.glp_set_col_name(lp, S[i][j][g], name1);
			    			 GLPK.glp_set_col_kind(lp, S[i][j][g], GLPKConstants.GLP_BV);  
	    			}
        		}
    		}			
         }*/
		S=new int[Variable_Count][Variable_Count][numgroups+1];
    	for(int i=0; i<Variable_Count; i++)
    		for(int j=0; j<Variable_Count; j++)
    			for(int g=1; g<=numgroups; g++)
    				S[i][j][g]=0;
    	
    	
    	for(int i=0;i<shr.length; i++)
    			for(int g=1;g<=numgroups; g++)
    			{
    				S[shr[i][0]][shr[i][1]][g]=1;
    				//System.out.println("S["+shr[i][0]+","+shr[i][1]+","+g+"]");
    			}
    	//define Constraints
          // the number of decision variables is n*n
    	int n=Variable_Count*Variable_Count;
        ind = GLPK.new_intArray(n);
        val = GLPK.new_doubleArray(n);
        int row=0;
   //   source constraint
		int m=0;       
		
        for(int k=1; k<=numpaths; k++)
        {
	        	m=0;
	        	row=GLPK.glp_add_rows(lp,1);
	            GLPK.glp_set_row_name(lp, row, "source_constraint"+String.valueOf(k));
	            GLPK.glp_set_row_bnds(lp, row, GLPKConstants.GLP_FX, 1, 1);
	        for (int j = 0; j <Variable_Count; j++)
		       {
	        	if(j!=source){
		       	
		       		m++;
		               GLPK.intArray_setitem(ind, m, x[source][j][k]);
		               GLPK.doubleArray_setitem(val, m, 1);
	        	}
		       	}
		       
	        
	        for (int j = 0; j <Variable_Count; j++)
	        {
	        	if(j!=source ){
		       		m++;
		               GLPK.intArray_setitem(ind, m, x[j][source][k]);
		               GLPK.doubleArray_setitem(val, m, -1);
	        	}
		       	}
		       
		       GLPK.glp_set_mat_row(lp, row, m, ind, val);
        }
        
        //Internal constraints
        for(int i=0; i<Variable_Count; i++)
        {
		        for(int k=1; k<=numpaths; k++)
		        {
			     if(i!=source && source!=destination && i!=destination)
			     {
		        	    m=0;
			        	row=GLPK.glp_add_rows(lp,1);
			            GLPK.glp_set_row_name(lp, row, "Internal_constraint"+String.valueOf(k));
			            GLPK.glp_set_row_bnds(lp, row, GLPKConstants.GLP_FX, 0, 0);
				        for (int j = 0; j <Variable_Count; j++)
					       {
					        	if(j!=i)
					        	{
						       	
						       		m++;
						               GLPK.intArray_setitem(ind, m, x[i][j][k]);
						               GLPK.doubleArray_setitem(val, m, 1);
					        	}
					       	}
					       
				        
				        for (int j = 0; j <Variable_Count; j++)
				        {
				        	if(j!=i)
				        	{
					       		m++;
					               GLPK.intArray_setitem(ind, m, x[j][i][k]);
					               GLPK.doubleArray_setitem(val, m, -1);
				        	}
					     
				        }
					       
					       GLPK.glp_set_mat_row(lp, row, m, ind, val);
			        }
		        }
        }
		        
// DSJ constraints

        for(int i=0; i<Variable_Count; i++)
        {
        	for(int j=0; j<Variable_Count; j++)
        	{
        		for(int k1=1; k1<=numpaths; k1++)
        		{
        			for(int k2=1; k2<=numpaths; k2++)
        			{
        				if(k1!=k2 && i!=j)
        				{
        				   	row=GLPK.glp_add_rows(lp,1);
    			            GLPK.glp_set_row_name(lp, row, "DSJ_constraint"+String.valueOf(k1));
    			            GLPK.glp_set_row_bnds(lp, row, GLPKConstants.GLP_UP, 0, 1);
    			            GLPK.intArray_setitem(ind, 1, x[i][j][k1]);
				            GLPK.doubleArray_setitem(val, 1, 1);
				            GLPK.intArray_setitem(ind, 2, x[i][j][k2]);
				            GLPK.doubleArray_setitem(val, 2, 1);
						    GLPK.glp_set_mat_row(lp, row, 2, ind, val);
        				}
        			}
        		}
        	}
        }
        
        
        // SRL_DSJ constraint

        for(int i1=0; i1<Variable_Count; i1++)
        {
        	for(int j1=0; j1<Variable_Count; j1++)
        	{
                for(int i2=0; i2<Variable_Count; i2++)
                {
                	for(int j2=0; j2<Variable_Count; j2++)
                	{
                		for(int g=1; g<=numgroups; g++)
                		{
                			for(int k1=1; k1<=numpaths; k1++)
			        		{
			        			for(int k2=1; k2<=numpaths; k2++)
			        			{
			        				if(k1!=k2  && ((S[i1][j1][g]+ S[i2][j2][g])==2 && i1!=i2) && i1!=j1 && i2!=j2)
			        				{
			        				   	row=GLPK.glp_add_rows(lp,1);
			    			            GLPK.glp_set_row_name(lp, row, "SRLG_DSJ_constraint"+String.valueOf(k1));
			    			            GLPK.glp_set_row_bnds(lp, row, GLPKConstants.GLP_UP, 0, 1);
			    			            GLPK.intArray_setitem(ind, 1, x[i1][j1][k1]);
							            GLPK.doubleArray_setitem(val, 1, 1);
							            GLPK.intArray_setitem(ind, 2, x[i2][j2][k2]);
							            GLPK.doubleArray_setitem(val, 2, 1);
					    				System.out.println(S[i1][j1][g]+"   "+i1+"   "+j1);
					    				System.out.println(S[i2][j2][g]+"   "+i2+"   "+j2);

									    GLPK.glp_set_mat_row(lp, row, 2, ind, val);
			        				}
			        			}
			        		}
                		}
                	}
                }
        	}
        }
        
        GLPK.delete_intArray(ind);
        GLPK.delete_doubleArray(val);
        
        //objective function
        GLPK.glp_set_obj_name(lp, "SRLG Objective");
        GLPK.glp_set_obj_dir(lp, GLPKConstants.GLP_MIN);
        for (int i = 0; i < Variable_Count; i++) 
        {
                for (int j = 0; j <Variable_Count; j++)
                {
                	for(int k=1; k<=numpaths; k++)
                	{
	                	if(i!=j)
	                		 GLPK.glp_set_obj_coef(lp, x[i][j][k], Node_Matrix[i][j]);
                	}
                }
        }
        
        
    //  solve model
        iocp = new glp_iocp();
        GLPK.glp_init_iocp(iocp);
        iocp.setPresolve(GLPKConstants.GLP_ON);
        GLPK.glp_write_lp(lp, null, "yi.lp");//copy model formula to file
        ret = GLPK.glp_intopt(lp, iocp);
    //  Retrieve solution
        if (ret == 0) {
        	findpath=true;
          write_mip_solution(lp);
        }
        else {
          System.out.println("The problem could not be solved");
        };
        
        // free memory
        GLPK.glp_delete_prob(lp);
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
             }
            }
            return Node_Matrix;
    }
  /**
   * write integer solution
   * @param mip problem
   */
  public void write_mip_solution(glp_prob lp)
  {
    int i;
    int n;
    String name;
    double val;
    name = GLPK.glp_get_obj_name(lp);
    val  = GLPK.glp_mip_obj_val(lp);
    System.out.print(name);
    System.out.print(" = ");
    System.out.println(val);
    n = GLPK.glp_get_num_cols(lp);
    int k=0;
    
    for(i=1; i <= n; i++)
    {
      name = GLPK.glp_get_col_name(lp, i);
      val  = GLPK.glp_mip_col_val(lp, i);
      if(val>0){
    	  String str1=name.substring(name.lastIndexOf(",")+1,name.indexOf("]"));
     	 // System.out.print(str1+"  ");
     	  if(Integer.valueOf(str1)==1)//first path
      
      {k++;}
    }
    }
      
    int[][] temp_path1=new int[2][k];
    int j=0;
    for(i=1; i <= n; i++)
    {
      name = GLPK.glp_get_col_name(lp, i);
      val  = GLPK.glp_mip_col_val(lp, i);
      if(val>0)
      {
    	  String str1=name.substring(name.lastIndexOf(",")+1,name.indexOf("]"));
    	 // System.out.print(str1+"  ");
    	  if(Integer.valueOf(str1)==1)//first path
    	  {
    		  System.out.print(name+"   ");
    		  temp_path1[0][j]=Integer.valueOf(name.substring(name.indexOf("[")+1, name.indexOf(",")));
    		  temp_path1[1][j]=Integer.valueOf(name.substring(name.indexOf(",")+1, name.lastIndexOf(",")));
    		  j++;
    	  }
      }
    }
    System.out.println();

    first_path=make_path(temp_path1,j,source,destination);
    first_path_len=j;
    System.out.println();
    k=0;
    
    for(i=1; i <= n; i++)
    {
      name = GLPK.glp_get_col_name(lp, i);
      val  = GLPK.glp_mip_col_val(lp, i);
      if(val>0){
    	  String str1=name.substring(name.lastIndexOf(",")+1,name.indexOf("]"));
     	 // System.out.print(str1+"  ");
     	  if(Integer.valueOf(str1)==2)//second path
      
      {k++;}
    }
    }
      
    int[][] temp_path2=new int[2][k];
    j=0;
    for(i=1; i <= n; i++)
    {
      name = GLPK.glp_get_col_name(lp, i);
      val  = GLPK.glp_mip_col_val(lp, i);
      if(val>0)
      {
    	  String str1=name.substring(name.lastIndexOf(",")+1,name.indexOf("]"));
    	 // System.out.print(str1+"  ");
    	  if(Integer.valueOf(str1)==2)//second path
    	  {
    		  System.out.print(name+"   ");
    		  temp_path2[0][j]=Integer.valueOf(name.substring(name.indexOf("[")+1, name.indexOf(",")));
    		  temp_path2[1][j]=Integer.valueOf(name.substring(name.indexOf(",")+1, name.lastIndexOf(",")));
    		  j++;
    	  }
      }
    }
    System.out.println();

    second_path=make_path(temp_path2,j,source,destination);
    second_path_len=j;
    System.out.println();
  }
  public int[] make_path(int[][] path_matrix, int len,int src, int dst)
  {
	  int[] path=new int[len+1];
	  int index=src;
	  int c=0;
	  
	  path[c++]=index;
	  for(int i=0; i<len; i++)
	  for(int j=0; j<len; j++)
		  if(path_matrix[0][j]==index)
		  { 
			  index=path_matrix[1][j];
			  path[c++]=index;
			  //System.out.print(index+"-");
			  break;
		 }
	  
	  
	 /* for(int i=0; i<c; i++)
		  System.out.print(path[i]+" ");*/
	  return path;  
  }
}

