from typing import Literal
from pydantic import BaseModel, Field


class TaskSummary(BaseModel):
    title: str = Field(..., min_length=5, description="Short title for the task")
    priority: Literal["high", "medium", "low"]
    summary: str = Field(..., min_length=20, description="Brief summary of the task")