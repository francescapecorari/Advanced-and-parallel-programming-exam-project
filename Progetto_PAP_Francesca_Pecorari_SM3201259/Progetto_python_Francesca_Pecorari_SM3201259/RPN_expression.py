"""

    Francesca Pecorari SM3201259 

"""

"""

     Eccezioni

"""

class EmptyStackException(Exception):
    pass

class MissingVariableException(Exception):
    pass

class UndefinedOperationException(Exception):
    pass

class InvalidExpressionException(Exception):
    pass


"""

    Stack

"""

class Stack:

    def __init__(self):
        self.data = []

    def push(self, x):
        self.data.append(x)

    def pop(self):
        if self.data == []:
            raise EmptyStackException
        res = self.data[-1]
        self.data = self.data[0:-1]
        return res

    def __str__(self):
        return " ".join([str(s) for s in self.data])


"""

    Classi base

"""

class Expression:

    '''
        Metodi della classe: 

        __init__:
            Costruttore della classe. 
            Solleva un'eccezione NotImplementedError perché 
            questa classe è pensata per essere una classe base astratta, 
            e non dovrebbe essere istanziata direttamente.
        
        from_program(cls, text, dispatch):
            Metodo di classe (decorato con @classmethod) 
            che prende in input una stringa text rappresentante un programma e un 
            dizionario dispatch che associa i token del programma alle classi 
            di operazioni appropriate. 
            Questo metodo analizza il testo del programma, 
            crea un albero di espressioni utilizzando uno stack
            e restituisce l'espressione radice dell'albero. 
            Utilizza le classi di operazioni definite nel dizionario dispatch 
            per creare le operazioni appropriate.
        
        evaluate(self, env): 
            Metodo astratto che deve essere implementato dalle sottoclassi. 
            Prende in input un ambiente env e restituisce il risultato 
            della valutazione dell'espressione nell'ambiente dato.

    '''

    def __init__(self):
        raise NotImplementedError()

    @classmethod
    def from_program(cls, text, dispatch):
        '''
           Parametri:

           text: Una stringa rappresentante il programma da analizzare.
           dispatch: Un dizionario che associa i token del programma 
           alle classi di operazioni appropriate.
           
           Algoritmo:
           
           Inizializza una pila vuota stack.
           Suddivide la stringa text in token utilizzando lo spazio come delimitatore.

           Itera attraverso i token del programma:
           Se un token è numerico, lo converte in un oggetto Constant e lo inserisce nella pila.
           Se un token è presente nel dizionario dispatch, lo considera come un'operazione 
           e ne crea un'istanza utilizzando la classe corrispondente. 
           Prende gli argomenti necessari dalla pila e li utilizza per inizializzare l'operazione.
           Se un token inizia con il pattern "prog", lo considera come un blocco di sequenza 
           e crea un'istanza della classe Sequence. 
           Questo è utile per gestire i blocchi di istruzioni sequenziali nel programma.
           Se un token è una stringa alfabetica, lo considera come una variabile e crea 
           un'istanza della classe Variable.
           Se un token non è né numerico, né un'operazione, né un blocco di sequenza, né una variabile, 
           solleva un'eccezione UndefinedOperationException indicando un token non valido.
           
           Una volta analizzati tutti i token, se la pila contiene più di un elemento, 
           solleva un'eccezione InvalidExpressionException poiché l'espressione non è valida.
           Restituisce l'elemento rimanente nella pila, che dovrebbe essere l'espressione radice 
           dell'albero di espressioni.
           
           Output:

           Restituisce l'espressione radice dell'albero di espressioni costruito dal programma.

        '''

        stack = Stack()
        tokens = text.split()
        prog_pattern = "prog"

        for token in tokens:
            if token.isnumeric():
                stack.push(Constant(int(token)))
            elif token in dispatch:
                op_class = dispatch[token]
                if issubclass(op_class, Operation):
                    arity = op_class.arity
                    args = [stack.pop() for _ in range(arity)]
                    
                    stack.push(op_class(args))
            elif token.startswith(prog_pattern):
                prog_number = token[len(prog_pattern):]
                current_sequence = []
                while len(stack.data) != 0:
                    current_sequence.append(stack.pop())
                stack.push(Sequence(current_sequence, prog_number))
                
            elif token.isalpha():
                stack.push(Variable(token))
            else:
                raise UndefinedOperationException(f"Invalid token: {token}")
        if len(stack.data) != 1:
            raise InvalidExpressionException("Invalid expression")
        return stack.pop()     


    def evaluate(self, env):
        raise NotImplementedError()


