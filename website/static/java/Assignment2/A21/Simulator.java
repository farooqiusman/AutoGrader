public class Simulator {
     public static boolean run(DFA dfa, String input){
        String str = dfa.startState; // will get the current state
        int i = 0;
        Character c = (char)0; //make empty char
        while(i != input.length()){
            c = input.charAt(i); //get current char
            str = dfa.transitions.get(str + "_" + c); // get next state
            i++; // set i++, also next char
        }
        if(dfa.finalStates.contains(str) && c != null){
            return true;
        }
        return false;
    }

}
