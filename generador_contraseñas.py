import random as rd
import string as st
import sqlite3 as sql
import pandas as pd
import re
import bcrypt

#validar correo
def validar_correo(email):
   patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
   if re.match(patron, email):
       return True
   else:
       return False

#crear tabla usuario 
def crear_tabla_usuario():
    conexion = sql.connect('gestor_contraseñas.db')
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        email TEXT UNIQUE,
                        contraseña_hash BLOB)''')
    conexion.commit()
    conexion.close()

#Crear la tabla de contraseñas 
def crear_tabla_contraseñas():
    conexion = sql.connect('gestor_contraseñas.db')
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contraseñas (
                        servicio TEXT,
                        email TEXT,
                        contraseña_hash BLOB,
                        FOREIGN KEY(email) REFERENCES usuarios(email)
                    )''')
    conexion.commit()
    conexion.close()

#alacenar usuario
def almacenar_usuario(email, contraseña):
    conexion = sql.connect('gestor_contraseñas.db')
    cursor = conexion.cursor()

    #Hashear la contraseña
    contraseña_hash = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

    #para manejar errores por si ingresan un mail existente
    try:
        cursor.execute('''INSERT INTO usuarios (email, contraseña_hash)
                    VALUES (?, ?)''', (email, contraseña_hash))
        conexion.commit()
        print('Usuario registrado correctamente')
    except sql.IntegrityError:
        print("Error: El correo electrónico ya está registrado.")
    conexion.close()

#almacenar contraseñas
def almacenar_contraseña(email, servicio , contraseña_nueva):
    conexion = sql.connect('gestor_contraseñas.db')
    cursor = conexion.cursor()

    # Generar el hash de la nueva contraseña
    salt = bcrypt.gensalt()
    contraseña_hash = bcrypt.hashpw(contraseña_nueva.encode('utf-8'), salt)
    
    cursor.execute('''INSERT INTO contraseñas (email, servicio, contraseña_hash)
                   VALUES (?, ?, ?)''', (email,servicio, contraseña_hash))
    conexion.commit()
    conexion.close()

#Ver contraseña
def ver_contraseñas(email):
    conexion = sql.connect('gestor_contraseñas.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT servicio, email, contraseña_hash FROM contraseñas WHERE email = ?', (email,))
    resultado = cursor.fetchall()
    resultado_df = pd.DataFrame(resultado)
    conexion.close()
    return resultado_df


#validar usuario
def validar_usuario(email,contraseña):
    conexion = sql.connect('gestor_contraseñas.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT email, contraseña_hash FROM usuarios WHERE email = ?',(email,))
    
    #obteniendo resultado de la consulta.
    resultado = cursor.fetchone()
    
    conexion.close()

    if resultado:
        email, contraseña_hash = resultado
        #verificar si la contraseña ingresada coincide con la almacenada 
        if bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_hash):
            print("Inicio de sesión exitoso.")
            return email
        else:
            print("Contraseña incorrecta.")
    else:
        print("Correo electrónico no registrado.")
    
    return None

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

#Manejo de error, para asegurarnos que no ingresen una letra en vez de un numero
def obtener_entero(m):
 while True:
    try:
        var = input(m)
        entero = int(var)
        return entero
    except ValueError:
        print('Ingresar un numero por favor')


#entrada del programa
def main():

    #creando tablas si no existen
    crear_tabla_usuario()
    crear_tabla_contraseñas()

    #bienvenida
    print('Bienverido al creador de contraseñas: ')

    while True:
            
            #menu iniciar sesión
            print('''
                    1 - Ingresar
                    2 - Crear usuario
                    3 - Salir
                    ''')
            opcion_usuario = input("Elige una opción: ")

            #ingreso cuenta ya existente
            if opcion_usuario == '1' :
                email = input('Ingresa tu correo: ')
                contraseña= input('Ingresa tu contraseña: ')
                login_usuario = validar_usuario(email,contraseña)

                if login_usuario:

                    #Gestion de contraseñas si el login es exitoso
                    while True:
                        print('''
                        1- Crear contraseña
                        2- Ver contraseñas
                        3- Salir del programa
                        ''')
                        opcion = input("Elige una opción: ")

                        #creando contraseña
                        if opcion == '1':
                                while True:

                                    #introducir servicio
                                    servicio = input('Introduce el nombre del servicio (ej. Gmail, Facebook): ')
                                    
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
                                    
                                    #almacenamos contraseña en sql
                                    almacenar_contraseña(login_usuario, servicio, contraseña)

                                    print (f'La contraseña creada es: {contraseña}')

                                    salida = input('''
                                                    Quieres crear una otra contraseña
                                                    1-Si 2-No
                                                    ''') == '2'
                                    if salida:
                                        break
                        
                        #Ver contraseñas creadas
                        elif opcion == '2':
                            tabla = ver_contraseñas(email)
                            print(tabla)

                        #salir del programa
                        else:
                         break
            
            elif opcion_usuario == '2':
                while True :
                    #pedimos el mail
                    email = input('Ingresa tu correo electronico: ')
                    if validar_correo(email):
                        break
                    else:
                        print('Correo no valido')
                contraseña = input('Ingresa tu contraseña: ')
                almacenar_usuario(email, contraseña)

            elif opcion_usuario == '3':
                print('Saliendo...')
                break

            else:
                print('Opcion no valida.')

    print('Hasta luego!')


if __name__ == "__main__":
    main()


