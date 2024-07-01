import tkinter as tk
from tkinter import scrolledtext, messagebox
import ply.lex as lex
import ply.yacc as yacc

import sys

sys.stderr = open("yacc_debug.log", "w")

# Desactivar la depuración de yacc
yacc.debug = False


# Definición del analizador léxico (Lexer)
tokens = (
    'ID',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'EQUALS',
    'SEMICOLON',
)

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_SEMICOLON = r';'

# Token para identificadores (nombres de variables)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Token para números enteros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios y tabuladores
t_ignore = ' \t'

# Manejar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejar errores de caracteres no reconocidos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Definición del analizador sintáctico (Parser)
def p_statements(p):
    '''
    statements : statements statement
               | statement
    '''

def p_statement_assign(p):
    'statement : ID EQUALS expression SEMICOLON'
    variables[p[1]] = p[3]

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_divide(p):
    'term : term DIVIDE factor'
    if p[3] != 0:
        p[0] = p[1] / p[3]
    else:
        raise ZeroDivisionError('división por cero')

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_factor_id(p):
    'factor : ID'
    if p[1] not in variables:
        messagebox.showerror("Error", f"Variable '{p[1]}' no definida.")
        p[0] = 0
    else:
        p[0] = variables[p[1]]

def p_error(p):
    print("Error de sintaxis!")

parser = yacc.yacc()

# Variables globales para almacenar las variables
variables = {}

# Función para ejecutar el análisis semántico
def ejecutar_analisis_semantico():
    codigo = texto_entrada.get("1.0", tk.END)
    lexer.input(codigo)
    while True:
        tok = lexer.token()
        if not tok:
            break
    try:
        # Limpiar tabla de variables antes de ejecutar el análisis
        variables.clear()

        # Ejecutar análisis sintáctico y semántico
        parser.parse(codigo, lexer=lexer)

        texto_salida.delete("1.0", tk.END)
        texto_salida.insert(tk.END, f"Variables definidas: {variables}\n")
    except Exception as e:
        texto_salida.delete("1.0", tk.END)
        texto_salida.insert(tk.END, f"Error: {str(e)}\n")

# Configuración de la interfaz gráfica
raiz = tk.Tk()
raiz.title("Analizador Semántico by Bryan Marc 1190040")
raiz.geometry("800x600")
raiz.configure(bg='#1f1f1f')

etiqueta_entrada = tk.Label(raiz, text="Ingrese código:", fg="white", bg='#1f1f1f')
etiqueta_entrada.pack(pady=10)

texto_entrada = scrolledtext.ScrolledText(raiz, height=10, wrap=tk.WORD, bg='#333333', fg='white', insertbackground='white')
texto_entrada.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
texto_entrada.insert(tk.END, "a = 10;\n")
texto_entrada.insert(tk.END, "b = 5;\n")
texto_entrada.insert(tk.END, "resultado = (a + b) * 2;\n")

boton_ejecutar = tk.Button(raiz, text="Ejecutar", command=ejecutar_analisis_semantico, bg='#4CAF50', fg='white', relief=tk.FLAT)
boton_ejecutar.pack(pady=10)

etiqueta_salida = tk.Label(raiz, text="Salida:", fg="white", bg='#1f1f1f')
etiqueta_salida.pack(pady=10)

texto_salida = scrolledtext.ScrolledText(raiz, height=10, wrap=tk.WORD, bg='#333333', fg='white', insertbackground='white')
texto_salida.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

raiz.mainloop()
