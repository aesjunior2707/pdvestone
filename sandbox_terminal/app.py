import asyncio
from bleak import BleakScanner

async def escanear_ble():
    print("Procurando dispositivos BLE...")
    dispositivos = await BleakScanner.discover()
    for d in dispositivos:
        print(f"{d.name} - {d.address}")

asyncio.run(escanear_ble())