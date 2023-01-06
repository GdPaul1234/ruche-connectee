export type Hive = {
  id: number
  name: string
  sensors_values: Record<'temperature' | 'humidity' | 'weight' | 'alert' | 'battery', number>
}

export function getHive(hiveId: number): Promise<Hive> {
  return Promise.resolve({
    id: hiveId,
    name: `$Ruche {hiveId}`,
    sensors_values: {
      temperature: 15,
      humidity: 70,
      weight: 50,
      battery: 75,
      alert: 2
    }
  })
}
