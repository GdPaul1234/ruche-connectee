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

export type TemperatureHumidityResponse = Record<'indoor' | 'outdoor', { updatedAt: string, value: number }[]>

export function getHiveTemperature(hiveId: string, start: number, stop: number): Promise<TemperatureHumidityResponse> {
  const days = Array.from({ length: 30 }, (_, i) => (new Date(Date.now() - (30 - i) * 24 * 60 * 60 * 1000)).toISOString())

  return Promise.resolve({
    indoor: days.map(day => ({ updatedAt: day, value: faker.datatype.number({ min: 0, max: 36 }) })),
    outdoor: days.map(day => ({ updatedAt: day, value: faker.datatype.number({ min: 0, max: 36 }) }))
  })
}

export function getHiveHumidity(hiveId: string, start: number, stop: number): Promise<TemperatureHumidityResponse> {
  const days = Array.from({ length: 30 }, (_, i) => (new Date(Date.now() - (30 - i) * 24 * 60 * 60 * 1000)).toISOString())

  return Promise.resolve({
    indoor: days.map(day => ({ updatedAt: day, value: faker.datatype.number({ min: 0, max: 36 }) })),
    outdoor: days.map(day => ({ updatedAt: day, value: faker.datatype.number({ min: 0, max: 36 }) }))
  })
}

export type WeightResponse = Record<'weight', { updatedAt: string, value: number }[]>

export function getHiveWeight(hiveId: string, start: number, stop: number): Promise<WeightResponse> {
  const days = Array.from({ length: 30 }, (_, i) => (new Date(Date.now() - (30 - i) * 24 * 60 * 60 * 1000)).toISOString())

  return Promise.resolve({
    weight: days.map(day => ({ updatedAt: day, value: faker.datatype.number({ min: 0, max: 36 }) })),
  })
}

export type BatteryResponse = Record<'battery', { updatedAt: string, value: number }[]>

export function getBatteryResponse(hiveId: string, start: number, stop: number): Promise<BatteryResponse> {
  const days = Array.from({ length: 30 }, (_, i) => (new Date(Date.now() - (30 - i) * 24 * 60 * 60 * 1000)).toISOString())

  return Promise.resolve({
    battery: days.map(day => ({ updatedAt: day, value: faker.datatype.number({ min: 0, max: 36 }) })),
  })
}

export type AlertResponse = Record<'alert', {
  updatedAt: string
  value: number
  messages: {
    type: string
    updatedAt: string
    message: string
  }[]
}[]>

export function getAlertResponse(hiveId: string, start: number, stop: number): Promise<AlertResponse> {
  const days = Array.from({ length: 30 }, (_, i) => (new Date(Date.now() - (30 - i) * 24 * 60 * 60 * 1000)).toISOString())

  return Promise.resolve({
    alert: days.map(day => {
      const nbMessage = faker.datatype.number({ min: 0, max: 5 })
      return {
        updatedAt: day,
        value: nbMessage,
        messages: Array.from(
          { length: nbMessage },
          (_, i) => ({
            type: 'info',
            updatedAt: new Date(new Date(day).getTime() + i * 2 * 3600 * 1000).toISOString(),
            message: faker.hacker.phrase()
          })
        )
      }
    }),
  })
}
