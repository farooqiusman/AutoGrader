import java_cup.runtime.*;


class A3Scanner implements java_cup.runtime.Scanner {
	private final int YY_BUFFER_SIZE = 512;
	private final int YY_F = -1;
	private final int YY_NO_STATE = -1;
	private final int YY_NOT_ACCEPT = 0;
	private final int YY_START = 1;
	private final int YY_END = 2;
	private final int YY_NO_ANCHOR = 4;
	private final int YY_BOL = 128;
	private final int YY_EOF = 129;
	private java.io.BufferedReader yy_reader;
	private int yy_buffer_index;
	private int yy_buffer_read;
	private int yy_buffer_start;
	private int yy_buffer_end;
	private char yy_buffer[];
	private boolean yy_at_bol;
	private int yy_lexical_state;

	A3Scanner (java.io.Reader reader) {
		this ();
		if (null == reader) {
			throw (new Error("Error: Bad input stream initializer."));
		}
		yy_reader = new java.io.BufferedReader(reader);
	}

	A3Scanner (java.io.InputStream instream) {
		this ();
		if (null == instream) {
			throw (new Error("Error: Bad input stream initializer."));
		}
		yy_reader = new java.io.BufferedReader(new java.io.InputStreamReader(instream));
	}

	private A3Scanner () {
		yy_buffer = new char[YY_BUFFER_SIZE];
		yy_buffer_read = 0;
		yy_buffer_index = 0;
		yy_buffer_start = 0;
		yy_buffer_end = 0;
		yy_at_bol = true;
		yy_lexical_state = YYINITIAL;
	}

