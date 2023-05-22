grammar Gramatica;

program: block EOF;

block: LCURLY decls stmts ret RCURLY;

decls: ((decl decls)
     | (func_decl decls))*;

decl: type ID SEMI;

type: basic 
    | type LSQBRACKETS INT RSQBRACKETS;

basic: INTTYPE 
     | FLOATTYPE 
     | VOIDTYPE
     | BOOLTYPE;

func_decl: basic ID LPAREN args RPAREN block;

args: (arg_list)*;

arg_list: arg_list COMMA type ID
        | type ID;

call_args: (call_arg_list)*;

call_arg_list: (factor | ID) (COMMA call_arg_list)*;

stmts: (stmt stmts)*;

stmt: loc EQ bool SEMI
    | loc EQ hw_interact SEMI
    | loc EQ ID LPAREN args RPAREN SEMI
    | hw_interact SEMI
    | ID LPAREN call_args RPAREN SEMI
    | RESVFOR LPAREN loc EQ INT SEMI equality SEMI loc EQ expr RPAREN stmt
    | ctrl_struct
    | RESVWHILE LPAREN bool RPAREN stmt
    | RESVDO stmt RESVWHILE LPAREN bool RPAREN
    | RESVBREAK SEMI
    | block;
    
loc: loc LSQBRACKETS bool RSQBRACKETS
   | ID;

ctrl_struct: RESVIF LPAREN bool RPAREN stmt (ctrl_struct)*
           | RESVELSEIF LPAREN bool RPAREN stmt (ctrl_struct)*
           | RESVELSE stmt;

hw_interact: HWPINMODE INT ',' INT
           | HWDIGREAD INT
           | HWDIGWRITE INT ',' loc
           | HWDIGWRITE INT ',' boolean
           | HWANAREAD INT
           | HWANAWRITE INT ',' loc
           | HWANAWRITE INT ',' INT
           | HWBAUD INT
           | HWAVAILABLE
           | HWSERIALREAD
           | HWSERIALWRITE loc
           | HWSERIALWRITE INT;

ret: (RESVRET (bool)* SEMI)*;

bool: join
    | bool OR join;

join: equality
    | join AND equality;


equality: rel
        | equality DOUBLEEQUAL rel
        | equality DIFFERENT rel;

rel: (expr (LOWERTHAN | LOWEREQUALTHAN | HIGHERTHAN | HIGHEREQUALTHAN))* expr;

expr: term
    | expr PLUS term
    | expr MINUS term;

term: unary
    | term MULTIPLIE unary
    | term DIVIDE unary;

unary: (MINUS | NOT) unary
     | factor;
    
factor: LPAREN bool RPAREN
      | loc
      | INT
      | FLOAT
      | boolean;
      
boolean: TRUE | FALSE;

FLOATINGPOINT: '.';
AND : '&&' ;
OR : '||' ;
NOT : '!' ;
EQ : '=' ;
COMMA : ',' ;
SEMI : ';' ;
MINUS: '-' ;
DOUBLEEQUAL: '==';
DIFFERENT: '!=';
LOWERTHAN: '<';
LOWEREQUALTHAN: '<=';
HIGHERTHAN: '>';
HIGHEREQUALTHAN: '>=';
PLUS:'+';
MULTIPLIE: '*';
DIVIDE: '/';
LPAREN : '(' ;
RPAREN : ')' ;
LCURLY : '{' ;
RCURLY : '}' ;
LSQBRACKETS: '[';
RSQBRACKETS: ']';
INTTYPE: 'int';
FLOATTYPE: 'float';
VOIDTYPE: 'void';
BOOLTYPE: 'boolean';
TRUE: 'true';
FALSE: 'false';
RESVFOR: 'for';
RESVWHILE: 'while';
RESVDO: 'do';
RESVBREAK: 'break';
RESVIF: 'if';
RESVELSEIF: 'elseif';
RESVELSE: 'else';
RESVRET: 'return';

HWPINMODE: 'pinMode';
HWDIGREAD: 'digitalRead';
HWDIGWRITE: 'digitalWrite';
HWANAREAD: 'analogRead';
HWANAWRITE: 'analogWrite';
HWBAUD: 'serialBaud';
HWAVAILABLE: 'serialAvailable';
HWSERIALREAD: 'serialRead';
HWSERIALWRITE: 'serialWrite';

INT : [0-9]+ ;
FLOAT : (INT)* FLOATINGPOINT INT;
ID: [a-zA-Z_][a-zA-Z_0-9]* ;
WS: [ \t\n\r\f]+ -> skip ;