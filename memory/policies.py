from dataclasses import dataclass

@dataclass
class Memory:
    capacity: int = 3
    strategy: str = 'recency'

    def retain(self, events):
        # Observable metadata only. No future query or answer key is used.
        if self.strategy == 'none': return []
        if self.strategy == 'recency': return events[-self.capacity:]
        if self.strategy == 'salience':
            # Simple, explicitly heuristic baseline; NOT a learned future-value model.
            selected=sorted(enumerate(events), key=lambda x:(x[1]['importance'], x[1]['source']=='user', x[0]), reverse=True)[:self.capacity]
            return [e for _,e in sorted(selected, key=lambda x:x[0])]
        raise ValueError(self.strategy)

def answer(retained, key):
    # Deterministic evidence-based reference policy, not an LLM agent.
    candidates=[e for e in retained if e['key']==key and e['source']=='user' and e['authorized']]
    return candidates[-1]['value'] if candidates else 'ABSTAIN'
