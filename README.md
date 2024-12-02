# Compresor
Se removio el texto 1 porque demoraba mucho y creimos que era un loop infinito. pero esto se arreglo.
Ahora solo se demora 20 minutos. 
Los demas entre 30 segundos a 2 minutos

Aparte de eso el paralelo corrido en un contenedor bota alrededor de p errores donde p es la cantidad de procesos. Pero el proceso padre termina correctamente y la compresion es exitosa

Lo otro malo es que la compresion del arabe es muy minima, una iteracion del programa encontraba 10mil palabras distintas para comprimir. pero como ese codigo dejaba un espacio en el diccionari (asi: 1: palabra) el cambio lo da;o para el arabe y ahora solo encuentra unas cuantas decenas para una compresion de 5kb