	private boolean yy_eof_done = false;
	private final int YYINITIAL = 0;
	private final int COMMENT = 1;
	private final int yy_state_dtrans[] = {
		0,
		38
	};
	private void yybegin (int state) {
		yy_lexical_state = state;
	}
	private int yy_advance ()
		throws java.io.IOException {
		int next_read;
		int i;
		int j;

		if (yy_buffer_index < yy_buffer_read) {
			return yy_buffer[yy_buffer_index++];
		}

		if (0 != yy_buffer_start) {
			i = yy_buffer_start;
			j = 0;
			while (i < yy_buffer_read) {
				yy_buffer[j] = yy_buffer[i];
				++i;
				++j;
			}
			yy_buffer_end = yy_buffer_end - yy_buffer_start;
			yy_buffer_start = 0;
			yy_buffer_read = j;
			yy_buffer_index = j;
			next_read = yy_reader.read(yy_buffer,
					yy_buffer_read,
					yy_buffer.length - yy_buffer_read);
			if (-1 == next_read) {
				return YY_EOF;
			}
			yy_buffer_read = yy_buffer_read + next_read;
		}

		while (yy_buffer_index >= yy_buffer_read) {
			if (yy_buffer_index >= yy_buffer.length) {
				yy_buffer = yy_double(yy_buffer);
			}
			next_read = yy_reader.read(yy_buffer,
					yy_buffer_read,
					yy_buffer.length - yy_buffer_read);
			if (-1 == next_read) {
				return YY_EOF;
			}
			yy_buffer_read = yy_buffer_read + next_read;
		}
		return yy_buffer[yy_buffer_index++];
	}
	private void yy_move_end () {
		if (yy_buffer_end > yy_buffer_start &&
		    '\n' == yy_buffer[yy_buffer_end-1])
			yy_buffer_end--;
		if (yy_buffer_end > yy_buffer_start &&
		    '\r' == yy_buffer[yy_buffer_end-1])
			yy_buffer_end--;
	}
	private boolean yy_last_was_cr=false;
	private void yy_mark_start () {
		yy_buffer_start = yy_buffer_index;
	}
	private void yy_mark_end () {
		yy_buffer_end = yy_buffer_index;
	}
	private void yy_to_mark () {
		yy_buffer_index = yy_buffer_end;
		yy_at_bol = (yy_buffer_end > yy_buffer_start) &&
		            ('\r' == yy_buffer[yy_buffer_end-1] ||
		             '\n' == yy_buffer[yy_buffer_end-1] ||
		             2028/*LS*/ == yy_buffer[yy_buffer_end-1] ||
		             2029/*PS*/ == yy_buffer[yy_buffer_end-1]);
	}
	private java.lang.String yytext () {
		return (new java.lang.String(yy_buffer,
			yy_buffer_start,
			yy_buffer_end - yy_buffer_start));
	}
	private int yylength () {
		return yy_buffer_end - yy_buffer_start;
	}
	private char[] yy_double (char buf[]) {
		int i;
		char newbuf[];
		newbuf = new char[2*buf.length];
		for (i = 0; i < buf.length; ++i) {
			newbuf[i] = buf[i];
		}
		return newbuf;
	}
	private final int YY_E_INTERNAL = 0;
	private final int YY_E_MATCH = 1;
	private java.lang.String yy_error_string[] = {
		"Error: Internal error.\n",
		"Error: Unmatched input.\n"
	};
	private void yy_error (int code,boolean fatal) {
		java.lang.System.out.print(yy_error_string[code]);
		java.lang.System.out.flush();
		if (fatal) {
			throw new Error("Fatal Error.\n");
		}
	}
	private int[][] unpackFromString(int size1, int size2, String st) {
		int colonIndex = -1;
		String lengthString;
		int sequenceLength = 0;
		int sequenceInteger = 0;

		int commaIndex;
		String workString;

		int res[][] = new int[size1][size2];
		for (int i= 0; i < size1; i++) {
			for (int j= 0; j < size2; j++) {
				if (sequenceLength != 0) {
					res[i][j] = sequenceInteger;
					sequenceLength--;
					continue;
				}
				commaIndex = st.indexOf(',');
				workString = (commaIndex==-1) ? st :
					st.substring(0, commaIndex);
				st = st.substring(commaIndex+1);
				colonIndex = workString.indexOf(':');
				if (colonIndex == -1) {
					res[i][j]=Integer.parseInt(workString);
					continue;
				}
				lengthString =
					workString.substring(colonIndex+1);
				sequenceLength=Integer.parseInt(lengthString);
				workString=workString.substring(0,colonIndex);
				sequenceInteger=Integer.parseInt(workString);
				res[i][j] = sequenceInteger;
				sequenceLength--;
			}
		}
		return res;
	}
	private int yy_acpt[] = {
		/* 0 */ YY_NO_ANCHOR,
		/* 1 */ YY_NO_ANCHOR,
		/* 2 */ YY_NO_ANCHOR,
		/* 3 */ YY_NO_ANCHOR,
		/* 4 */ YY_NO_ANCHOR,
		/* 5 */ YY_NO_ANCHOR,
		/* 6 */ YY_NO_ANCHOR,
		/* 7 */ YY_NO_ANCHOR,
		/* 8 */ YY_NO_ANCHOR,
		/* 9 */ YY_NO_ANCHOR,
		/* 10 */ YY_NO_ANCHOR,
		/* 11 */ YY_NO_ANCHOR,
		/* 12 */ YY_NO_ANCHOR,
		/* 13 */ YY_NOT_ACCEPT,
		/* 14 */ YY_NO_ANCHOR,
		/* 15 */ YY_NO_ANCHOR,
		/* 16 */ YY_NO_ANCHOR,
		/* 17 */ YY_NO_ANCHOR,
		/* 18 */ YY_NO_ANCHOR,
		/* 19 */ YY_NO_ANCHOR,
		/* 20 */ YY_NO_ANCHOR,
		/* 21 */ YY_NO_ANCHOR,
		/* 22 */ YY_NO_ANCHOR,
		/* 23 */ YY_NO_ANCHOR,
		/* 24 */ YY_NO_ANCHOR,
		/* 25 */ YY_NO_ANCHOR,
		/* 26 */ YY_NO_ANCHOR,
		/* 27 */ YY_NO_ANCHOR,
		/* 28 */ YY_NO_ANCHOR,
		/* 29 */ YY_NO_ANCHOR,
		/* 30 */ YY_NO_ANCHOR,
		/* 31 */ YY_NO_ANCHOR,
		/* 32 */ YY_NO_ANCHOR,
		/* 33 */ YY_NOT_ACCEPT,
		/* 34 */ YY_NO_ANCHOR,
		/* 35 */ YY_NO_ANCHOR,
		/* 36 */ YY_NO_ANCHOR,
		/* 37 */ YY_NO_ANCHOR,
		/* 38 */ YY_NOT_ACCEPT,
		/* 39 */ YY_NO_ANCHOR,
		/* 40 */ YY_NO_ANCHOR,
		/* 41 */ YY_NOT_ACCEPT,
		/* 42 */ YY_NO_ANCHOR,
		/* 43 */ YY_NO_ANCHOR,
		/* 44 */ YY_NO_ANCHOR,
		/* 45 */ YY_NO_ANCHOR,
		/* 46 */ YY_NO_ANCHOR,
		/* 47 */ YY_NO_ANCHOR,
		/* 48 */ YY_NO_ANCHOR,
		/* 49 */ YY_NO_ANCHOR,
		/* 50 */ YY_NO_ANCHOR,
		/* 51 */ YY_NO_ANCHOR,
		/* 52 */ YY_NO_ANCHOR,
		/* 53 */ YY_NO_ANCHOR,
		/* 54 */ YY_NO_ANCHOR,
		/* 55 */ YY_NO_ANCHOR,
		/* 56 */ YY_NO_ANCHOR,
		/* 57 */ YY_NO_ANCHOR,
		/* 58 */ YY_NO_ANCHOR,
		/* 59 */ YY_NO_ANCHOR,
		/* 60 */ YY_NO_ANCHOR,
		/* 61 */ YY_NO_ANCHOR,
		/* 62 */ YY_NO_ANCHOR,
		/* 63 */ YY_NO_ANCHOR,
		/* 64 */ YY_NO_ANCHOR,
		/* 65 */ YY_NO_ANCHOR,
		/* 66 */ YY_NO_ANCHOR,
		/* 67 */ YY_NO_ANCHOR
	};
	private int yy_cmap[] = unpackFromString(1,130,
"3:9,4:2,3:2,4,3:18,4,22,29,3:5,26,27,2,23,28,24,32,1,31:10,20,25,3,21,3:3,1" +
"2,14,30,15,11,16,10,30,8,30:2,13,19,9,30:3,7,5,6,18,30,17,30:3,3:6,30:26,3:" +
"5,0:2")[0];

