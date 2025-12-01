import psutil
import time
import pandas as pd
import matplotlib.pyplot as plt

def estimate_power(cpu, ram):
    return (cpu * 0.5) + (ram * 0.75)

def monitor(duration=30):
    logs = []
    start = time.time()

    while time.time() - start < duration:
        for p in psutil.process_iter(['pid','name','cpu_percent','memory_info']):
            try:
                cpu = p.info['cpu_percent']
                ram = p.info['memory_info'].rss / (1024**3)
                power = estimate_power(cpu, ram)

                logs.append({
                    "time": time.time(),
                    "app": p.info['name'],
                    "cpu": cpu,
                    "ram_gb": ram,
                    "power_watts": power
                })
            except:
                continue

        time.sleep(1)

    return pd.DataFrame(logs)

df = monitor(20)
df.to_csv("energy_report.csv", index=False)
print("Report created!")
