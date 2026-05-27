import csv
import matplotlib.pyplot as plt 
import numpy as np
import os

ruta_archivo = r"/content/TP_Organizacion_Ventas/Repo-Proyecto/Datos/Ventas.txt"
# Nueva ruta para guardar el gráfico PNG
ruta_grafico = r"/content/TP_Organizacion_Ventas/Repo-Proyecto/Resultados/graficoVentas.png"

lista_ventas = []
cantidades_por_producto = {}
analisis_mensual = {}
AcumVendidos = 0

try:
    with open(ruta_archivo, mode="r", encoding="utf-8-sig") as archivo:
        lector_dict = csv.DictReader(archivo, delimiter=';')
        
        for fila in lector_dict:
            fila = {k.strip(): v for k, v in fila.items()}
            
            producto = fila["Producto"]
            cantidad = int(fila["CantidadVendida"])
            mes = fila["FechaVenta"][:7] # Extrae "AAAA-MM"
            
            # Guardamos en la lista general
            lista_ventas.append({
                "Producto": producto,
                "Cantidad": cantidad,
                "Precio": float(fila["Precio"]),
                "Fecha": fila["FechaVenta"]
            })
            
            # 1. Acumular unidades por nombre de producto
            cantidades_por_producto[producto] = cantidades_por_producto.get(producto, 0) + cantidad
            
            # 2. Análisis por mes: Transacciones y Unidades Totales
            if mes not in analisis_mensual:
                analisis_mensual[mes] = {"transacciones": 0, "unidades_totales": 0}
            
            analisis_mensual[mes]["transacciones"] += 1
            analisis_mensual[mes]["unidades_totales"] += cantidad

    # --- REPORTE FINAL ---
    if lista_ventas:
        # Producto más vendido
        producto_top = max(cantidades_por_producto, key=cantidades_por_producto.get)
        
        print(f"--- REPORTE DE VENTAS ---")
        print(f"Producto más vendido: {producto_top} ({cantidades_por_producto[producto_top]} unidades)")
        
        print(f"\n{'Mes':<10} | {'Ventas (Filas)':<15} | {'Productos Totales':<18}")
        print("-" * 50)
        
        # Ordenamos los meses cronológicamente para el reporte y el gráfico
        meses_ordenados = sorted(analisis_mensual.keys())
        
        for mes in meses_ordenados:
            v = analisis_mensual[mes]
            print(f"{mes:<10} | {v['transacciones']:<15} | {v['unidades_totales']:<18}")
            AcumVendidos = AcumVendidos + v['unidades_totales']
        
        # --- CONFIGURACIÓN DEL GRÁFICO ---
        ejex_meses = meses_ordenados
        ejey_unidades = [analisis_mensual[m]["unidades_totales"] for m in meses_ordenados]
        
        plt.figure(figsize=(10, 5))
        plt.plot(ejex_meses, ejey_unidades, marker='o', color='blue', linewidth=2)
        
        plt.title("Gráfico de Ventas por mes")
        plt.xlabel("Meses")
        plt.ylabel("Unidades Vendidas")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # --- Asegurar que la carpeta 'Resultados' exista antes de guardar ---
        carpeta_resultados = os.path.dirname(ruta_grafico)
        if not os.path.exists(carpeta_resultados):
            os.makedirs(carpeta_resultados)
            
        # Guardar gráfico en la ruta específica de Resultados
        plt.savefig(ruta_grafico, dpi=300)
        plt.close()
        
        print(f"\nTotal de productos vendidos: {AcumVendidos}")
        print(f"El gráfico se ha guardado con éxito en:\n{ruta_grafico}")
        
    else:
        print("No hay datos para mostrar.")

except Exception as e:
    print(f"Error general: {e}")