/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */


import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author REZMO
 */
public class GLPK_IN_JAVA {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        try {
            // TODO code application logic here
            Runtime rt = Runtime.getRuntime();
            Process pr = rt.exec("G:\\SEMESTER5\\THESIS\\Problems\\glpk-4.57\\w64\\glpsol -m G:\\SEMESTER5\\THESIS\\Problems\\SRLG.ALG -d G:\\SEMESTER5\\THESIS\\Problems\\SRLG.DATA -o G:\\SEMESTER5\\THESIS\\Problems\\SRLG.out");
            System.out.println("It was run OK");
        } catch (IOException ex) {
            Logger.getLogger(GLPK_IN_JAVA.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

}
