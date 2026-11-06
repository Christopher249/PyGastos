import json
import math
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "gastos.json"


def cargar_gastos():
    """Carga los gastos guardados en el archivo JSON."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        print("No se pudieron leer los gastos guardados.")
        return []


def guardar_gastos(gastos):
    """Guarda los gastos en un archivo JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with DATA_FILE.open("w", encoding="utf-8") as archivo:
        json.dump(gastos, archivo, indent=4, ensure_ascii=False)


def registrar_gasto(gastos):
    descripcion = input("Descripción del gasto: ").strip()

    if not descripcion:
        print("La descripción no puede estar vacía.")
        return

    try:
        # Aceptamos coma o punto decimal: 18,50 o 18.50
        monto = float(input("Monto del gasto (S/): ").replace(",", "."))
    except ValueError:
        print("Ingresa un monto válido.")
        return

    if not math.isfinite(monto) or monto <= 0:
        print("El monto debe ser un número mayor que cero.")
        return

    gastos.append({
        "descripcion": descripcion,
        "monto": round(monto, 2)
    })

    guardar_gastos(gastos)
    print("¡Gasto registrado correctamente!")


def mostrar_gastos(gastos):
    if not gastos:
        print("Todavía no tienes gastos registrados.")
        return

    print("\n--- LISTA DE GASTOS ---")

    for numero, gasto in enumerate(gastos, start=1):
        print(
            f"{numero}. {gasto['descripcion']}: "
            f"S/ {gasto['monto']:.2f}"
        )

    total = sum(gasto["monto"] for gasto in gastos)
    print(f"\nTotal gastado: S/ {total:.2f}")


def main():
    gastos = cargar_gastos()

    while True:
        print("\n=== PyGastos ===")
        print("1. Registrar gasto")
        print("2. Mostrar gastos")
        print("3. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            registrar_gasto(gastos)
        elif opcion == "2":
            mostrar_gastos(gastos)
        elif opcion == "3":
            print("¡Gracias por usar PyGastos!")
            break
        else:
            print("Opción no válida. Intenta nuevamente.")


if __name__ == "__main__":
    main()