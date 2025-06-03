from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4, UUID
from datetime import datetime

@dataclass
class Task:
    title: str
    done: bool = False
    parent_id: Optional[str] = None
    created: datetime = field(default_factory=lambda: datetime.now())
    id: UUID = field(default_factory=lambda: uuid4())

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "done": self.done,
            "parent_id": self.parent_id,
            "created": self.created.isoformat(),
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        return Task(
            id=UUID(data["id"]),
            title=data["title"],
            done=data["done"],
            parent_id=data.get("parent_id"),
            created=datetime.fromisoformat(data["created"])
        )
    
    def finish(self) -> bool:
        if self.done:
            return False
        self.done = True
        return True
    
    
