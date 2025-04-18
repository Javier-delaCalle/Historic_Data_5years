import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import statistics
import os

def obtener_datos_y_analisis(ticker_symbol):
    print(f"\nProcesando el ticker: {ticker_symbol}")
    # Fechas para últimos 5 años
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=5*365)
    
    stock = yf.Ticker(ticker_symbol)
    datos = stock.history(start=start, end=end)
    
    if datos.empty:
        print(f"No se han obtenido datos para {ticker_symbol}. Verifica el símbolo o tu conexión.")
        return
    else:
        print(f"\nDatos obtenidos para {ticker_symbol}:")
        print(datos.head())
        
        # Calcular la variación diaria en porcentaje
        datos['Daily Return'] = datos['Close'].pct_change() * 100
        # Formatear la variación diaria para que aparezca como porcentaje con dos decimales
        datos['Daily Return'] = datos['Daily Return'].apply(lambda x: f"{x:.2f}%".replace('.', ','))
        
        initial_price = datos['Close'].iloc[0]
        final_price = datos['Close'].iloc[-1]
        total_return = (final_price / initial_price - 1) * 100
        years = (end - start).days / 365.25
        annualized_return = (final_price / initial_price) ** (1 / years) - 1
        
        geometric_mean_close = statistics.geometric_mean(datos['Close'])
        
        print(f"\nVariación total en 5 años: {total_return:.2f}%")
        print(f"Rentabilidad anualizada: {annualized_return*100:.2f}%")
        print(f"Media geométrica del precio de cierre: {geometric_mean_close:.2f}")
        
        columnas_numericas = datos.select_dtypes(include=['float', 'int']).columns
        datos[columnas_numericas] = datos[columnas_numericas].round(2)
        
        # Crear la carpeta para CSV en el mismo directorio del script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        carpeta_csv = os.path.join(script_dir, "CSV_Files")
        if not os.path.exists(carpeta_csv):
            os.makedirs(carpeta_csv)
        
        csv_filename = os.path.join(carpeta_csv, f"{ticker_symbol}_5_anos.csv")
        try:
            datos.to_csv(csv_filename, sep=';', float_format="%.2f", decimal=',')
            print(f"\nDatos exportados correctamente a '{csv_filename}'.")
        except Exception as e:
            print(f"Error al exportar CSV: {e}")
        
        # Graficar los datos
        plt.figure(figsize=(14, 10))
        plt.suptitle(f"Gráfica 5 años: {ticker_symbol}", fontsize=16)
        
        plt.subplot(2, 1, 1)
        plt.plot(datos.index, datos['Close'], label='Precio de Cierre', color='blue')
        plt.ylabel('Precio ($)')
        plt.legend()
        
        daily_return_numeric = datos['Close'].pct_change() * 100
        plt.subplot(2, 1, 2)
        plt.plot(datos.index, daily_return_numeric, label='Variación Diaria (%)', color='orange')
        plt.xlabel('Fecha')
        plt.ylabel('Porcentaje (%)')
        plt.legend()
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()
        # Cerrar todas las figuras para asegurar que se retoma el código
        plt.close('all')

def menu():
    print("\nBienvenido al analizador financiero en Python")
    print("Seleccione un ticker de las opciones a continuación:")
    print("1. ETF S&P 500 Vanguard (VOO)")
    print("2. ETF EURO STOXX SPDR (FEZ)")
    print("3. Invesco Physical Gold ETC (8PSG.DE)")
    print("4. EUR Govt. Bond 15-30y iShares (IBCL.DE)")
    print("5. US Treasury Bond 0-1y iShares (IB01.L)")
    print("6. Ingresar otro ticker manualmente")
    opcion = input("Ingrese el número de su opción: ")
    
    if opcion == "1":
        return "VOO"
    elif opcion == "2":
        return "FEZ"
    elif opcion == "3":
        return "8PSG.DE"
    elif opcion == "4":
        return "IBCL.DE"
    elif opcion == "5":
        return "IB01.L"
    elif opcion == "6":
        ticker_manual = input("Ingrese el símbolo del ticker: ").strip().upper()
        if ticker_manual:
            return ticker_manual
        else:
            print("No se ingresó un ticker válido.")
            return None
    else:
        print("Opción no válida.")
        return None

if __name__ == "__main__":
    pd.set_option("display.max_rows", None)
    
    while True:
        ticker = menu()
        if ticker:
            obtener_datos_y_analisis(ticker)
        else:
            print("\nEl programa se ha detenido debido a un error en la selección del ticker.")
        
        opcion = input("\n¿Desea analizar otro ticker? (s/n): ").strip().lower()
        if opcion != "s":
            print("\nPrograma finalizado.")
            break
