import java_cup.runtime.*;

%%
%cup
%class A3Scanner
%eofval{ return null;
%eofval}
%state COMMENT

IDENTIFIER = [a-zA-Z][a-zA-Z0-9]*
NUMBER = [0-9]*[.]?[0-9]*
QUOTES = \"[^\"]*\"

%%
<YYINITIAL>"/**" {yybegin(COMMENT);}
<COMMENT>"**/" {yybegin(YYINITIAL);}
<COMMENT>.|\r|\n {}
<YYINITIAL>STRING|INT|REAL {return new Symbol(A3Symbol.TYPE);}
<YYINITIAL>BEGIN {return new Symbol(A3Symbol.BEGIN);}
<YYINITIAL>END {return new Symbol(A3Symbol.END);}
<YYINITIAL>IF {return new Symbol(A3Symbol.IF);}
<YYINITIAL>ELSE {return new Symbol(A3Symbol.ELSE);}
<YYINITIAL>READ {return new Symbol(A3Symbol.READ);}
<YYINITIAL>WRITE {return new Symbol(A3Symbol.WRITE);}
<YYINITIAL>RETURN {return new Symbol(A3Symbol.RETURN);}
<YYINITIAL>MAIN {return new Symbol(A3Symbol.MAIN);}
<YYINITIAL>":=" {return new Symbol(A3Symbol.ASIGN);}
<YYINITIAL>"==" {return new Symbol(A3Symbol.EQ);}
<YYINITIAL>"!=" {return new Symbol(A3Symbol.NOTEQUAL);}
<YYINITIAL>"+" {return new Symbol(A3Symbol.PLUS);}
<YYINITIAL>"-" {return new Symbol(A3Symbol.MINUS);}
<YYINITIAL>"*" {return new Symbol(A3Symbol.TIMES);}
<YYINITIAL>"/" {return new Symbol(A3Symbol.DIVIDE);}
<YYINITIAL>";" {return new Symbol(A3Symbol.SEMI);}
<YYINITIAL>"(" {return new Symbol(A3Symbol.LPAREN);}
<YYINITIAL>")" {return new Symbol(A3Symbol.RPAREN);}
<YYINITIAL>"," {return new Symbol(A3Symbol.COMMA);}
<YYINITIAL> {QUOTES} {return new Symbol(A3Symbol.QUOTES, yytext());}
<YYINITIAL> {IDENTIFIER} {return new Symbol(A3Symbol.ID, yytext());}
<YYINITIAL> {NUMBER} {return new Symbol(A3Symbol.NUMBER, yytext());}
" "|\t|\r|\n {}
. { return new Symbol(A3Symbol.error);}