class Variable(Expression):

    '''
        Metodi della classe:

        __init__(self, name):
            Costruttore della classe. 
            Prende un parametro name, che rappresenta il nome della variabile.
        
        evaluate(self, env):
            Metodo che valuta la variabile utilizzando un ambiente dato. 
            Se la variabile è presente nell'ambiente, restituisce il suo valore corrispondente. 
            Altrimenti, solleva un'eccezione MissingVariableException.
        
        __str__(self):
            Metodo che restituisce una rappresentazione in stringa della variabile, 
            che è semplicemente il suo nome.
  
    '''

    def __init__(self, name):
        self.name = name

    def evaluate(self, env):
        if self.name in env:
            return env[self.name]
        else:
            raise MissingVariableException(f"Variable '{self.name}' not found in the environment.")

    def __str__(self):
        return self.name


class Constant(Expression):

    '''
        Metodi della classe:

        __init__(self, value):
            Costruttore della classe. 
            Prende un parametro value, che rappresenta il valore della costante.
        
        evaluate(self, env):
            Metodo valuta la costante. 
            Poiché una costante ha sempre lo stesso valore, 
            restituisce semplicemente il valore memorizzato.
        
        __str__(self):
            Metodo restituisce una rappresentazione in stringa della costante,
            che è il suo valore convertito in stringa.
  
    '''

    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value

    def __str__(self):
        return str(self.value)


class Operation(Expression):

    '''
        Metodi della classe:

        __init__(self, args):
            Costruttore della classe. 
            Prende un parametro args, che rappresenta gli argomenti dell'operazione.
        
        evaluate(self, env):
            Questo metodo valuta l'operazione. 
            Prima valuta tutti gli argomenti dell'operazione nell'ambiente dato. 
            Quindi, chiama il metodo op (che deve essere implementato dalle sottoclassi) 
            per eseguire l'operazione utilizzando gli argomenti valutati.
        
        op(self, *args):
            Questo è un metodo astratto che deve essere implementato dalle sottoclassi. 
            Rappresenta l'operazione effettiva che l'istanza dell'operazione esegue.
            Prende gli argomenti valutati come parametri e restituisce il risultato dell'operazione.
        
        __str__(self):
        Questo metodo restituisce una rappresentazione in stringa dell'operazione. 
        Concatena il nome dell'operazione (op_str) con una stringa rappresentante 
        gli argomenti dell'operazione.

    '''

    def __init__(self, args):
        self.args = args

    def evaluate(self, env):
        evaluated_args = [arg.evaluate(env) if isinstance(arg, Expression) else arg for arg in self.args]
        return self.op(*evaluated_args)

    def op(self, *args):
        raise NotImplementedError()

    def __str__(self):
        args_str = " ".join([str(arg) for arg in self.args])
        return f"({self.op_str} {args_str})"


"""

    Sottoclassi di Operation in cui è specificatà l'arità dell'operazione

"""

class UnaryOp(Operation):
    arity = 1

class BinaryOp(Operation):
    arity = 2

class TernaryOp(Operation):
    arity = 3

class QuaternaryOp(Operation):
    arity = 4


""" 

    Operazioni matematiche

"""

class Addition(BinaryOp):
    op_str = "+"

    def op(self, x, y):
        return x + y


class Subtraction(BinaryOp):
    op_str = "-"

    def op(self, x, y):
        return x - y


class Division(BinaryOp):
    op_str = "/"

    def op(self, x, y):
        if y == 0:
            raise ValueError("Division by zero")
        return x / y


class Multiplication(BinaryOp):
    op_str = "*"

    def op(self, x, y):
        return x * y


class Power(BinaryOp):
    op_str = "**"

    def op(self, x, y):
        return x ** y


class Modulus(BinaryOp):
    op_str = "%"

    def op(self, x, y):
        return x % y


class Reciprocal(UnaryOp):
    op_str = "1/"

    def op(self, x):
        if x == 0:
            raise ValueError("Reciprocal of zero is undefined")
        return 1 / x


class AbsoluteValue(UnaryOp):
    op_str = "abs"

    def op(self, x):
        return abs(x)


"""

 Operazioni con operatori di confronto

"""

class GreaterThan(BinaryOp):
    op_str = ">"

    def op(self, x, y):
        return x > y


class LessThan(BinaryOp):
    op_str = "<"

    def op(self, x, y):
        return x < y