	private int yy_rmap[] = unpackFromString(1,68,
"0,1,2,1:3,3,1:6,4,5,1:5,5:8,1:2,6,7,8,9,10,11,12,13,14,15,16,17,9,18,19,20," +
"21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,5")[0];

	private int yy_nxt[][] = unpackFromString(42,33,
"1,2,3,4,5,6,67,58,32,67:2,50,67:2,64,67:2,65,67,59,31,36,39,7,8,9,10,11,12," +
"42,67,30,35,-1:35,13,-1:35,67,66,67:13,-1:10,67:2,-1:3,19,-1:35,67:15,-1:10" +
",67:2,-1:32,30,35,-1:21,15,-1:16,67:4,37,67:6,14,67:3,-1:10,67:2,-1:2,33:28" +
",18,33:3,-1:2,41,-1:61,35,-1:22,16,-1:16,67,20,67:13,-1:10,67:2,-1,1,28,34," +
"28:30,-1:21,17,-1:16,67:10,21,67:4,-1:10,67:2,-1:2,29,-1:36,67:8,20,67,22,6" +
"7:4,-1:10,67:2,-1:6,67:6,23,67:8,-1:10,67:2,-1:6,67:4,24,67:10,-1:10,67:2,-" +
"1:6,67:4,25,67:10,-1:10,67:2,-1:6,67:6,26,67:8,-1:10,67:2,-1:6,67:5,20,67:9" +
",-1:10,67:2,-1:6,67:4,27,67:10,-1:10,67:2,-1:6,67:4,40,67:3,52,67:6,-1:10,6" +
"7:2,-1:6,67,63,67:5,43,67:7,-1:10,67:2,-1:6,44,67:14,-1:10,67:2,-1:6,67:3,4" +
"5,67:11,-1:10,67:2,-1:6,67:3,46,67:11,-1:10,67:2,-1:6,67,47,67:13,-1:10,67:" +
"2,-1:6,67:4,48,67:10,-1:10,67:2,-1:6,67:2,49,67:12,-1:10,67:2,-1:6,67:6,51," +
"67:8,-1:10,67:2,-1:6,67:7,53,67:7,-1:10,67:2,-1:6,67:5,54,67:9,-1:10,67:2,-" +
"1:6,67:3,55,67:11,-1:10,67:2,-1:6,67:3,56,67:11,-1:10,67:2,-1:6,67:13,57,67" +
",-1:10,67:2,-1:6,67:6,60,67:8,-1:10,67:2,-1:6,67:2,61,67:12,-1:10,67:2,-1:6" +
",67:2,62,67:12,-1:10,67:2,-1");

