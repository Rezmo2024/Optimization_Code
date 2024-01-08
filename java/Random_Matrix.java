import java.util.Random;
public class Random_Matrix
{
	public Random_Matrix()
	{
		
	}
	public double[][] Create_Matrix(int size_mat, int low,int high)
	{
		double[][] rand_mat=new double[size_mat][size_mat];
                int w=1;
		for(int i=0; i<size_mat; i++)
			for(int j=i+1; j<size_mat; j++)
			{
				Random r=new Random();
				int result = r.nextInt(high-low) + low;
				rand_mat[i][j]=(double)result;
				rand_mat[j][i]=(double)result;
                                w++;
                                if(w%2==0)
                                {
                                    rand_mat[i][j]=0;
				rand_mat[j][i]=0;
                                }
			}
		return rand_mat;
		
	}
    public static void main(String args[])
    {
       // System.out.print("hello");
		double[][] rand_mat1=new double[5][5];
		Random_Matrix rm=new Random_Matrix();
		rand_mat1=rm.Create_Matrix(5, 10, 20);
		System.out.print("{");
		for(int i=0; i<5; i++){
			for(int j=0; j<5; j++){
				System.out.print(rand_mat1[i][j]+",");
			}
			System.out.print("},");
			System.out.println();
			System.out.print("{");
		}
    }
}