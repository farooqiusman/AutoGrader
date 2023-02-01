/*
SOLUTION BY JEREMIE BORNAIS
*/
/** 
 * DFA format:
      alphabet
      states
      start state
      final state(s)
      transition_1
      transition_2
      ...
      transition_n
      
Example DFA for RE (a|b)(a|b|0|1)* 
The diagram is

     a,b  a,b,0,1
    A-->B---->
         <----   
The dfa.txt is: 
      a b 0 1
      A B
      A
      B
      A a B
      A b B
      B a B
      B b B
      B 0 B
      B 1 B
        
 **/
import java.util.TreeMap;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.io.*;
import java.util.Scanner;

public class DFA {
	public static String [] alphabet;
	public String startState;
	public Set<String> finalStates;
	
    public static TreeMap<String, String> transitions=new TreeMap<String, String>();
       
    /** Construct a DFA from a text file
     */
    public DFA(String filename) throws Exception{  
        BufferedReader br  = new BufferedReader(new FileReader(filename));
        alphabet=br.readLine().trim().split(" ");
        String[] states=br.readLine().split(" ");
        startState=br.readLine().trim();
        String[] finals=br.readLine().trim().split(" ");
        finalStates= new HashSet<>(Arrays.asList(finals));
        String line="";
        while ((line=br.readLine())!=null) {        	
        	String[] transition=line.trim().split(" ");
        	transitions.put(transition[0]+"_"+transition[1], transition[2]);
        }
    }
    
    public static void main(String[] args) throws Exception{
        DFA dfa = new DFA(args[0]);
        try{
            Scanner scanner = new Scanner(new File(args[1]));
            BufferedWriter bw=new BufferedWriter(new FileWriter(args[2]));
			int count = 0;
            while(scanner.hasNextLine()){
                boolean result = Simulator.run(dfa,scanner.nextLine());
                bw.write("case " + count +": " + result+"\n");
				count ++;
            }
            bw.close();

        }catch(FileNotFoundException e){
            e.printStackTrace();
        }
     }
}
