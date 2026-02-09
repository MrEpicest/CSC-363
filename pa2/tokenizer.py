from charstream import CharStream
from tokens import Token, TokenType
from tokenstream import TokenStream
import string

RESERVED = {'i', 'f', 'o', 'n', 'p', 'l', 's'}
VALID_VARS = set(string.ascii_lowercase) - RESERVED

class Tokenizer:

    def __init__(self, cs: CharStream):
        self.cs = cs

    def tokenize(self) -> TokenStream:
        ts = TokenStream()
        while True:
            tok = self.nexttoken()
            ts.append(tok)
            if tok.tokentype == TokenType.EOF:
                break

        return ts
    

    def nexttoken(self) -> Token:

        char = self.cs.read()

        while char in {' ', '\n', '\r', '\t'}:
            char = self.cs.read() # Consume chars for space, newline, etc.
        
        
        if char == '':
            return Token(TokenType.EOF, lexeme = f"{char}")



        match char:

            case '=':
                return Token(TokenType.ASSIGN, lexeme = f"{char}")
            
            case '(':
                return Token(TokenType.LPAREN, lexeme = f"{char}")
                
            case ')': 
                return Token(TokenType.RPAREN, lexeme = f"{char}")
            
            case '+':
                return Token(TokenType.PLUS, lexeme = f"{char}")
            
            case '-':
                return Token(TokenType.MINUS, lexeme = f"{char}")
            
            case '*':
                return Token(TokenType.TIMES, lexeme = f"{char}")
            
            case '/':
                return Token(TokenType.DIVIDE, lexeme = f"{char}")
            
            case '^':
                return Token(TokenType.EXPONENT, lexeme = f"{char}")
            
            case 'i':
                next = self.cs.read()
                while next in {' ', '\n', '\r', '\t'}:
                    next = self.cs.read()
                if next in RESERVED:
                    raise ValueError(f"Invalid variable character: '{next}'")
                return Token(TokenType.INTDEC, lexeme = f"{char}{next}", name = f"{next}")

            case 'p':
                next = self.cs.read()
                while next in {' ', '\n', '\r', '\t'}:
                    next = self.cs.read()
                if next in RESERVED:
                    raise ValueError(f"Invalid variable character: '{next}'")
                return Token(TokenType.PRINT, lexeme = f"{char}{next}", name = f"{next}")
            
            case '0':
                next = self.cs.peek()
                if next in ["1","2","3","4","5","6","7","8","9","0"]:
                    raise ValueError("Integer literal cannot have a leading zero")
                else:
                    return Token(TokenType.INTLIT, lexeme = f"{char}", intvalue = f"{char}")

            case "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                number = char
                next = self.cs.peek()
                        
                while next in ["1","2","3","4","5","6","7","8","9","0"]:
                    self.cs.advance()
                    number += next
                    next = self.cs.peek()

                return Token(TokenType.INTLIT, lexeme = f"{number}", intvalue = f"{number}")

            case _:

                if char in VALID_VARS:
                    return Token(TokenType.VARREF, lexeme = f"{char}")

                pass # Move on to secondary inspection to handle digits, vars, error case

        if char.isdigit():
            lexeme, intvalue = self.readintliteral(char)
            return Token(TokenType.INTLIT, lexeme = lexeme, intvalue = intvalue)


        if char.isalpha():
            if char not in VALID_VARS:
                raise ValueError(f"Invalid variable character: {char}")
            else:
                raise NotImplementedError
           
        raise ValueError(f"Unexpected character: {char!r}")
        
    

    def readintliteral(self, firstchar: str) -> tuple[str, int]:
        
        digits: list[str] = []
        digits.append(firstchar)
        #if CONDITION:
        #    raise ValueError("Integer literal cannot have a leading zero")

        #while not self.cs.eof() and SOMETHING:
        #    digits.append(SOMETHING)

        lexeme = ''.join(digits)

        return lexeme, int(lexeme)