class GreaterThanOrEqual(BinaryOp):
    op_str = ">="

    def op(self, x, y):
        return x >= y


class LessThanOrEqual(BinaryOp):
    op_str = "<="

    def op(self, x, y):
        return x <= y


class Equal(BinaryOp):
    op_str = "="

    def op(self, x, y):
        return x == y

class NotEqual(BinaryOp):
    op_str = "!="

    def op(self, x, y):
        return x != y


"""

 Definizione di variabili

"""

class VarAlloc(UnaryOp):

    '''
        Metodi della classe:
        
        evaluate(self, env):
            Questo metodo valuta l'operazione di allocazione di variabili. 
            Estrae la variabile dagli argomenti e verifica se è un'istanza della classe Variable. 
            Se non lo è, solleva un'eccezione TypeError. 
            Altrimenti, aggiunge la variabile all'ambiente env con un valore iniziale di 0.
        
        __str__(self):
            Questo metodo restituisce una rappresentazione in stringa dell'operazione di allocazione. 
            Mostra il nome della variabile seguito dall'operatore di allocazione.
 
    '''

    op_str = "alloc"

    def evaluate(self, env):
        var = self.args[0]

        if not isinstance(var, Variable):
            raise TypeError("The variable must be an instance of the Variable class")
        env[var.name] = 0
        
    def __str__(self):
        return f"({self.args[0]} alloc)"
    

class ArrayAlloc(BinaryOp):
    
    '''
        Metodi della classe:

        evaluate(self, env):
            Questo metodo valuta l'allocazione di un array con valori di default impostati a 0. 
            Prende due argomenti: la variabile che rappresenta l'array e un'espressione n 
            che rappresenta la dimensione dell'array.
            Valuta l'espressione n nell'ambiente dato per calcolare la dimensione dell'array.
            Verifica se la variabile è un'istanza della classe Variable. 
            Se non lo è, solleva un'eccezione di tipo TypeError.
            Assegna all'ambiente la variabile come chiave e una lista vuota di lunghezza size 
            come valore, creando così l'array.
        
        __str__(self):
            Questo metodo restituisce una rappresentazione in stringa dell'operazione 
            di allocazione dell'array. 
            Concatena gli argomenti dell'operazione in una stringa separata da spazi 
            e restituisce una stringa formattata che rappresenta l'operazione.

    '''

    op_str = "valloc"

    def evaluate(self, env):
        var, n = self.args
        size = n.evaluate(env) # use n to calculate the size of the array
        if not isinstance(var, Variable):
            raise TypeError (f"The variable must be an instance of the Variable class")
        
        env[var.name] = [0] * size 

    def __str__(self):
        args_str = ' '.join(map(str, self.args))
        return f"{args_str} valloc"


class SetqOperation(BinaryOp):
    
    '''
        Metodi della classe:

        evaluate(self, env):
            Questo metodo valuta l'operazione "setq", che assegna un valore 
            a una variabile nell'ambiente. 
            Prende due argomenti: la variabile x e un'espressione expr 
            che rappresenta il valore da assegnare alla variabile.
            Verifica se x è un'istanza della classe Variable. 
            Se non lo è, solleva un'eccezione di tipo TypeError.
            Valuta l'espressione expr nell'ambiente dato per ottenere il valore 
            da assegnare alla variabile.
            Assegna il valore alla variabile nell'ambiente e restituisce il valore assegnato.
        
        __str__(self):
            Questo metodo restituisce una rappresentazione in stringa dell'operazione "setq". 
            Mostra il nome della variabile e il valore da assegnare, 
            separati da spazi e seguiti dalla parola "setq".

    '''

    op_str = "setq"

    def evaluate(self, env):
        x, expr = self.args
        
        if not isinstance(x, Variable):
            raise TypeError (f"The variable must be an instance of the Variable class")
        
        env[x.name] = expr.evaluate(env)
        return env[x.name]
    
    def __str__(self):
        
        args_str = ' '.join(map(str, self.args))
        return f"{args_str} setq"


