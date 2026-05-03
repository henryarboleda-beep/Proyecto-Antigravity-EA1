import json
import random
from datetime import datetime, timedelta

def generar_datos():
    sensores = []
    current_id = 1
    
    tipos_config = [
        {"sensor_id": 1, "type": "temperatura", "min": -10, "max": 100,
         "start": datetime(2026, 1, 5, 6, 0, 0)},
        {"sensor_id": 2, "type": "presion", "min": 0, "max": 500,
         "start": datetime(2026, 2, 10, 10, 0, 0)},
        {"sensor_id": 3, "type": "velocidad", "min": 0, "max": 150,
         "start": datetime(2026, 3, 15, 14, 0, 0)},
    ]
    
    for config in tipos_config:
        tiempo = config["start"]
        for i in range(200):
            val = random.uniform(config["min"], config["max"])
            sensores.append({
                "id": current_id,
                "sensor_id": config["sensor_id"],
                "type": config["type"],
                "value": round(val, 2),
                "timestamp": tiempo.strftime("%Y-%m-%dT%H:%M:%S")
            })
            current_id += 1
            # Avanzar entre 2 y 8 horas aleatorias para dispersar las fechas
            tiempo += timedelta(hours=random.randint(2, 8),
                                minutes=random.choice([0, 15, 30, 45]))
            
    with open("sensores.json", "w", encoding="utf-8") as f:
        json.dump(sensores, f, indent=2, ensure_ascii=False)
        
    # Imprimir resumen de rangos
    for config in tipos_config:
        registros = [s for s in sensores if s["sensor_id"] == config["sensor_id"]]
        fechas = [s["timestamp"] for s in registros]
        print(f"Sensor {config['sensor_id']} ({config['type']}): "
              f"{min(fechas)} -> {max(fechas)} ({len(registros)} registros)")
    print(f"\nTotal: {len(sensores)} registros generados.")

if __name__ == "__main__":
    generar_datos()
