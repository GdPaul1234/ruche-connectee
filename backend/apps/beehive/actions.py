from bson import ObjectId

from apps.sensor.models import SensorType
from apps.beehive.models import BehiveMetric

async def update_behive_sensor_last_value(behives_db, behive_id: str, sensor_type: SensorType, last_value: BehiveMetric, session):
    await behives_db.update_one(
        {"_id": ObjectId(behive_id)},
        {"$set": { f"last_metrics.{sensor_type}": last_value }},
        session=session
    )