class SetvOperation(TernaryOp):
    
    '''
        Metodi della classe:

        evaluate(self, env):
            Questo metodo valuta l'operazione "setv", 
            che assegna un valore a un elemento specifico di un array nell'ambiente. 
            Prende tre argomenti: la variabile x che rappresenta l'array, 
            un'espressione n che rappresenta l'indice dell'elemento nell'array 
            e un'espressione expr che rappresenta il valore da assegnare all'elemento.
            Valuta l'espressione n nell'ambiente dato per ottenere l'indice dell'elemento nell'array.
            Verifica se la variabile x è presente nell'ambiente e se il suo valore è una lista, 
            che rappresenta un array. 
            Se non lo è, solleva un'eccezione di tipo ValueError.
            Valuta l'espressione expr nell'ambiente dato per ottenere il valore da assegnare
            all'elemento dell'array.
            Assegna il valore all'elemento specificato dell'array nell'ambiente 
            e restituisce l'array modificato.
        
        __str__(self):
            Questo metodo restituisce una rappresentazione in stringa dell'operazione "setv". 
            Concatena gli argomenti dell'operazione in una stringa separata da spazi 
            e restituisce una stringa formattata che rappresenta l'operazione.
   
    '''

    op_str = "setv"

    def evaluate(self, env):
        x, n, expr = self.args
        index = n.evaluate(env)

        if x.name not in env or not isinstance(env[x.name], list):
            raise ValueError(f"{x.name} is not a valid array in the environment")
        
        value = expr.evaluate(env)
        env[x.name][index] = value
    
        return env[x.name]
    
    def __str__(self):
        args_str = ' '.join(map(str, self.args))
        return f"{args_str} setv"
    

"""

 Sequenze

"""

class Sequence(Expression):
    
    '''
        Metodi della classe:

        __init__(self, expressions, prog_number):
            Questo è il costruttore della classe. 
            Prende due argomenti: 
            expressions, che è una lista di espressioni da eseguire in sequenza, 
            e prog_number, che è il numero di sequenza associato a questa istanza della classe.
        
        evaluate(self, env):
            Questo metodo valuta la sequenza di espressioni. 
            Valuta ogni espressione nell'ambiente dato in ordine 
            e memorizza il risultato dell'ultima espressione valutata.
            Se è presente un numero di sequenza (prog_number), 
            aggiunge il risultato dell'ultima espressione valutata all'ambiente 
            con una chiave che usa il numero di sequenza.
        
        __str__(self):
            Questo metodo restituisce una rappresentazione in stringa della sequenza di espressioni. 
            Concatena le rappresentazioni in stringa di tutte le espressioni nella sequenza, 
            separate da spazi.
       
    '''

    def __init__(self, expressions, prog_number):
        self.expressions = expressions
        self.prog_number = prog_number

    def evaluate(self, env):

        result = None
        for expression in self.expressions:
            result = expression.evaluate(env)

        # Aggiunta del risultato all'ambiente con una chiave che usa il numero di sequenza, se presente
        if self.prog_number is not None:
            env[f'prog{self.prog_number}'] = result
        else:
            raise ValueError("Sequence number not declared")

        return result

    def __str__(self):
        
        return " ".join(map(str, self.expressions))  
    

"""

 Condizionali e iterazioni

"""
    
class If(TernaryOp):
    
    '''
        Metodi della classe:

        evaluate(self, env):
            Questo metodo valuta l'operazione "if". 
            Prende tre argomenti: cond, if_yes, e if_no, che rappresentano rispettivamente 
            la condizione, l'espressione da valutare se la condizione è vera 
            e l'espressione da valutare se la condizione è falsa.
            Valuta la condizione (cond) nell'ambiente dato. 
            Se la condizione restituisce un valore vero, 
            valuta l'espressione if_yes nell'ambiente e restituisce il suo risultato.
            Se la condizione è falsa, valuta l'espressione if_no nell'ambiente 
            e restituisce il suo risultato.
            Restituisce il valore dell'espressione valutata, che può essere o if_yes o if_no, 
            a seconda della valutazione della condizione.
            
        __str__(self):
            Questo metodo restituisce una rappresentazione in stringa dell'operazione "if". 
            Concatena gli argomenti dell'operazione in una stringa separata da spazi 
            e aggiunge "if" alla fine per indicare che si tratta di un'operazione condizionale.
       
    '''

    op_str = "if"

    def evaluate(self, env):

        cond, if_yes, if_no = self.args

        if (cond.evaluate(env) == True):
            return if_yes.evaluate(env)
        else:
            return if_no.evaluate(env)
    
    def __str__(self):
            
        args_str = ' '.join(map(str, self.args))
        return f"{args_str} if"
    

