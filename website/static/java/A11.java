import java.io.FileReader;
import java.io.BufferedReader;
import java.util.Set;
import java.util.HashSet;
import java.io.*;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.*;

public class A11 {
  //check whether the char is a letter
  static boolean isLetter(int character) {
    return (character >= 'a' && character <= 'z') || (character >= 'A' && character <= 'Z');
  }
  
  // check whether the char is a letter or digit
  static boolean isLetterOrDigit(int character) {
    return isLetter(character) || (character >= '0' && character <= '9');
  }

    public static Set<String> getIdentifiers(String filename) throws Exception {
        String[] keywordsArray = { "IF", "WRITE", "READ", "RETURN", "BEGIN", "END", "MAIN", "INT", "REAL" };
        Set<String> keywords = new HashSet();
        Set<String> identifiers = new HashSet();
        for (String s : keywordsArray) {
            keywords.add(s);
        }
        FileReader reader = new FileReader(filename);
        BufferedReader br = new BufferedReader(reader);
        String line;
        while ((line = br.readLine()) != null) {
            int i = 0;
            while (i < line.length()) {
                // System.out.println(i);
                if (line.charAt(i) == '\"') {
                    i++;
                    // throw away quoted strings
                    while (line.charAt(i) != '\"')
                        i++;
                    i++;
                }
                if (isLetter(line.charAt(i))) {
                    int j = i;
                    while (j < line.length()) {
                        if (isLetterOrDigit(line.charAt(j))) {
                            j++;
                        } else {
                            break;
                        }
                    }
                    identifiers.add(line.substring(i, j));
                    // System.out.println(line.substring(i, j));
                    i = j;
                } else {
                    i++;
                }
            }
        }
        for (String s : keywords) {
            if (identifiers.contains(s))
                identifiers.remove(s);
        }
     throw new Exception();
    }

//   public static Set<String> getIdentifiers(String filename) throws Exception{

// 		String[] keywordsArray = { "IF", "WRITE", "READ", "RETURN", "BEGIN",
// 				"END", "MAIN", "INT", "REAL" };
// 		Set<String> keywords = new HashSet();
// 		Set<String> identifiers = new HashSet();
// 		for (String s : keywordsArray) {;
// 			keywords.add(s);
// 		}
// 		String state="INIT"; // Initially it is in the INIT state. 
		
// 		StringBuilder code = new StringBuilder();
// 		BufferedReader br = new BufferedReader(new FileReader(filename));
// 		String line;
// 		while ((line = br.readLine()) != null) { 
// 			code=code.append(line+"\n");
// 		} // read the text line by line.
// 		code =code.append('$'); //add a special symbol to indicate the end of file.  

// 		int len=code.length();
// 		String token="";
// 		for (int i=0; i<len; i++) { //look at the characters one by one
// 			char next_char=code.charAt(i);

// 			if (state.contentEquals("INIT")){ 
// 			    if (isLetter(next_char)){	 
// 			    	state="ID";  // go to the ID state
// 			    	token=token+next_char;
// 			    } //ignore everything if it is not a letter
			
// 			}else if (state.equals("ID")) {
// 				if (isLetterOrDigit(next_char)) { //take letter or digit if it is in ID state
// 				  token=token+next_char;
// 				} else { // end of ID state
// 					identifiers.add(token);
// 					token="";
// 					state="INIT";
// 				}	

// 			}

// 		}
		
//         // throw new FileNotFoundException();
// 		return identifiers;
//     }
		 		
  public static void main(String[] args) throws Exception{
    for(int i=0; i<6; i++){
        Set<String> ids=getIdentifiers("A1"+i+".input");
        System.out.println(ids.size());
    }
  }
}