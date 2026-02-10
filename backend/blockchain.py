import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self, index, data, prev_hash):
        self.index = index
        self.timestamp = datetime.utcnow().isoformat()
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        raw = f"{self.index}{self.timestamp}{json.dumps(self.data)}{self.prev_hash}"
        return hashlib.sha256(raw.encode()).hexdigest()

class AuditChain:
    def __init__(self):
        self.chain = [self.genesis()]

    def genesis(self):
        return Block(0, {"event": "GENESIS"}, "0")

    def add_event(self, data):
        prev = self.chain[-1]
        block = Block(len(self.chain), data, prev.hash)
        self.chain.append(block)

audit_chain = AuditChain()