class While(BinaryOp):

    '''
        Metodi della classe:

        evaluate(self, env):
            Questo metodo valuta l'operazione "while". 
            Prende due argomenti: cond e expr, che rappresentano rispettivamente 
            la condizione da verificare e l'espressione da valutare finché la condizione è vera.
            Valuta la condizione (cond) nell'ambiente dato. 
            Se la condizione è vera, continua a valutare l'espressione expr nell'ambiente 
            fino a quando la condizione diventa falsa.
            Continua a eseguire il ciclo finché la condizione è vera.
            
        __str__(self):
            Questo metodo restituisce una rappresentazione in stringa dell'operazione "while". 
            Concatena gli argomenti dell'operazione in una stringa separata da spazi 
            e aggiunge "while" alla fine per indicare che si tratta di un'operazione di iterazione.
 
    '''

    op_str = "while"

    def evaluate(self, env):
        cond, expr = self.args

        while (cond.evaluate(env) == True):
            expr.evaluate(env)

    def __str__(self):
            
        args_str = ' '.join(map(str, self.args))
        return f"{args_str} while"


class For(QuaternaryOp):

    '''
        Metodi della classe:
        
        evaluate(self, env):
            Questo metodo valuta l'operazione "for". 
            Prende quattro argomenti: i_var, start_expr, end_expr e body_expr, 
            che rappresentano rispettivamente la variabile di iterazione, 
            l'espressione iniziale, l'espressione finale e il corpo dell'iterazione.
            Valuta le espressioni start_expr e end_expr nell'ambiente dato per ottenere 
            i valori di inizio e fine dell'iterazione.
            Verifica se i_var è un'istanza della classe Variable. 
            Se non lo è, solleva un'eccezione di tipo TypeError.
            Itera attraverso i valori da start a end - 1 per la variabile di iterazione i, 
            assegnando ogni valore a i_var nell'ambiente 
            e valutando il corpo dell'iterazione body_expr nell'ambiente.
            
        __str__(self):
            Questo metodo restituisce una rappresentazione in stringa dell'operazione "for". 
            Concatena gli argomenti dell'operazione in una stringa separata da spazi 
            e aggiunge "for" alla fine per indicare che si tratta di un'operazione di iterazione.
       
    '''

    op_str = "for"
    def evaluate(self, env):
        i_var, start_expr, end_expr, body_expr = self.args
        start = start_expr.evaluate(env)
        end = end_expr.evaluate(env)

        if not isinstance(i_var, Variable):
            raise TypeError("The variable must be an instance of the Variable class")

        for i in range(start, end):
            env[i_var.name] = i
            body_expr.evaluate(env)


    def __str__(self):
            
        args_str = ' '.join(map(str, self.args))
        return f"{args_str} for"
    

"""

 Subroutine

"""

class DefSub(BinaryOp):

    '''
        Metodi della classe:
        
        evaluate(self, env):
            Questo metodo valuta l'operazione "defsub", che associa un'espressione 
            a una variabile per creare una subroutine. 
            Prende due argomenti: f, che è la variabile a cui associare l'espressione, 
            e expr, che è l'espressione da associare.
            Verifica se f è un'istanza della classe Variable. 
            Se non lo è, solleva un'eccezione di tipo TypeError.
            Associa l'espressione expr alla variabile f nell'ambiente.
        
        __str__(self):
            Questo metodo restituisce una rappresentazione in stringa dell'operazione "defsub". 
            Concatena gli argomenti dell'operazione in una stringa separata da spazi 
            e aggiunge "defsub" alla fine per indicare che si tratta di un'operazione 
            di definizione di subroutine.

    '''

    op_str = "defsub"

    def evaluate(self, env):

        f, expr = self.args

        if not isinstance(f, Variable):
            raise TypeError (f"The variable must be an instance of the Variable class")
        
        env[f.name] = expr   

    def __str__(self):

        args_str = ' '.join(map(str, self.args))
        return f"{args_str} defsub"
    

