from dataclasses import dataclass

@dataclass
class Message:
    id: int
    sender: str
    content: str
    created_at: str
