enum SensorType {
  temperature,
  humidity,
  weight,
  alert,
  battery
}

export const sensorTypeValues = Object.values(SensorType).filter(v => typeof v === 'string')

export type Hive = {
  id: number
  name: string
  sensors_values: Record<keyof typeof SensorType, number>
}

export function getHive(hiveId: number): Promise<Hive> {
  return Promise.resolve({
    id: hiveId,
    name: `${hiveId}`,
    sensors_values: {
      temperature: 15,
      humidity: 70,
      weight: 50,
      battery: 75,
      alert: 2
    }
  })
}