class Call(UnaryOp):

    '''
        Metodi della classe:

        evaluate(self, env):
            Questo metodo valuta l'operazione "call", che esegue un'espressione associata 
            a una variabile precedentemente definita utilizzando l'operazione "defsub". 
            Prende un solo argomento: f, che è la variabile che contiene l'espressione da eseguire.
            Verifica se f è un'istanza della classe Variable. 
            Se non lo è, solleva un'eccezione di tipo TypeError.
            Ottiene l'espressione associata alla variabile f dall'ambiente. 
            Se l'espressione non è definita (vale None), solleva un'eccezione di tipo ValueError.
            Verifica se l'espressione è un'istanza della classe Expression. 
            Se non lo è, solleva un'eccezione di tipo TypeError.
            Valuta l'espressione nell'ambiente dato e restituisce il suo risultato.
        
        __str__(self):
            Questo metodo restituisce una rappresentazione in stringa dell'operazione "call". 
            Concatena l'argomento dell'operazione in una stringa formattata che indica 
            che si tratta di una chiamata a subroutine.

    '''

    op_str = "call"
    
    def evaluate(self, env):

        f = self.args[0]

        if not isinstance(f, Variable):
            raise TypeError (f"The variable must be an instance of the Variable class")
        
        expr = env[f.name]

        if expr is None:
            raise ValueError(f"Subroutine '{f}' not defined")
        
        elif not isinstance(expr, Expression):
            raise TypeError (f"The expression must be an instance of the Expression class")

        return expr.evaluate(env)  
    
    def __str__(self):
        return f"({self.args[0]} call)"


"""

 Funzioni aggiuntive: print e operazione nulla

"""

class Print(UnaryOp):

    '''
        Metodi della classe:

        evaluate(self, env):
            Questo metodo valuta l'operazione "print", che valuta un'espressione 
            e stampa il risultato. 
            Prende un solo argomento: expr, che è l'espressione da valutare e stampare.
            Valuta l'espressione nell'ambiente dato e memorizza il risultato.
            Stampa il risultato utilizzando la funzione print().
            Restituisce il risultato dell'espressione valutata.
        
        __str__(self):
            Questo metodo restituisce una rappresentazione in stringa dell'operazione "print". 
            Concatena l'argomento dell'operazione in una stringa formattata che indica 
            che si tratta di un'operazione di stampa.

    '''

    op_str = "print"

    def evaluate(self, env):
        expr = self.args[0]
        result = expr.evaluate(env)
        print(result)
        return result
    
    def __str__(self):
        return f"({self.args[0]} print)"   


class Nop(Operation):

    '''
        Metodi della classe:

        op(self):
            Questo metodo rappresenta l'operazione effettiva dell'operazione "nop" (no-operation). 
            Poiché "nop" non effettua alcuna operazione, questo metodo è vuoto e non fa nulla.
       
    '''

    arity = 0 # specifo l'arità, che in questo caso, per l'operazione nulla è uguale a 0

    op_str = "nop"

    def op(self):
        return

"""

    Main

"""

d = {"+": Addition, "*": Multiplication, "**": Power, "-": Subtraction,
     "/": Division, "%": Modulus, "1/": Reciprocal, "abs": AbsoluteValue, ">": GreaterThan,
     "<": LessThan, ">=": GreaterThanOrEqual, "<=": LessThanOrEqual,
     "=": Equal, "!=": NotEqual, "alloc": VarAlloc, "valloc": ArrayAlloc,
     "setq": SetqOperation, "setv": SetvOperation, "prog": Sequence,
     "if": If, "while": While, "for": For,
     "defsub": DefSub, "call": Call, "print": Print, "nop": Nop}


# Esempio operatorii matematici - Esercitazione 11
example = "2 3 + x * 6 5 - / abs 2 ** y 1/ + 1/"
e = Expression.from_program(example, d)
print(e)
res = e.evaluate({"x": 3, "y": 7})
print(res)

# Ouput atteso:
# (1/ (+ (1/ y) (** 2 (abs (/ (- 5 6) (* x (+ 3 2)))))))
# 0.84022932953024

# Esempi forniti nella consegna e su teams

expr2 = "x 1 + x setq x 10 > while x alloc prog2"
expr3 = "v print i i * i v setv prog2 10 0 i for 10 v valloc prog2"
expr4 = "x print f call x alloc x 4 + x setq f defsub prog4"
expr5 = "nop i print i x % 0 = if 1000 2 i for 783 x setq x alloc prog3"
expr6 = "nop x print prime if nop 0 0 != prime setq i x % 0 = if 1 x - 2 i for 0 0 = prime setq prime alloc prog4 100 2 x for"
expr7 = "v print i j * 1 i - 10 * 1 j - + v setv 11 1 j for 11 1 i for 100 v valloc prog3"
expr8 = "x print 1 3 x * + x setq 2 x / x setq 2 x % 0 = if prog2 1 x != while 50 x setq x alloc prog3"

expressions = [expr2, expr3, expr4, expr5, expr6, expr7, expr8]

for expr in expressions:
    try:
        e = Expression.from_program(expr, d)
        print(e)
        res = e.evaluate({})
        print(res)
        print("\n")
    except Exception as exc:
        print(f"An error has occurred: {exc}")
        