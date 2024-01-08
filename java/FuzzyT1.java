import generic.Input;
import generic.Output;
import generic.Tuple;
import type1.sets.T1MF_Triangular;
import type1.system.T1_Antecedent;
import type1.system.T1_Consequent;
import type1.system.T1_Rule;
import type1.system.T1_Rulebase;
public class FuzzyT1
{

    double Max_Delay,Max_BW;
	Input delay,bw;
	Output cost;
	T1_Rulebase rulebase;
    
    public FuzzyT1(double Max_delay, double Max_bw)
    {
    	Max_Delay=Max_delay;
    	Max_BW=Max_bw;
    }
    public double Get_Cost(double del, double bandwidth)
    {
    	double result=0.0;

        //Define the inputs
        delay = new Input("Delay", new Tuple(0,Max_Delay));
        bw = new Input("BandWidth", new Tuple(0,Max_BW));
        cost = new Output("Cost", new Tuple(0,100));               

        T1MF_Triangular lowdelay = new T1MF_Triangular(" MF for Low Delay",0.0, 0, Max_Delay/2);
        T1MF_Triangular mediumdelay = new T1MF_Triangular("MF for Medium Delay",0.0, Max_Delay/2, Max_Delay);
        T1MF_Triangular highdelay = new T1MF_Triangular("MF for High Delay",Max_Delay/2, Max_Delay, Max_Delay);
        
        T1MF_Triangular lowbw = new T1MF_Triangular("MF for Low bw",0.0, 0, Max_BW/2);
        T1MF_Triangular mediumbw = new T1MF_Triangular(" MF for Medium bw",0.0, Max_BW/2, Max_BW);
        T1MF_Triangular highbw = new T1MF_Triangular("MF for High bw",Max_BW/2, Max_BW,Max_BW);
        
        T1MF_Triangular excellentcost = new T1MF_Triangular(" MF for Excellent Cost",0.0, 0, 40);
        T1MF_Triangular goodcost = new T1MF_Triangular("MF for good Cost",40, 48, 55);
        T1MF_Triangular faircost= new T1MF_Triangular("MF for fair Cost",48, 55, 69);
        T1MF_Triangular poorcost = new T1MF_Triangular("MF for poor Cost",55, 69, 79);
        T1MF_Triangular badcost = new T1MF_Triangular("MF for bad Cost",80, 100, 100);
        
        
        //Set up the antecedents and consequents - note how the inputs are associated...
        T1_Antecedent ldelay = new T1_Antecedent("Low_DELAY", lowdelay, delay);
        T1_Antecedent mdelay = new T1_Antecedent("Med_DELAY", mediumdelay, delay);
        T1_Antecedent hdelay = new T1_Antecedent("High_DELAY", highdelay, delay);
        T1_Antecedent lbw = new T1_Antecedent("Low_bw", lowbw, bw);
        T1_Antecedent mbw = new T1_Antecedent("Medium_bw", mediumbw, bw);
        T1_Antecedent hbw = new T1_Antecedent("High_bw", highbw, bw);
    
        T1_Consequent excost = new T1_Consequent("Excellent_Cost", excellentcost, cost);
        T1_Consequent gcost = new T1_Consequent("Good_Cost", goodcost, cost);
        T1_Consequent fcost = new T1_Consequent("Fair_Cost", faircost, cost);
        T1_Consequent pcost = new T1_Consequent("Poor_Cost", poorcost, cost);
        T1_Consequent bcost = new T1_Consequent("Bad_Cost", badcost, cost);


        //Set up the rulebase and add rules
        rulebase = new T1_Rulebase(9);
        rulebase.addRule(new T1_Rule(new T1_Antecedent[]{ldelay, hbw}, excost));
        rulebase.addRule(new T1_Rule(new T1_Antecedent[]{ldelay, mbw}, gcost));
        rulebase.addRule(new T1_Rule(new T1_Antecedent[]{ldelay, lbw}, pcost));
        rulebase.addRule(new T1_Rule(new T1_Antecedent[]{mdelay, hbw}, gcost));
        rulebase.addRule(new T1_Rule(new T1_Antecedent[]{mdelay, mbw}, fcost));
        rulebase.addRule(new T1_Rule(new T1_Antecedent[]{mdelay, lbw}, pcost));
        rulebase.addRule(new T1_Rule(new T1_Antecedent[]{hdelay, hbw}, pcost));
        rulebase.addRule(new T1_Rule(new T1_Antecedent[]{hdelay, mbw}, pcost));
        rulebase.addRule(new T1_Rule(new T1_Antecedent[]{hdelay, lbw},bcost));
        delay.setInput(del);
        bw.setInput(bandwidth);
        result=rulebase.evaluate(0).get(cost);
        return result;
    }
    public static void main(String args[])
    {
       // System.out.print("hello");
        FuzzyT1 f=new FuzzyT1(200, 100);
        double res=f.Get_Cost(50, 20);
        System.out.println("Cost is "+res);
        
        
    }
}
