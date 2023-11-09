import pyodbc
import csv
import sys
from datetime import datetime

# Parámetro recibido por línea de comandos
codigo_local = sys.argv[1]


# Actualizar FECHA_SINCRONIZACION con la fecha y hora actual para los registros obtenidos
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=master;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

# Actualizar FECHA_SINCRONIZACION para los registros obtenidos
update_query = f"UPDATE FPERUANAS.dbo.PRODUCTO_STOCK SET FECHA_SINCRONIZACION = GETDATE() WHERE CODIGO_LOCAL = ?"
cursor.execute(update_query, codigo_local)

# Confirmar la actualización
conn.commit()

# Cerrar la conexión a la base de datos
conn.close()


# Conexión a la base de datos
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=master;'
                      'Trusted_Connection=yes;')

# Crear un cursor para ejecutar consultas
cursor = conn.cursor()

# Consulta SQL para obtener los datos filtrados por CODIGO_LOCAL
sql_query = f"SELECT CODIGO_LOCAL, CODIGO_PRODUCTO, STOCK, FECHA_SINCRONIZACION FROM FPERUANAS.dbo.PRODUCTO_STOCK WHERE CODIGO_LOCAL = ?"
cursor.execute(sql_query, codigo_local)

# Obtener los resultados
results = cursor.fetchall()

# Cerrar la conexión a la base de datos
conn.close()

# Guardar los resultados en un archivo CSV
csv_filename = f"resultados_{codigo_local}.csv"
with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Escribir encabezados
    csv_writer.writerow(['CODIGO_LOCAL', 'CODIGO_PRODUCTO', 'STOCK', 'FECHA_SINCRONIZACION'])
    # Escribir filas de resultados
    csv_writer.writerows(results)



print(f"Resultados guardados en {csv_filename}. Registros actualizados con fecha y hora actual.")
