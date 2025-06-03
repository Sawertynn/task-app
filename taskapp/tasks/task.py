from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4, UUID
from datetime import datetime


@dataclass
class Task:
    title: str
    done: bool = False
    id: UUID = field(default_factory=lambda: uuid4())
    parent_id: Optional[UUID] = None
    created: datetime = field(default_factory=lambda: datetime.now())
    finished: Optional[datetime] = None
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "done": self.done,
            "parent_id": str(self.parent_id) if self.parent_id else None,
            "created": self.created.isoformat(),
            "finished": self.finished.isoformat() if self.finished else None,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        return Task(
            id=UUID(data["id"]),
            title=data["title"],
            done=data["done"],
            parent_id=UUID(data["parent_id"]) if data.get("parent_id") else None,
            created=datetime.fromisoformat(data["created"]),
            finished=datetime.fromisoformat(data["finished"]) if data.get("finished") else None,
        )

    
    def finish(self, completion_time = None) -> bool:
        if self.done:
            return False
        self.done = True
        self.finished = completion_time or datetime.now()
        return True
    
    