/*
SOLUTION BY JEREMIE BORNAIS
*/
public class Simulator {
    public static boolean run(DFA dfa, String input) {
        String s = dfa.startState;
        String c;
        for (int i = 0; i < input.length(); i++) {
            c = input.substring(i, i + 1);
            s = dfa.transitions.get(s + "_" + c);
        }
        if (dfa.finalStates.contains(s))
            return true;
        return false;
    }
}