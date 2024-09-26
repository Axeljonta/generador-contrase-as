import random as rd
import string as st
import sqlite3 as sql
import pandas as pd

#creador de contraseña
def crear_contraseña(longitud, mayus, nums, esp):
    caracteres = st.ascii_uppercase
    if mayus:
       caracteres += st.ascii_lowercase
    if nums:
       caracteres += st.digits
    if esp:
       caracteres += st.punctuation
    contraseña = ''.join(rd.choice(caracteres) for i in range(longitud))
    return contraseña

#para asegurarnos que mo ingresen una letra en vez de un numero
def obtener_entero(m):
 while True:
    try:
        var = input(m)
        entero = int(var)
        return entero
    except ValueError:
        print('Ingresar un numero por favor')

#almacenar contraseñas en sql
def almacenar_contraseña(nombre_usuario, contraseña):
    conexion = sql.connect('gestor_contraseñas.db')
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contraseñas (nombre_usuario TEXT, contraseña BLOB, PRIMARY KEY("nombre_usuario"))''')
    cursor.execute('''INSERT INTO contraseñas (nombre_usuario, contraseña) VALUES (?, ?)''', (nombre_usuario, contraseña))
    conexion.commit()
    conexion.close()

def ver_contraseñas():
    conexion = sql.connect('gestor_contraseñas.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM contraseñas')
    resultado = cursor.fetchall()
    resultado_df = pd.DataFrame(resultado)
    return resultado_df

def main(): 
    print('Bienverido al creador de contraseñas: ')
    while True:
        menu = input('''
                    1- Crear contraseña
                    2- Ver contraseñas guardadas
                    3- Salir del programa
                    ''')
        if menu == '1':
                while True:
                    #pedimos mail
                    nombre = input('Introduzca su nombre de usuario: ')
                    #longuitud de contradeña
                    longitud = obtener_entero('Por favor, ingresa la cantidad de caracteres para la contraseña (mínimo 8): ') 
                    #nos aseguramos que la contraseña dea de mas de 8 caracterees
                    while longitud < 8 : 
                            print('La longitud tiene que ser mayor a 8')
                            longitud = obtener_entero('Cantidad de caracteres de tu contraseña (mínimo 8): ')
                    mayusculas = input('Quieres que la contraseña contenga mayusculas (s/n):').lower() == 's'
                    numeros = input('Quieres que la contraseña contenga numeros (s/n):').lower() == 's'
                    especiales = input('Quieres que la contraseña contenga caracteres especiales (s/n):').lower() == 's'
                    contraseña = crear_contraseña(longitud, mayusculas, numeros, especiales )
                    almacenar_contraseña(nombre, contraseña)
                    
                    print (f'La contraseña creada es: {contraseña}')
                        
                    salida = input('''
                                    Quieres crear una otra contraseña 
                                    1-Si 2-No 
                                    ''') == '2'
                    if salida: 
                        break
        elif menu == '2':
            tabla = ver_contraseñas()
            print(tabla)

        else: 
         break
    print('Hasta luego!')
            

if __name__ == "__main__":
    main()