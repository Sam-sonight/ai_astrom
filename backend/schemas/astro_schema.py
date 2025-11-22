from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ChartRequest(BaseModel):
    dt_local: datetime
    lat: float
    lon: float
    tz_name: str | None = None
    include_angles_in_aspects: bool = True

    model_config = ConfigDict(extra="ignore")
