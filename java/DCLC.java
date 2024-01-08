//import javax.print.attribute.standard.NumberOfDocuments;
import org.gnu.glpk.GLPK;
import org.gnu.glpk.GLPKConstants;
import org.gnu.glpk.SWIGTYPE_p_double;
import org.gnu.glpk.SWIGTYPE_p_int;
import org.gnu.glpk.glp_prob;
import org.gnu.glpk.glp_iocp;

public class DCLC {
	int DELAY_THRESH=0;
	double[][] Node_Matrix;
    double[][] Delay_Matrix;
    double INFINITY=99999999;
    int Variable_Count=0;
    int x[][][];
    int y[][][];
    int z[][];
    int source=0, destination=0,numdests=0;
    int[] destinations;
    public DCLC(double[][] mat,double[][] del,int dt,int src, int nds)
    {
    	DELAY_THRESH=dt;
    	Node_Matrix=Init_Node_Matrix(mat);
    	Delay_Matrix=Init_Delay_Matrix(del);
    	Variable_Count=mat.length;
    	source=src-1;//begins from 0
    	numdests=nds;
    	destinations=new int[numdests];
    	//destinations=dests;
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
        GLPK.glp_set_prob_name(lp, "DCLC_PROBLEM");
        x=new int [Variable_Count][][];
        y=new int [Variable_Count][][];
        z=new int[Variable_Count][];
        //define variables
    	for(int i=0; i<Variable_Count; i++)
    	{
    		z[i]=new int[Variable_Count];
    		for(int j=0; j<Variable_Count; j++)
		    		{
		    			if(i!=j)
		    			{
				    			z[i][j]=GLPK.glp_add_cols(lp, 1);
				    			String name1 = "z[" + i + "," + j + "]";
				    			GLPK.glp_set_col_name(lp, z[i][j], name1);
				    			GLPK.glp_set_col_kind(lp, z[i][j], GLPKConstants.GLP_BV);  
		    			}
		    		}
    	}
    	
     	for(int i=0; i<Variable_Count; i++)
    	{    	
    		x[i]=new int[Variable_Count][numdests];
    		for(int j=0; j<Variable_Count; j++)
    		{
    			x[i][j]=new int[numdests+1];
    			for(int k=1; k<=numdests; k++)
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
     	for(int i=0; i<Variable_Count; i++)
    	{    	
    		y[i]=new int[Variable_Count][numdests];
    		for(int j=0; j<Variable_Count; j++)
    		{
    			y[i][j]=new int[numdests+1];
    			for(int k=1; k<=numdests; k++)
        		{
    				if(i!=j)
	    			{
			    			y[i][j][k] = GLPK.glp_add_cols(lp, 1);
			    			String name2 = "y[" + i + "," + j +","+k+ "]";
			    			GLPK.glp_set_col_name(lp, y[i][j][k], name2);
			    			 GLPK.glp_set_col_kind(lp, y[i][j][k], GLPKConstants.GLP_BV);
	    			}
        		}
    		}			
         }
    
    	//define Constraints
          // the number of decision variables is n*n
    	int n=Variable_Count*Variable_Count;
        ind = GLPK.new_intArray(n);
        val = GLPK.new_doubleArray(n);
        int row=0;
        for (int i = 0; i < Variable_Count; i++) 
        {
                for (int j = 0; j <Variable_Count; j++)
                {
                	for(int k=1; k<=numdests; k++)
                	{
                		if(i!=j)
		    			{
	                		  GLPK.glp_add_rows(lp,1);
	                	         row++;
	                	        GLPK.glp_set_row_name(lp, row, "Xconstraint"+row);
	                	        GLPK.glp_set_row_bnds(lp, row, GLPKConstants.GLP_UP, 0, 0);
			                GLPK.intArray_setitem(ind, 1,x[i][j][k]);
			                GLPK.doubleArray_setitem(val, 1, 1);
			                GLPK.intArray_setitem(ind, 2,y[i][j][k] );
			                GLPK.doubleArray_setitem(val, 2, -numdests);
			                GLPK.glp_set_mat_row(lp, row,2, ind, val);
			    		}

                	}
                }
        }
        
        for (int i = 0; i < Variable_Count; i++) 
        {
                for (int j = 0; j <Variable_Count; j++)
                {
                	for(int k=1; k<=numdests; k++)
                	{
                		if(i!=j)
		    			{
	                		  GLPK.glp_add_rows(lp,1);
	                	         row++;
	                	        GLPK.glp_set_row_name(lp, row, "Zconstraint"+row);
	                	        GLPK.glp_set_row_bnds(lp, row, GLPKConstants.GLP_UP, 0, 0);
				                GLPK.intArray_setitem(ind, 1,x[i][j][k]);
				                GLPK.doubleArray_setitem(val, 1, 1);
				                GLPK.intArray_setitem(ind, 2,z[i][j] );
				                GLPK.doubleArray_setitem(val, 2, -numdests);
				                GLPK.glp_set_mat_row(lp, row,2, ind, val);
			    		}

                	}
                }
        }
        
   //   source constraint
		int m=0;       
		
        for(int k=1; k<=numdests; k++)
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

        //   destinations constraint
             
     		 m=0;       
     		for(int a=1; a<=numdests; a++)
     		{
     				for(int i=0; i< Variable_Count; i++)
     				{	
     					for(int k=1; k<=numdests; k++)
     			        {
     						
     			        	if(i!=source && i!=a && a!=source && k==a)
     			        	{
     			        		row=GLPK.glp_add_rows(lp,1);
     				            GLPK.glp_set_row_name(lp, row, "destinations_constraint"+String.valueOf(k)+"_"+String.valueOf(i));
     				            GLPK.glp_set_row_bnds(lp, row, GLPKConstants.GLP_FX, 0,0);
     				       m=0;
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
     							        	if(j!=i )
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
     		}

     		//   Delay constraint
     			 m=0;       
     			for(int a=1; a<=numdests; a++)
     			{
     						for(int k=1; k<=numdests; k++)
     				        {
     							
     				        	if( k==a)
     				        	{
     				        		row=GLPK.glp_add_rows(lp,1);
     					            GLPK.glp_set_row_name(lp, row, "Delay_constraint"+String.valueOf(k));
     					            GLPK.glp_set_row_bnds(lp, row, GLPKConstants.GLP_UP, 0,DELAY_THRESH);
     					       m=0;
     					            for(int i=0; i<Variable_Count; i++)
     					            {
     					        	 for (int j = 0; j <Variable_Count; j++)
     						       {
     						        	if(j!=i)
     						        	{
       							       		m++;
     							               GLPK.intArray_setitem(ind, m, y[i][j][k]);
     							               GLPK.doubleArray_setitem(val, m, Delay_Matrix[i][j]);
     						        	}
     						       }
     					            }
     					       GLPK.glp_set_mat_row(lp, row, m, ind, val);
     					       }
     				        }
     				        }
       GLPK.delete_intArray(ind);
        GLPK.delete_doubleArray(val);
        
        //objective function
        GLPK.glp_set_obj_name(lp, "DCLC Objective");
        GLPK.glp_set_obj_dir(lp, GLPKConstants.GLP_MIN);
        for (int i = 0; i < Variable_Count; i++) 
        {
                for (int j = 0; j <Variable_Count; j++)
                {
                	if(i!=j)
                		 GLPK.glp_set_obj_coef(lp, z[i][j], Node_Matrix[i][j]);
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
    for(i=1; i <= n; i++)
    {
      name = GLPK.glp_get_col_name(lp, i);
      val  = GLPK.glp_mip_col_val(lp, i);
      if(val>0 && name.indexOf("z")>=0)
      {
    	  String str1=name.substring(2,name.indexOf(","));
    	  String str2=name.substring(name.indexOf(",")+1, name.indexOf("]"));
         System.out.print("("+(Integer.valueOf(str1)+1)+","+(Integer.valueOf(str2)+1)+")");
      }
    }
  }
}

