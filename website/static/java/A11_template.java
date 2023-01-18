import java.io.FileReader;
import java.io.BufferedReader;
import java.util.Set;
import java.util.HashSet;
import java.io.*;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.*;

public class A11_template {
  //check whether the char is a letter
  static boolean isLetter(int character) {
    return (character >= 'a' && character <= 'z') || (character >= 'A' && character <= 'Z');
  }
  
  // check whether the char is a letter or digit
  static boolean isLetterOrDigit(int character) {
    return isLetter(character) || (character >= '0' && character <= '9');
  }

//IDENTIFIERCODEHERE
		 		
  public static void main(String[] args) throws Exception{
    for(int i=0; i<6; i++){
        Set<String> ids=getIdentifiers("A1"+i+".input");
        System.out.println(ids.size());
    }
  }
}