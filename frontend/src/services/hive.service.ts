import { faker } from '@faker-js/faker'

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

export type TemperatureResponse = Record<'indoor' | 'outdoor', { updatedAt: string, value: number }[]>

export function getHiveTemperature(hiveId: number, start: number, stop: number): Promise<TemperatureResponse> {
  const days = Array.from({ length: 30 }, (_, i) => (new Date(Date.now() - (30 - i) * 24 * 60 * 60 * 1000)).toISOString())

  return Promise.resolve({
    indoor: days.map(day => ({ updatedAt: day, value: faker.datatype.number({ min: 0, max: 36 }) })),
    outdoor: days.map(day => ({ updatedAt: day, value: faker.datatype.number({ min: 0, max: 36 }) }))
  })
}
