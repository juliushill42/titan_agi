"""
TITAN AGI - REASONING & NLP SYSTEM
Add this to backend/modules/agi_brain_02.py
"""

import re
import math
from collections import defaultdict, Counter
from datetime import datetime

class NLPProcessor:
    """Natural Language Understanding"""
    def __init__(self):
        self.vocabulary = set()
        self.word_freq = Counter()
        self.intent_patterns = {
            'query': ['what', 'who', 'when', 'where', 'why', 'how'],
            'command': ['run', 'execute', 'start', 'stop', 'create', 'delete'],
            'analyze': ['analyze', 'evaluate', 'assess', 'compare'],
            'learn': ['learn', 'train', 'remember', 'study']
        }
    
    def tokenize(self, text):
        """Break text into tokens"""
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        self.vocabulary.update(tokens)
        self.word_freq.update(tokens)
        return tokens
    
    def extract_intent(self, text):
        """Determine what user wants"""
        tokens = self.tokenize(text)
        scores = defaultdict(int)
        
        for intent, keywords in self.intent_patterns.items():
            for token in tokens:
                if token in keywords:
                    scores[intent] += 1
        
        if scores:
            intent = max(scores, key=scores.get)
            confidence = scores[intent] / len(tokens)
            return {'intent': intent, 'confidence': confidence}
        
        return {'intent': 'unknown', 'confidence': 0.0}
    
    def extract_entities(self, text):
        """Find key entities (simplified NER)"""
        tokens = self.tokenize(text)
        entities = {
            'numbers': [t for t in tokens if t.isdigit()],
            'capitalized': [w for w in text.split() if w and w[0].isupper()],
            'keywords': [t for t in tokens if self.word_freq[t] < 3]  # rare = important
        }
        return entities
    
    def semantic_similarity(self, text1, text2):
        """Calculate how similar two texts are"""
        tokens1 = set(self.tokenize(text1))
        tokens2 = set(self.tokenize(text2))
        
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)

class LogicEngine:
    """Symbolic reasoning and inference"""
    def __init__(self):
        self.facts = set()
        self.rules = []
    
    def add_fact(self, fact):
        """Store a known truth"""
        self.facts.add(fact)
    
    def add_rule(self, condition, conclusion):
        """Add inference rule: IF condition THEN conclusion"""
        self.rules.append({'if': condition, 'then': conclusion})
    
    def infer(self):
        """Apply rules to derive new facts"""
        new_facts = set()
        
        for rule in self.rules:
            # Check if condition is satisfied
            if all(fact in self.facts for fact in rule['if']):
                new_facts.add(rule['then'])
        
        self.facts.update(new_facts)
        return new_facts
    
    def query(self, fact):
        """Check if something is true"""
        return fact in self.facts
    
    def explain(self, fact):
        """Show reasoning chain"""
        if fact in self.facts:
            # Find which rule led to this
            for rule in self.rules:
                if rule['then'] == fact:
                    return f"Because: {' AND '.join(rule['if'])} → {fact}"
        return f"{fact} is a base fact"

class ProblemSolver:
    """Algorithm for multi-step problem solving"""
    def __init__(self):
        self.steps = []
    
    def decompose(self, problem):
        """Break complex problem into sub-problems"""
        # Simple heuristic decomposition
        if 'and' in problem.lower():
            return problem.lower().split('and')
        if 'then' in problem.lower():
            return problem.lower().split('then')
        return [problem]
    
    def solve_step(self, step):
        """Solve individual step"""
        step = step.strip()
        
        # Mathematical expressions
        if any(op in step for op in ['+', '-', '*', '/', '^']):
            try:
                # Safe eval for math
                result = eval(step.replace('^', '**'))
                return {'step': step, 'result': result, 'solved': True}
            except:
                pass
        
        # Logical operations
        if 'if' in step and 'then' in step:
            parts = step.split('then')
            return {'step': step, 'result': 'conditional evaluated', 'solved': True}
        
        return {'step': step, 'result': 'requires external knowledge', 'solved': False}
    
    def solve(self, problem):
        """Full problem solving pipeline"""
        sub_problems = self.decompose(problem)
        solutions = []
        
        for sub in sub_problems:
            sol = self.solve_step(sub)
            solutions.append(sol)
            self.steps.append(sol)
        
        success_rate = sum(1 for s in solutions if s['solved']) / len(solutions)
        
        return {
            'problem': problem,
            'sub_problems': len(sub_problems),
            'solutions': solutions,
            'success_rate': success_rate
        }

