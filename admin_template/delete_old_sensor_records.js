// To launch in MongoSH

db.sensors.updateMany(
  {},
  { $pull: { values: { updated_at: { $lt: new Date("2023-02-30") } } } }
)
