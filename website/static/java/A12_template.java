import java.io.*;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.*;

public class A12_template {

//IDENTIFIERCODEHERE

    public static void main(String[] args) throws Exception {
        for(int i=0; i<6; i++){
            Set<String> ids=getIdRegex("A1"+i+".input");
            System.out.println(ids.size());
        }
    }
}