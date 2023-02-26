import { BehivesService, SensorsService, EventsService, SensorOut, EventsOut } from '../generated'

enum SensorType {
  temperature_indoor,
  temperature_outdoor,
  humidity_indoor,
  humidity_outdoor,
  weight,
  battery
}

export const sensorTypeValues = Object.values(SensorType).concat('temperature', 'humidity').filter(v => typeof v === 'string')

function safeGetSensorValue(behiveId: string, fromDate: Date, toDate: Date, sensorType: 'temperature_indoor' | 'temperature_outdoor' | 'humidity_indoor' | 'humidity_outdoor') {
  return SensorsService.listSensorRecordsByTypeApiSensorsBehiveBehiveIdSensorTypeGet({
    behiveId, sensorType, fromDate: fromDate.toISOString(), toDate: toDate.toISOString()
  })
    .then(response => response.values)
    .catch(() => [])
}

export async function getHives() {
  return await BehivesService.listBehivesApiBehivesGet()
}

export async function getHive(id: string) {
  return await BehivesService.showBehiveApiBehivesIdGet({ id })
}

export type TemperatureHumidityResponse = Record<'indoor' | 'outdoor', { updated_at: string, value: number, unit: string }[]>

export async function getHiveTemperature(behiveId: string, fromDate: Date, toDate: Date): Promise<TemperatureHumidityResponse> {
  return {
    indoor: await safeGetSensorValue(behiveId, fromDate, toDate, 'temperature_indoor'),
    outdoor: await safeGetSensorValue(behiveId, fromDate, toDate, 'temperature_outdoor'),
  }
}

export async function getHiveHumidity(behiveId: string, fromDate: Date, toDate: Date): Promise<TemperatureHumidityResponse> {
  return {
    indoor: await safeGetSensorValue(behiveId, fromDate, toDate, 'humidity_indoor'),
    outdoor: await safeGetSensorValue(behiveId, fromDate, toDate, 'humidity_outdoor')
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