	public java_cup.runtime.Symbol next_token ()
		throws java.io.IOException {
		int yy_lookahead;
		int yy_anchor = YY_NO_ANCHOR;
		int yy_state = yy_state_dtrans[yy_lexical_state];
		int yy_next_state = YY_NO_STATE;
		int yy_last_accept_state = YY_NO_STATE;
		boolean yy_initial = true;
		int yy_this_accept;

		yy_mark_start();
		yy_this_accept = yy_acpt[yy_state];
		if (YY_NOT_ACCEPT != yy_this_accept) {
			yy_last_accept_state = yy_state;
			yy_mark_end();
		}
		while (true) {
			if (yy_initial && yy_at_bol) yy_lookahead = YY_BOL;
			else yy_lookahead = yy_advance();
			yy_next_state = YY_F;
			yy_next_state = yy_nxt[yy_rmap[yy_state]][yy_cmap[yy_lookahead]];
			if (YY_EOF == yy_lookahead && true == yy_initial) {
 return null;
			}
			if (YY_F != yy_next_state) {
				yy_state = yy_next_state;
				yy_initial = false;
				yy_this_accept = yy_acpt[yy_state];
				if (YY_NOT_ACCEPT != yy_this_accept) {
					yy_last_accept_state = yy_state;
					yy_mark_end();
				}
			}
			else {
				if (YY_NO_STATE == yy_last_accept_state) {
					throw (new Error("Lexical Error: Unmatched Input."));
				}
				else {
					yy_anchor = yy_acpt[yy_last_accept_state];
					if (0 != (YY_END & yy_anchor)) {
						yy_move_end();
					}
					yy_to_mark();
					switch (yy_last_accept_state) {
					case 0:
						{return new Symbol(A3Symbol.NUMBER, yytext());}
					case -2:
						break;
					case 1:
						
					case -3:
						break;
					case 2:
						{return new Symbol(A3Symbol.DIVIDE);}
					case -4:
						break;
					case 3:
						{return new Symbol(A3Symbol.TIMES);}
					case -5:
						break;
					case 4:
						{ return new Symbol(A3Symbol.error);}
					case -6:
						break;
					case 5:
						{}
					case -7:
						break;
					case 6:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -8:
						break;
					case 7:
						{return new Symbol(A3Symbol.PLUS);}
					case -9:
						break;
					case 8:
						{return new Symbol(A3Symbol.MINUS);}
					case -10:
						break;
					case 9:
						{return new Symbol(A3Symbol.SEMI);}
					case -11:
						break;
					case 10:
						{return new Symbol(A3Symbol.LPAREN);}
					case -12:
						break;
					case 11:
						{return new Symbol(A3Symbol.RPAREN);}
					case -13:
						break;
					case 12:
						{return new Symbol(A3Symbol.COMMA);}
					case -14:
						break;
					case 14:
						{return new Symbol(A3Symbol.IF);}
					case -15:
						break;
					case 15:
						{return new Symbol(A3Symbol.ASIGN);}
					case -16:
						break;
					case 16:
						{return new Symbol(A3Symbol.EQ);}
					case -17:
						break;
					case 17:
						{return new Symbol(A3Symbol.NOTEQUAL);}
					case -18:
						break;
					case 18:
						{return new Symbol(A3Symbol.QUOTES, yytext());}
					case -19:
						break;
					case 19:
						{yybegin(COMMENT);}
					case -20:
						break;
					case 20:
						{return new Symbol(A3Symbol.TYPE);}
					case -21:
						break;
					case 21:
						{return new Symbol(A3Symbol.END);}
					case -22:
						break;
					case 22:
						{return new Symbol(A3Symbol.READ);}
					case -23:
						break;
					case 23:
						{return new Symbol(A3Symbol.ELSE);}
					case -24:
						break;
					case 24:
						{return new Symbol(A3Symbol.MAIN);}
					case -25:
						break;
					case 25:
						{return new Symbol(A3Symbol.BEGIN);}
					case -26:
						break;
					case 26:
						{return new Symbol(A3Symbol.WRITE);}
					case -27:
						break;
					case 27:
						{return new Symbol(A3Symbol.RETURN);}
					case -28:
						break;
					case 28:
						{}
					case -29:
						break;
					case 29:
						{yybegin(YYINITIAL);}
					case -30:
						break;
					case 30:
						{return new Symbol(A3Symbol.NUMBER, yytext());}
					case -31:
						break;
					case 31:
						{ return new Symbol(A3Symbol.error);}
					case -32:
						break;
					case 32:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -33:
						break;
					case 34:
						{}
					case -34:
						break;
					case 35:
						{return new Symbol(A3Symbol.NUMBER, yytext());}
					case -35:
						break;
					case 36:
						{ return new Symbol(A3Symbol.error);}
					case -36:
						break;
					case 37:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -37:
						break;
					case 39:
						{ return new Symbol(A3Symbol.error);}
					case -38:
						break;
					case 40:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -39:
						break;
					case 42:
						{ return new Symbol(A3Symbol.error);}
					case -40:
						break;
					case 43:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -41:
						break;
					case 44:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -42:
						break;
					case 45:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -43:
						break;
					case 46:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -44:
						break;
					case 47:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -45:
						break;
					case 48:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -46:
						break;
					case 49:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -47:
						break;
					case 50:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -48:
						break;
					case 51:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -49:
						break;
					case 52:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -50:
						break;
					case 53:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -51:
						break;
					case 54:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -52:
						break;
					case 55:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -53:
						break;
					case 56:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -54:
						break;
					case 57:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -55:
						break;
					case 58:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -56:
						break;
					case 59:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -57:
						break;
					case 60:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -58:
						break;
					case 61:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -59:
						break;
					case 62:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -60:
						break;
					case 63:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -61:
						break;
					case 64:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -62:
						break;
					case 65:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -63:
						break;
					case 66:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -64:
						break;
					case 67:
						{return new Symbol(A3Symbol.ID, yytext());}
					case -65:
						break;
					default:
						yy_error(YY_E_INTERNAL,false);
					case -1:
					}
					yy_initial = true;
					yy_state = yy_state_dtrans[yy_lexical_state];
					yy_next_state = YY_NO_STATE;
					yy_last_accept_state = YY_NO_STATE;
					yy_mark_start();
					yy_this_accept = yy_acpt[yy_state];
					if (YY_NOT_ACCEPT != yy_this_accept) {
						yy_last_accept_state = yy_state;
						yy_mark_end();
					}
				}
			}
		}
	}
}
