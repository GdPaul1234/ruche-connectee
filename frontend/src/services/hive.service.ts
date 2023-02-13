import { faker } from '@faker-js/faker'

import { BehivesService } from '../generated/services/BehivesService'
import { SensorsService } from '../generated/services/SensorsService'
import { EventsService } from '../generated/services/EventsService'
import { BehiveOut } from '../generated/models/BehiveOut'
import { SensorOut } from '../generated/models/SensorOut'
import { EventsOut } from '../generated/models/EventsOut'

enum SensorType {
  temperature,
  humidity,
  weight,
  alert,
  battery
}

export const sensorTypeValues = Object.values(SensorType).filter(v => typeof v === 'string')

export async function getHive(id: string): Promise<BehiveOut> {
  return await BehivesService.showBehiveApiBehivesIdGet({ id })
}

export type TemperatureHumidityResponse = Record<'indoor' | 'outdoor', { updated_at: string, value: number, unit: string }[]>

export async function getHiveTemperature(behiveId: string, fromDate: Date, toDate: Date): Promise<TemperatureHumidityResponse> {
  const response = await SensorsService.listSensorRecordsByTypeApiSensorsBehiveBehiveIdSensorTypeGet({
    behiveId,
    sensorType: 'temperature',
    fromDate: fromDate.toISOString(),
    toDate: toDate.toISOString()
  })

  return {
    indoor: response.values,
    outdoor: response.values.map(v => ({ ...v, value: faker.datatype.number({ min: 0, max: 36 }) }))
  }
}

export async function getHiveHumidity(behiveId: string, fromDate: Date, toDate: Date): Promise<TemperatureHumidityResponse> {
  const response = await SensorsService.listSensorRecordsByTypeApiSensorsBehiveBehiveIdSensorTypeGet({
    behiveId,
    sensorType: 'humidity',
    fromDate: fromDate.toISOString(),
    toDate: toDate.toISOString()
  })

  return {
    indoor: response.values,
    outdoor: response.values.map(v => ({ ...v, value: faker.datatype.number({ min: 60, max: 100 }) }))
  }
}

export type WeightResponse = Record<'weight', SensorOut['values']>
export async function getHiveWeight(behiveId: string, fromDate: Date, toDate: Date): Promise<WeightResponse> {
  const response = await SensorsService.listSensorRecordsByTypeApiSensorsBehiveBehiveIdSensorTypeGet({
    behiveId,
    sensorType: 'weight',
    fromDate: fromDate.toISOString(),
    toDate: toDate.toISOString()
  })

  return { weight: response.values }
}

export type BatteryResponse = Record<'battery', SensorOut['values']>
export async function getBatteryResponse(behiveId: string, fromDate: Date, toDate: Date): Promise<BatteryResponse> {
  const response = await SensorsService.listSensorRecordsByTypeApiSensorsBehiveBehiveIdSensorTypeGet({
    behiveId,
    sensorType: 'battery',
    fromDate: fromDate.toISOString(),
    toDate: toDate.toISOString()
  })

  return { battery: response.values }
}

export type AlertResponse = Record<'alert', EventsOut['values']>
export async function getAlertResponse(behiveId: string, fromDate: Date, toDate: Date): Promise<AlertResponse> {
  const response = await EventsService.listEventsApiEventsBehiveBehiveIdGet({
    behiveId,
    fromDate: fromDate.toISOString(),
    toDate: toDate.toISOString()
  })

  return { alert: response.values }
}
