import java.io.*;
%%
%{    public static void main(String argv[]) throws java.io.IOException {
			// SOLUTION BY JEREMIE BORNAIS
      		A2 yy = new A2(new FileInputStream(new File("A2.input")));
	  		int t, identifiers=0, keywords=0, numbers=0, quotes=0, comments=0;
			while ((t = yy.yylex())>=0){
				switch(t){
					case 0:
						keywords++;
						break;
					case 1:
						identifiers++;
						break;
					case 2:
						numbers++;
						break;
					case 3:
						quotes++;
						break;
					case 4:
						comments++;
						break;
				}
	  		}
			FileWriter f = new FileWriter("A2.output");
			f.write("identifiers: "+identifiers+"\nkeywords: "+keywords+"\nnumbers: "+numbers+"\ncomments: "+comments+"\nquotedString: "+quotes);
			f.close();
      }
%}
%notunix
%type int
%class A2
%eofval{ return -1;
%eofval}

IDENTIFIER = [a-zA-Z][a-zA-Z0-9]*
KEYWORD = WRITE|READ|IF|ELSE|RETURN|BEGIN|END|MAIN|STRING|INT|REAL
NUMBER = [0-9]+(\.[0-9]+)?
QUOTED = \"[^\"]*\"
%state COMMENT

%%
<YYINITIAL>{KEYWORD} { return 0; }
<YYINITIAL>{IDENTIFIER} { return 1;}
<YYINITIAL>{NUMBER} { return 2;}
<YYINITIAL>{QUOTED} { return 3;}
<YYINITIAL>"/**" {yybegin(COMMENT);}
<COMMENT>"**/" {yybegin(YYINITIAL); return 4;} 

\r|\n {}
. {}