import random as rd
import string as st

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


def obtener_entero(m):
 while True:
    try:
        var = input(m)
        entero = int(var)
        return entero
    except ValueError:
        print('Ingresar un numero por favor')

def main(): 
    while True:
       longitud = obtener_entero('Cantidad de caracteres de tu contraseña (mínimo 8): ') 
       while longitud < 8 : 
            print('La longitud tiene que ser mayor a 8')
            longitud = obtener_entero('Cantidad de caracteres de tu contraseña (mínimo 8): ')
       mayusculas = input('Quieres que la contraseña contenga mayusculas (s/n):').lower() == 's'
       numeros = input('Quieres que la contraseña contenga numeros (s/n):').lower() == 's'
       especiales = input('Quieres que la contraseña contenga caracteres especiales (s/n):').lower() == 's'
       contraseña = crear_contraseña(longitud, mayusculas, numeros, especiales )
        
       print (f'La contraseña creada es: {contraseña}')
        
       salida = input('''
                      Quieres crear una otra contraseña 
                    1-Si 2-No 
                     ''') == '2'
       if salida: 
          break
    
    print('Hasta luego!')
        

if __name__ == "__main__":
    main()