class CausalReasoning:
    """Understanding cause and effect"""
    def __init__(self):
        self.causal_graph = defaultdict(list)  # cause -> [effects]
    
    def add_causal_link(self, cause, effect, strength=1.0):
        """Record that X causes Y"""
        self.causal_graph[cause].append({'effect': effect, 'strength': strength})
    
    def predict_effect(self, cause):
        """What happens if X occurs?"""
        return self.causal_graph.get(cause, [])
    
    def find_cause(self, effect):
        """What could have caused Y?"""
        causes = []
        for cause, effects in self.causal_graph.items():
            if any(e['effect'] == effect for e in effects):
                causes.append(cause)
        return causes
    
    def explain_chain(self, start, end, depth=3):
        """Find causal chain from start to end"""
        if depth == 0:
            return None
        
        effects = self.predict_effect(start)
        for e in effects:
            if e['effect'] == end:
                return [start, end]
            
            chain = self.explain_chain(e['effect'], end, depth - 1)
            if chain:
                return [start] + chain
        
        return None

class ReasoningService:
    """Main AGI Reasoning Service"""
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.nlp = NLPProcessor()
        self.logic = LogicEngine()
        self.solver = ProblemSolver()
        self.causal = CausalReasoning()
        self.interactions = 0
        
        # Pre-load some basic knowledge
        self._bootstrap_knowledge()
    
    def _bootstrap_knowledge(self):
        """Load basic common sense"""
        # Logic rules
        self.logic.add_fact('sky is blue')
        self.logic.add_fact('water is wet')
        self.logic.add_rule(['rain'], 'ground is wet')
        self.logic.add_rule(['ground is wet', 'cold'], 'ice forms')
        
        # Causal knowledge
        self.causal.add_causal_link('rain', 'wet ground', 0.95)
        self.causal.add_causal_link('heat', 'evaporation', 0.9)
        self.causal.add_causal_link('exercise', 'fitness', 0.8)
    
    def process_query(self, text):
        """Understand and respond to natural language"""
        self.interactions += 1
        
        # NLP Analysis
        intent = self.nlp.extract_intent(text)
        entities = self.nlp.extract_entities(text)
        
        # Reasoning
        response = {
            'understood': True,
            'intent': intent,
            'entities': entities,
            'reasoning': None
        }
        
        # If it's a problem
        if 'solve' in text.lower() or '=' in text:
            solution = self.solver.solve(text)
            response['reasoning'] = solution
        
        # If it's a logical query
        if '?' in text:
            # Extract fact being queried
            fact = text.replace('?', '').strip().lower()
            if self.logic.query(fact):
                response['reasoning'] = {
                    'answer': True,
                    'explanation': self.logic.explain(fact)
                }
        
        return response
    
    def reason_about(self, situation):
        """Deep reasoning about a situation"""
        # Infer new facts
        new_facts = self.logic.infer()
        
        # Find causal explanations
        tokens = self.nlp.tokenize(situation)
        causal_analysis = {}
        
        for token in tokens:
            effects = self.causal.predict_effect(token)
            if effects:
                causal_analysis[token] = effects
        
        return {
            'situation': situation,
            'inferred_facts': list(new_facts),
            'causal_analysis': causal_analysis,
            'reasoning_depth': len(self.logic.facts)
        }
    
    def execute(self):
        """Service interface for Titan swarm"""
        return {
            "id": self.id,
            "module": self.name,
            "status": "REASONING",
            "interactions": self.interactions,
            "vocabulary_size": len(self.nlp.vocabulary),
            "known_facts": len(self.logic.facts),
            "inference_rules": len(self.logic.rules),
            "causal_links": len(self.causal.causal_graph),
            "active": True
        }

# Example usage
if __name__ == "__main__":
    brain = ReasoningService("AGI_BRAIN_02", "Reasoning Engine")
    
    # Test NLP
    query1 = brain.process_query("What happens when it rains?")
    print(f"Query 1: {query1}")
    
    # Test problem solving
    query2 = brain.process_query("Solve 25 + 17 * 2")
    print(f"\nQuery 2: {query2}")
    
    # Test reasoning
    situation = brain.reason_about("rain and cold weather")
    print(f"\nReasoning: {situation}")