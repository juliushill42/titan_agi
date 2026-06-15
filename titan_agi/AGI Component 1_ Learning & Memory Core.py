"""
TITAN AGI - LEARNING & MEMORY SYSTEM
Add this to backend/modules/agi_brain_01.py
"""

import json
import os
from datetime import datetime
import numpy as np

class ShortTermMemory:
    """Working memory - last 100 interactions"""
    def __init__(self, capacity=100):
        self.buffer = []
        self.capacity = capacity
    
    def add(self, experience):
        self.buffer.append({
            'timestamp': datetime.now().isoformat(),
            'data': experience
        })
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)
    
    def recall(self, query_type):
        return [e for e in self.buffer if query_type in str(e['data'])]

class LongTermMemory:
    """Persistent knowledge storage"""
    def __init__(self, filepath="memory/longterm.json"):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.knowledge = self._load()
    
    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                return json.load(f)
        return {"facts": [], "patterns": [], "skills": []}
    
    def store(self, category, item):
        if category in self.knowledge:
            self.knowledge[category].append({
                'content': item,
                'stored_at': datetime.now().isoformat(),
                'access_count': 0
            })
            self._save()
    
    def retrieve(self, category, limit=10):
        items = self.knowledge.get(category, [])
        # Sort by access frequency
        return sorted(items, key=lambda x: x['access_count'], reverse=True)[:limit]
    
    def _save(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.knowledge, f, indent=2)

class SimpleNeuralLearner:
    """Basic pattern learning - simplified neural net"""
    def __init__(self, input_size=10, hidden_size=20, output_size=5):
        # Initialize random weights
        self.w1 = np.random.randn(input_size, hidden_size) * 0.01
        self.w2 = np.random.randn(hidden_size, output_size) * 0.01
        self.learning_rate = 0.01
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def forward(self, X):
        """Simple feedforward"""
        self.h = self.sigmoid(np.dot(X, self.w1))
        self.output = self.sigmoid(np.dot(self.h, self.w2))
        return self.output
    
    def train(self, X, y, epochs=100):
        """Basic backpropagation"""
        for _ in range(epochs):
            # Forward pass
            output = self.forward(X)
            
            # Calculate error
            error = y - output
            
            # Backward pass (simplified)
            d_output = error * output * (1 - output)
            d_hidden = np.dot(d_output, self.w2.T) * self.h * (1 - self.h)
            
            # Update weights
            self.w2 += self.learning_rate * np.dot(self.h.T, d_output)
            self.w1 += self.learning_rate * np.dot(X.T, d_hidden)
        
        return np.mean(np.abs(error))

class ReinforcementLearner:
    """Q-Learning for decision making"""
    def __init__(self, states=100, actions=10):
        self.q_table = np.zeros((states, actions))
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 0.1  # exploration rate
    
    def choose_action(self, state):
        """Epsilon-greedy action selection"""
        if np.random.random() < self.epsilon:
            return np.random.randint(0, self.q_table.shape[1])
        return np.argmax(self.q_table[state])
    
    def learn(self, state, action, reward, next_state):
        """Update Q-value based on experience"""
        predict = self.q_table[state, action]
        target = reward + self.discount_factor * np.max(self.q_table[next_state])
        self.q_table[state, action] += self.learning_rate * (target - predict)

class AdaptiveService:
    """Main AGI Learning Service"""
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.stm = ShortTermMemory()
        self.ltm = LongTermMemory()
        self.neural = SimpleNeuralLearner()
        self.rl = ReinforcementLearner()
        self.experience_count = 0
    
    def process_experience(self, input_data, outcome):
        """Learn from new experience"""
        self.experience_count += 1
        
        # Store in short-term memory
        self.stm.add({'input': input_data, 'outcome': outcome})
        
        # If pattern is successful, store in long-term
        if outcome.get('success', False):
            self.ltm.store('patterns', input_data)
        
        # Simple RL update
        state = hash(str(input_data)) % 100
        action = outcome.get('action_taken', 0)
        reward = 1 if outcome.get('success') else -1
        next_state = (state + 1) % 100
        
        self.rl.learn(state, action, reward, next_state)
        
        return {
            'learned': True,
            'experiences': self.experience_count,
            'stm_size': len(self.stm.buffer),
            'ltm_patterns': len(self.ltm.knowledge['patterns'])
        }
    
    def predict(self, situation):
        """Use learned knowledge to make prediction"""
        # Check long-term memory for similar patterns
        similar = self.ltm.retrieve('patterns', limit=5)
        
        # Use RL to choose action
        state = hash(str(situation)) % 100
        action = self.rl.choose_action(state)
        
        return {
            'recommended_action': action,
            'confidence': float(np.max(self.rl.q_table[state])),
            'similar_cases': len(similar),
            'based_on_experiences': self.experience_count
        }
    
    def execute(self):
        """Service interface for Titan swarm"""
        return {
            "id": self.id,
            "module": self.name,
            "status": "LEARNING",
            "experiences": self.experience_count,
            "stm_capacity": f"{len(self.stm.buffer)}/100",
            "ltm_facts": len(self.ltm.knowledge.get('facts', [])),
            "ltm_patterns": len(self.ltm.knowledge.get('patterns', [])),
            "learning_active": True
        }

# Example usage
if __name__ == "__main__":
    brain = AdaptiveService("AGI_BRAIN_01", "Learning Core")
    
    # Simulate learning
    for i in range(10):
        result = brain.process_experience(
            {'scenario': f'test_{i}', 'value': i * 10},
            {'success': i % 2 == 0, 'action_taken': i % 5}
        )
        print(f"Learning iteration {i}: {result}")
    
    # Make prediction
    prediction = brain.predict({'scenario': 'new_situation', 'value': 55})
    print(f"\nPrediction: {prediction}")