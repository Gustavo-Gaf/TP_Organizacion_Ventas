import csv

ruta_archivo = r"C:\Users\Guguisino\OneDrive\Escritorio\Trabajo Practico - Ventas\TP_Organizacion_Ventas\Repo-Proyecto\Datos\Ventas.txt"

lista_ventas = []
cantidades_por_producto = {}
# Ahora guardará: {"AAAA-MM": {"transacciones": 0, "unidades_totales": 0}}
analisis_mensual = {}
AcumVendidos = 0

try:
    with open(ruta_archivo, mode="r", encoding="utf-8-sig") as archivo:
        lector_dict = csv.DictReader(archivo, delimiter=';')
        
        for fila in lector_dict:
            fila = {k.strip(): v for k, v in fila.items()}
            
            producto = fila["Producto"]
            cantidad = int(fila["CantidadVendida"])
            mes = fila["FechaVenta"][:7]
            
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
        
        for mes in sorted(analisis_mensual.keys()):
            v = analisis_mensual[mes]
            print(f"{mes:<10} | {v['transacciones']:<15} | {v['unidades_totales']:<18}")
            AcumVendidos = AcumVendidos + v['unidades_totales']; 
    else:
        print("No hay datos para mostrar.")

    
    print(f"Producto más vendido: {producto_top} ({cantidades_por_producto[producto_top]} unidades)")
    print(f"Total de productos vendidos: {AcumVendidos}")

except Exception as e:
    print(f"Error: {e}")