import pandas as pd

# Definir la lista de códigos de interés
codigos_interes = [
    "250350001000000060801800000000"
    # Agrega aquí todos los códigos de interés
]

# Cargar datos exportados
local_construccion = pd.read_csv('cun25035_local_construccion.csv')
prod_construccion = pd.read_csv('cun25035_final_construccion.csv')

# Filtrar registros que contengan los códigos de interés
local_construccion_filtrado = local_construccion[local_construccion['codigo'].isin(codigos_interes)]
prod_construccion_filtrado = prod_construccion[prod_construccion['codigo'].isin(codigos_interes)]

# Campos que usaremos para la comparación (excluyendo el ID)
campos_comparacion = ['codigo', 'geometria']

# Crear un DataFrame con los campos de comparación para evitar problemas con el ID
local_construccion_comparacion = local_construccion_filtrado[campos_comparacion]
prod_construccion_comparacion = prod_construccion_filtrado[campos_comparacion]

# Encontrar diferencias (registros faltantes en producción)
diff_construccion = pd.merge(local_construccion_comparacion, prod_construccion_comparacion, 
                       on=campos_comparacion, 
                       how='outer', 
                       indicator=True)

registros_faltantes_construcciones = diff_construccion[diff_construccion['_merge'] == 'left_only']

# Mostrar registros faltantes en producción
print("Registros faltantes en producción para la tabla predio:")
print(registros_faltantes_construcciones)

# Opcional: Unir los registros faltantes con el DataFrame original para obtener todos los campos
registros_faltantes_detallados = pd.merge(registros_faltantes_construcciones, 
                                          local_construccion_filtrado, 
                                          on=campos_comparacion, 
                                          how='left')

# Guardar los registros faltantes en un archivo CSV para su posterior revisión
registros_faltantes_detallados.to_csv('registros_faltantes_construcciones.csv', index=False)
