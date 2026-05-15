from typing import Optional

from pydantic import BaseModel


class S3AdditionalData(BaseModel):
    s3_bucket: Optional[str]
    s3_key: Optional[str]
    s3_endpoint: Optional[str]
    s3_uri: Optional[str]
