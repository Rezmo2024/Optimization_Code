import org.gnu.glpk.GLPK;
import org.gnu.glpk.GLPKConstants;
import org.gnu.glpk.SWIGTYPE_p_double;
import org.gnu.glpk.SWIGTYPE_p_int;
import org.gnu.glpk.glp_prob;
import org.gnu.glpk.glp_iocp;

public class CSP {
//    Maximize z =  17 * x1 + 12* x2
//    subject to
//      10 x1 + 7 x2 <= 40
//         x1 +   x2 <=  5
//    where,
//      0.0 <= x1  integer
//      0.0 <= x2  integer
	
	int DELAY_THRESH=0;
	double[][] Node_Matrix;
    double[][] Delay_Matrix;
    double INFINITY=99999999;
    int Variable_Count=0;
    int x[][];
    boolean findpath=false;
    int source=0, destination=0;
    public CSP(double[][] mat,double[][] del,int dt,int src,int dst)
    {
    	DELAY_THRESH=dt;
    	Node_Matrix=Init_Node_Matrix(mat);
    	Delay_Matrix=Init_Delay_Matrix(del);
    	Variable_Count=mat.length;
    	source=src-1;//begins from 0
    	destination=dst-1;
    }
    public void Solve()
    {
    	glp_prob lp;
        glp_iocp iocp;
        SWIGTYPE_p_int ind;
        SWIGTYPE_p_double val;
        int ret;
        findpath=false;
    //  Create problem    
        lp = GLPK.glp_create_prob();
        System.out.println("Problem created");
        GLPK.glp_set_prob_name(lp, "CSP_PROBLEM");
        x=new int [Variable_Count][];
        //define variables
    	for(int i=0; i<Variable_Count; i++)
    	{
    		x[i]=new int[Variable_Count];
    		for(int j=0; j<Variable_Count; j++)
    //			if(Node_Matrix[i][j]==INFINITY)
    	//			x[i][j]=0;
    	//			else
    				{
    					x[i][j] = GLPK.glp_add_cols(lp, 1);
                        String name = "x[" + i + "," + j + "]";
                        GLPK.glp_set_col_name(lp, x[i][j], name);
                       // System.out.println(name+"="+x[i][j]);
                        GLPK.glp_set_col_kind(lp, x[i][j], GLPKConstants.GLP_BV);                       
                       // GLPK.glp_set_col_bnds(lp, 2, GLPKConstants.GLP_LO, 0,0);//lower bound is 0
                    
    				}			
         }
    	
    	//define Constraints
          // the number of decision variables is n*n
    	int n=Variable_Count*Variable_Count;
        ind = GLPK.new_intArray(n);
        val = GLPK.new_doubleArray(n);
        int row=0;
        int  k=0;

         GLPK.glp_add_rows(lp,1);
         row=1;
        GLPK.glp_set_row_name(lp, row, "delay_constraint");
        GLPK.glp_set_row_bnds(lp, row, GLPKConstants.GLP_UP, 0, DELAY_THRESH);
        for (int i = 0; i < Variable_Count; i++) 
        {
                for (int j = 0; j <Variable_Count; j++)
                {
                	if(i!=j)
                	{
                		k++;
		                GLPK.intArray_setitem(ind, k, x[i][j]);
		                GLPK.doubleArray_setitem(val, k, Delay_Matrix[i][j]);
                	}
                }
        }
        GLPK.glp_set_mat_row(lp, row, k, ind, val);
        
        //source constraint
        k=0;
 

        
        for(int p=0; p<Variable_Count; p++)
        {
        	if(p==source && source!=destination)
        	{
        		row=GLPK.glp_add_rows(lp,1);
                GLPK.glp_set_row_name(lp, row, "source_constraint"+String.valueOf(p));
                GLPK.glp_set_row_bnds(lp, row, GLPKConstants.GLP_FX, 1, 1);
                for (int j = 0; j <Variable_Count; j++)
			       {
			       	if(p!=j)
			       	{
			       		k++;
			               GLPK.intArray_setitem(ind, k, x[p][j]);
			               GLPK.doubleArray_setitem(val, k, 1);
			       	}
			       }
                for (int j = 0; j <Variable_Count; j++)
			       {
			       	if(p!=j)
			       	{
			       		k++;
			               GLPK.intArray_setitem(ind, k, x[j][p]);
			               GLPK.doubleArray_setitem(val, k, -1);
			       	}
			       }
			       GLPK.glp_set_mat_row(lp, row, k, ind, val);
        	}
        }
        
        
       
       //other intermediate nodes constraint
      
      int[][] y=new int[2][Variable_Count*Variable_Count]; //for preventing duplication
      for(int p=0; p<Variable_Count; p++)
      {
    	  k=0;
      	if(p!=source && source!=destination && p!=destination)
      	{
      		row=GLPK.glp_add_rows(lp,1);
              GLPK.glp_set_row_name(lp, row, "intermediate_constraint"+String.valueOf(p));
              GLPK.glp_set_row_bnds(lp, row, GLPKConstants.GLP_FX, 0,0);
              for (int j = 0; j <Variable_Count; j++)
			       {
			       	if(p!=j)
			       	{
			       		k++;
			               GLPK.intArray_setitem(ind, k, x[p][j]);
			               GLPK.doubleArray_setitem(val, k, 1);
			               y[0][k]=p;
			               y[1][k]=j;
			       	}
			       }
              
              for (int j = 0; j <Variable_Count; j++)
			       {
		            	 // boolean flag=false;
		            	//   for(int g=0; g<=h; g++)
		            		 //  if(y[0][g]==p && y[1][g]==j) {flag=true;System.out.println(p);};
		            	   
					       	if(p!=j )
					       	{
					       		k++;
					               GLPK.intArray_setitem(ind, k, x[j][p]);
					               GLPK.doubleArray_setitem(val, k, -1);
					       	}
			       }
			       GLPK.glp_set_mat_row(lp, row, k, ind, val);
      	}
      }
      
      
       
       GLPK.delete_intArray(ind);
        GLPK.delete_doubleArray(val);
        
        //objective function
        GLPK.glp_set_obj_name(lp, "CSP Objective");
        GLPK.glp_set_obj_dir(lp, GLPKConstants.GLP_MIN);
        for (int i = 0; i < Variable_Count; i++) 
        {
                for (int j = 0; j <Variable_Count; j++)
                {
                	if(i!=j)
                		 GLPK.glp_set_obj_coef(lp, x[i][j], Node_Matrix[i][j]);
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
        	findpath=false;
          System.out.println("The problemcould not be solved");
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

  /*public static void main(String[] arg)
  {
  }*/
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
    System.out.print(source+1+"->");
    int t=0;
    for(i=1; i <= n; i++)
    {
      name = GLPK.glp_get_col_name(lp, i);
      val  = GLPK.glp_mip_col_val(lp, i);
      if(val>0){
    	  String str=name.substring(name.indexOf(",")+1, name.indexOf("]"));
      System.out.print(+Integer.valueOf(str)+1+"->");
     //System.out.println(name);
      t++;

      }
    }
    if(t>1)findpath=true;
    else
    	findpath=false;
    /*for(i=1; i <= n; i++)
    {
      name = GLPK.glp_get_col_name(lp, i);
      val  = GLPK.glp_mip_col_val(lp, i);
      if(val>0){
      System.out.print(name);
      System.out.print(" = ");
      System.out.println(val);
      }1-->38-->7-->50-->25-->36-->
    }*/
  }
}

