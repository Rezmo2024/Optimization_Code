import generic.Input;
import generic.Output;
import generic.Tuple;
//import intervalType2.sets.IntervalT2MF_Gauangle;
//import intervalType2.sets.IntervalT2MF_Gaussian;
//import generalType2zSlices.*;
//import intervalType2.sets.IntervalT2MF_Interface;
import intervalType2.sets.IntervalT2MF_Triangular;
import intervalType2.system.IT2_Antecedent;
import intervalType2.system.IT2_Consequent;
import intervalType2.system.IT2_Rule;
import intervalType2.system.IT2_Rulebase;
import java.util.TreeMap;
//import type1.sets.T1MF_Gauangle;
//import type1.sets.T1MF_Gaussian;
import type1.sets.T1MF_Triangular;

public class FuzzyT2
{

    double Max_Delay,Max_BW;
    int delay_sensitive=1;
    int bw_sensitive=10;
       Input delay,bw;
       Output cost;
       IT2_Rulebase rulebase;
    public FuzzyT2(double Max_delay, double Max_bw, int dls,int bws)
    {
           Max_Delay=Max_delay;
           Max_BW=Max_bw;
           delay_sensitive=dls;
           bw_sensitive=bws;
    }
    public double Get_Cost(int del, double bandwidth)
    {
           double result=0.0;
        //Define the inputs
        delay = new Input("Delay", new Tuple(0,Max_Delay));
        bw = new Input("BandWidth", new Tuple(0,Max_BW));
        cost = new Output("Cost", new Tuple(0,100));
        T1MF_Triangular lowdelayUMF = new T1MF_Triangular("Upper MF for Low Delay",0.0, 0, (Max_Delay/2)+delay_sensitive);
        T1MF_Triangular lowdelayLMF = new T1MF_Triangular("Lower MF for Low Delay",0, 0, (Max_Delay/2)-delay_sensitive);
        IntervalT2MF_Triangular lowdelayMF = new IntervalT2MF_Triangular("IT2MF for Low Delay",lowdelayUMF,lowdelayLMF);
        T1MF_Triangular mediumdelayUMF = new T1MF_Triangular("Upper MF for Medium Delay",0.0, Max_Delay/2, Max_Delay);
        T1MF_Triangular mediumdelayLMF = new T1MF_Triangular("Lower MF for Medium Delay",delay_sensitive, Max_Delay/2, Max_Delay-delay_sensitive);
        IntervalT2MF_Triangular mediumdelayMF = new IntervalT2MF_Triangular("IT2MF for Medium Delay",mediumdelayUMF,mediumdelayLMF);
        T1MF_Triangular highdelayUMF = new T1MF_Triangular("Upper MF for High Delay",(Max_Delay/2)-delay_sensitive, Max_Delay, Max_Delay);
        T1MF_Triangular highdelayLMF = new T1MF_Triangular("Lower MF for High Delay",(Max_Delay/2)+delay_sensitive, Max_Delay,Max_Delay);
        IntervalT2MF_Triangular highdelayMF = new IntervalT2MF_Triangular("IT2MF for High Delay",highdelayUMF,highdelayLMF);
        T1MF_Triangular lowbwUMF = new T1MF_Triangular("Upper MF for Low bw",0.0, 0, (Max_BW/2)+bw_sensitive);
        T1MF_Triangular lowbwLMF = new T1MF_Triangular("Lower MF for Low bw",0, 0, (Max_BW/2)-bw_sensitive);
        IntervalT2MF_Triangular lowbwMF = new IntervalT2MF_Triangular("IT2MF for Low bw",lowbwUMF,lowbwLMF);
        T1MF_Triangular mediumbwUMF = new T1MF_Triangular("Upper MF for Medium bw",0.0, Max_BW/2, Max_BW);
        T1MF_Triangular mediumbwLMF = new T1MF_Triangular("Lower MF for Medium bw",bw_sensitive, Max_BW/2, Max_BW-bw_sensitive);
        IntervalT2MF_Triangular mediumbwMF = new IntervalT2MF_Triangular("IT2MF for Medium bw",mediumbwUMF,mediumbwLMF);
        T1MF_Triangular highbwUMF = new T1MF_Triangular("Upper MF for High bw",(Max_BW/2)-bw_sensitive, Max_BW,Max_BW);
        T1MF_Triangular highbwLMF = new T1MF_Triangular("Lower MF for High bw",(Max_BW/2)+bw_sensitive, Max_BW,Max_BW);
        IntervalT2MF_Triangular highbwMF = new IntervalT2MF_Triangular("IT2MF for High bw",highbwUMF,highbwLMF);
        T1MF_Triangular excellentcostUMF = new T1MF_Triangular("Upper MF for Excellent Cost",0.0, 0, 41);
        T1MF_Triangular excellentcostLMF = new T1MF_Triangular("Lower MF for Excellent Cost",0, 0, 39);
        IntervalT2MF_Triangular excllentcostMF = new IntervalT2MF_Triangular("IT2MF for Excellent Cost",excellentcostUMF,excellentcostLMF);
        T1MF_Triangular goodcostUMF = new T1MF_Triangular("Upper MF for good Cost",39, 48, 56);
        T1MF_Triangular goodcostLMF = new T1MF_Triangular("Lower MF for good Cost",41, 48, 54);
        IntervalT2MF_Triangular goodcostMF = new IntervalT2MF_Triangular("IT2MF for good Cost",goodcostUMF,goodcostLMF);
        T1MF_Triangular faircostUMF = new T1MF_Triangular("Upper MF for fair Cost",47, 55, 70);
        T1MF_Triangular faircostLMF = new T1MF_Triangular("Lower MF for fair Cost",49, 55, 68);
        IntervalT2MF_Triangular faircostMF = new IntervalT2MF_Triangular("IT2MF for fair Cost",faircostUMF,faircostLMF);
        T1MF_Triangular poorcostUMF = new T1MF_Triangular("Upper MF for poor Cost",54, 69, 80);
        T1MF_Triangular poorcostLMF = new T1MF_Triangular("Lower MF for poor Cost",56, 69, 78);
        IntervalT2MF_Triangular poorcostMF = new IntervalT2MF_Triangular("IT2MF for poor Cost",poorcostUMF,poorcostLMF);
        T1MF_Triangular badcostUMF = new T1MF_Triangular("Upper MF for bad Cost",79, 100, 100);
        T1MF_Triangular badcostLMF = new T1MF_Triangular("Lower MF for bad Cost",81, 100, 100);
        IntervalT2MF_Triangular badcostMF = new IntervalT2MF_Triangular("IT2MF for bad Cost",badcostUMF,badcostLMF);
        //Set up the antecedents and consequents - note how the inputs are associated...
        IT2_Antecedent lowdelay = new IT2_Antecedent("Low_DELAY", lowdelayMF, delay);
        IT2_Antecedent mediumdelay = new IT2_Antecedent("Medium_DELAY", mediumdelayMF, delay);
        IT2_Antecedent highdelay = new IT2_Antecedent("High_DELAY", highdelayMF, delay);
        IT2_Antecedent lowbw = new IT2_Antecedent("Low_bw", lowbwMF, bw);
        IT2_Antecedent mediumbw = new IT2_Antecedent("Medium_bw", mediumbwMF, bw);
        IT2_Antecedent highbw = new IT2_Antecedent("High_bw", highbwMF, bw);
        IT2_Consequent excellentcost = new IT2_Consequent("Excellent_Cost", excllentcostMF, cost);
        IT2_Consequent goodcost = new IT2_Consequent("Good_Cost", goodcostMF, cost);
        IT2_Consequent faircost = new IT2_Consequent("Fair_Cost", faircostMF, cost);
        IT2_Consequent poorcost = new IT2_Consequent("Poor_Cost", poorcostMF, cost);
        IT2_Consequent badcost = new IT2_Consequent("Bad_Cost", badcostMF, cost);
        //Set up the rulebase and add rules
        rulebase = new IT2_Rulebase(9);
        rulebase.addRule(new IT2_Rule(new IT2_Antecedent[]{lowdelay, highbw}, excellentcost));
        rulebase.addRule(new IT2_Rule(new IT2_Antecedent[]{lowdelay, mediumbw}, goodcost));
        rulebase.addRule(new IT2_Rule(new IT2_Antecedent[]{lowdelay, lowbw}, poorcost));
        rulebase.addRule(new IT2_Rule(new IT2_Antecedent[]{mediumdelay, highbw}, goodcost));
        rulebase.addRule(new IT2_Rule(new IT2_Antecedent[]{mediumdelay, mediumbw}, faircost));
        rulebase.addRule(new IT2_Rule(new IT2_Antecedent[]{mediumdelay, lowbw}, poorcost));
        rulebase.addRule(new IT2_Rule(new IT2_Antecedent[]{highdelay, highbw}, poorcost));
        rulebase.addRule(new IT2_Rule(new IT2_Antecedent[]{highdelay, mediumbw}, poorcost));
        rulebase.addRule(new IT2_Rule(new IT2_Antecedent[]{highdelay, lowbw},badcost));
        delay.setInput(del);
        bw.setInput(bandwidth);
        if((delay.getInput()==0) || ( bw.getInput()==0))
        {
          //This means the input variables are out of range
           result=9999;
           //System.out.println("The delay was: "+delay.getInput()+"   "+del);
           //System.out.println("The bw was: "+bw.getInput()+"   "+bandwidth);
           return result;
        }
      /*  System.out.println("The delay was: "+delay.getInput());
        System.out.println("The bw was: "+bw.getInput());
        System.out.println("Using center of sets type reduction, the IT2 FLS recommends a "
                + "cost of: "+rulebase.evaluate(0).get(cost));
        System.out.println("Using centroid type reduction, the IT2 FLS recommends a "
                + "cost of: "+rulebase.evaluate(1).get(cost));
        */
        result=rulebase.evaluate(0).get(cost);
        //show the output of the raw centroids
       // System.out.println("Centroid of the output for Cost (based on centroid type reduction):");
        TreeMap<Output, Object[]> centroid = rulebase.evaluateGetCentroid(1);
        Object[] centroidTip = centroid.get(cost);
        Tuple centroidTipXValues = (Tuple)centroidTip[0];
        double centroidTipYValues = ((Double)centroidTip[1]);
         //   System.out.println(centroidTipXValues+" at y= "+centroidTipYValues);
        //print out the rules
       // System.out.println("\n"+rulebase);
       // System.out.println("Result for del="+del+" and bw="+bandwidth+" is ="+result);
        result=Math.round(result);
        return result;
    }
}
