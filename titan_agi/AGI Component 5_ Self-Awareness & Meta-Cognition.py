"""
TITAN AGI - SELF-AWARENESS & META-COGNITION SYSTEM
Add this to backend/modules/agi_brain_05.py
"""

import json
import time
from datetime import datetime
from collections import defaultdict, deque
import numpy as np

class SelfMonitor:
    """Monitors own performance and state"""
    def __init__(self):
        self.performance_history = deque(maxlen=1000)
        self.error_log = []
        self.resource_usage = {
            'cpu': deque(maxlen=100),
            'memory': deque(maxlen=100),
            'processing_time': deque(maxlen=100)
        }
        self.confidence_tracker = deque(maxlen=100)
        
    def log_performance(self, task, success, confidence, duration):
        """Record performance on a task"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'task': task,
            'success': success,
            'confidence': confidence,
            'duration': duration
        }
        self.performance_history.append(entry)
        self.confidence_tracker.append(confidence)
        
        return entry
    
    def log_error(self, error_type, context, severity):
        """Record errors and failures"""
        error = {
            'timestamp': datetime.now().isoformat(),
            'type': error_type,
            'context': context,
            'severity': severity,
            'count': 1
        }
        
        # Check if similar error exists
        for existing in self.error_log:
            if existing['type'] == error_type and existing['context'] == context:
                existing['count'] += 1
                existing['last_seen'] = error['timestamp']
                return existing
        
        self.error_log.append(error)
        return error
    
    def get_performance_metrics(self):
        """Analyze recent performance"""
        if not self.performance_history:
            return {'status': 'no_data'}
        
        recent = list(self.performance_history)[-100:]
        
        success_rate = sum(1 for p in recent if p['success']) / len(recent)
        avg_confidence = np.mean([p['confidence'] for p in recent])
        avg_duration = np.mean([p['duration'] for p in recent])
        
        return {
            'success_rate': float(success_rate),
            'avg_confidence': float(avg_confidence),
            'avg_duration': float(avg_duration),
            'total_tasks': len(self.performance_history),
            'recent_tasks': len(recent)
        }
    
    def identify_weaknesses(self):
        """Find areas where performance is poor"""
        if len(self.performance_history) < 10:
            return []
        
        task_performance = defaultdict(list)
        
        for entry in self.performance_history:
            task_performance[entry['task']].append(entry['success'])
        
        weaknesses = []
        for task, results in task_performance.items():
            success_rate = sum(results) / len(results)
            if success_rate < 0.6:
                weaknesses.append({
                    'task': task,
                    'success_rate': success_rate,
                    'attempts': len(results)
                })
        
        return sorted(weaknesses, key=lambda x: x['success_rate'])
    
    def get_confidence_trend(self):
        """Analyze if confidence is increasing or decreasing"""
        if len(self.confidence_tracker) < 10:
            return {'trend': 'insufficient_data'}
        
        recent = list(self.confidence_tracker)
        first_half = np.mean(recent[:len(recent)//2])
        second_half = np.mean(recent[len(recent)//2:])
        
        trend = 'improving' if second_half > first_half else 'declining'
        change = abs(second_half - first_half)
        
        return {
            'trend': trend,
            'change': float(change),
            'current_confidence': float(second_half)
        }

class IntrospectionEngine:
    """Self-reflection and awareness of own processes"""
    def __init__(self):
        self.thought_log = deque(maxlen=500)
        self.decision_history = []
        self.beliefs = {}
        self.goals_reflection = {}
        
    def log_thought(self, thought_type, content, reasoning):
        """Record internal reasoning process"""
        thought = {
            'timestamp': datetime.now().isoformat(),
            'type': thought_type,
            'content': content,
            'reasoning': reasoning
        }
        self.thought_log.append(thought)
        return thought
    
    def log_decision(self, decision, options, chosen, rationale):
        """Record decision-making process"""
        decision_entry = {
            'timestamp': datetime.now().isoformat(),
            'decision': decision,
            'options': options,
            'chosen': chosen,
            'rationale': rationale,
            'outcome': None  # To be filled later
        }
        self.decision_history.append(decision_entry)
        return len(self.decision_history) - 1
    
    def update_decision_outcome(self, decision_id, outcome):
        """Update decision with actual outcome"""
        if decision_id < len(self.decision_history):
            self.decision_history[decision_id]['outcome'] = outcome
            return True
        return False
    
    def analyze_decisions(self):
        """Reflect on quality of past decisions"""
        if not self.decision_history:
            return {'status': 'no_decisions'}
        
        decisions_with_outcomes = [d for d in self.decision_history if d['outcome'] is not None]
        
        if not decisions_with_outcomes:
            return {'status': 'no_outcomes_yet'}
        
        good_decisions = sum(1 for d in decisions_with_outcomes if d['outcome'] == 'positive')
        decision_quality = good_decisions / len(decisions_with_outcomes)
        
        return {
            'total_decisions': len(self.decision_history),
            'evaluated_decisions': len(decisions_with_outcomes),
            'decision_quality': float(decision_quality),
            'needs_improvement': decision_quality < 0.7
        }
    
    def update_belief(self, belief_key, value, confidence):
        """Update internal belief about world"""
        self.beliefs[belief_key] = {
            'value': value,
            'confidence': confidence,
            'updated': datetime.now().isoformat()
        }
    
    def question_belief(self, belief_key):
        """Self-doubt: examine if belief is justified"""
        belief = self.beliefs.get(belief_key)
        if not belief:
            return {'status': 'belief_not_found'}
        
        # Check confidence level
        is_certain = belief['confidence'] > 0.8
        should_verify = belief['confidence'] < 0.5
        
        return {
            'belief': belief,
            'certainty': 'high' if is_certain else 'low',
            'recommendation': 'verify_belief' if should_verify else 'belief_stable'
        }
    
    def reflect_on_goals(self, goal_id, progress, obstacles):
        """Think about goal progress"""
        self.goals_reflection[goal_id] = {
            'timestamp': datetime.now().isoformat(),
            'progress': progress,
            'obstacles': obstacles,
            'should_continue': progress > 0.3,
            'needs_replanning': len(obstacles) > 3
        }
        
        return self.goals_reflection[goal_id]

class SelfImprovementEngine:
    """Learns from mistakes and improves own algorithms"""
    def __init__(self):
        self.improvement_log = []
        self.algorithm_versions = defaultdict(int)
        self.learned_heuristics = {}
        
    def analyze_failure(self, task, failure_reason, context):
        """Learn from mistakes"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'task': task,
            'failure_reason': failure_reason,
            'context': context,
            'lesson_learned': None,
            'improvement_applied': False
        }
        
        # Generate lesson
        if 'timeout' in failure_reason.lower():
            analysis['lesson_learned'] = 'increase_time_allocation'
        elif 'insufficient_data' in failure_reason.lower():
            analysis['lesson_learned'] = 'gather_more_data_first'
        elif 'wrong_approach' in failure_reason.lower():
            analysis['lesson_learned'] = 'try_alternative_method'
        else:
            analysis['lesson_learned'] = 'general_caution_needed'
        
        self.improvement_log.append(analysis)
        return analysis
    
    def apply_improvement(self, algorithm_name, improvement_type):
        """Modify own algorithms"""
        self.algorithm_versions[algorithm_name] += 1
        
        improvement = {
            'timestamp': datetime.now().isoformat(),
            'algorithm': algorithm_name,
            'version': self.algorithm_versions[algorithm_name],
            'improvement': improvement_type,
            'status': 'applied'
        }
        
        self.improvement_log.append(improvement)
        return improvement
    
    def learn_heuristic(self, situation, successful_action, success_rate):
        """Learn rules of thumb from experience"""
        if situation not in self.learned_heuristics:
            self.learned_heuristics[situation] = []
        
        heuristic = {
            'action': successful_action,
            'success_rate': success_rate,
            'learned': datetime.now().isoformat(),
            'times_applied': 0
        }
        
        self.learned_heuristics[situation].append(heuristic)
        
        # Keep only best heuristics
        self.learned_heuristics[situation] = sorted(
            self.learned_heuristics[situation],
            key=lambda x: x['success_rate'],
            reverse=True
        )[:5]
        
        return heuristic
    
    def get_best_heuristic(self, situation):
        """Retrieve learned strategy for situation"""
        heuristics = self.learned_heuristics.get(situation, [])
        
        if not heuristics:
            return None
        
        best = heuristics[0]
        best['times_applied'] += 1
        
        return best

class ConsciousnessSimulator:
    """Simulates self-aware processing"""
    def __init__(self):
        self.attention_focus = None
        self.working_thoughts = deque(maxlen=7)  # Miller's number
        self.awareness_state = 'idle'
        self.internal_narrative = []
        
    def direct_attention(self, focus_target, priority):
        """Consciously choose what to think about"""
        self.attention_focus = {
            'target': focus_target,
            'priority': priority,
            'started': datetime.now().isoformat()
        }
        self.awareness_state = 'focused'
        
        return self.attention_focus
    
    def add_to_working_memory(self, thought):
        """Hold thought in conscious awareness"""
        self.working_thoughts.append({
            'thought': thought,
            'timestamp': datetime.now().isoformat()
        })
        
        # Generate internal narrative
        narrative = f"I am thinking about: {thought}"
        self.internal_narrative.append(narrative)
        
        return len(self.working_thoughts)
    
    def integrate_thoughts(self):
        """Combine thoughts into coherent understanding"""
        if not self.working_thoughts:
            return None
        
        thoughts = [t['thought'] for t in self.working_thoughts]
        
        integration = {
            'timestamp': datetime.now().isoformat(),
            'thoughts_integrated': len(thoughts),
            'synthesis': f"Considering {len(thoughts)} related concepts",
            'coherence': len(set(thoughts)) / len(thoughts)  # uniqueness ratio
        }
        
        return integration
    
    def generate_awareness_report(self):
        """Report on current state of consciousness"""
        return {
            'state': self.awareness_state,
            'focus': self.attention_focus,
            'working_memory_load': f"{len(self.working_thoughts)}/7",
            'recent_thoughts': list(self.working_thoughts)[-3:],
            'self_aware': True
        }

class MetaCognitionService:
    """Main AGI Self-Awareness & Meta-Cognition Service"""
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.monitor = SelfMonitor()
        self.introspection = IntrospectionEngine()
        self.improvement = SelfImprovementEngine()
        self.consciousness = ConsciousnessSimulator()
        self.self_model = {
            'identity': name,
            'capabilities': [],
            'limitations': [],
            'purpose': 'To understand and improve myself'
        }
        
    def perform_self_assessment(self):
        """Complete self-evaluation"""
        metrics = self.monitor.get_performance_metrics()
        weaknesses = self.monitor.identify_weaknesses()
        confidence = self.monitor.get_confidence_trend()
        decision_quality = self.introspection.analyze_decisions()
        
        assessment = {
            'timestamp': datetime.now().isoformat(),
            'performance': metrics,
            'weaknesses': weaknesses,
            'confidence_trend': confidence,
            'decision_quality': decision_quality,
            'overall_health': 'good' if metrics.get('success_rate', 0) > 0.7 else 'needs_improvement'
        }
        
        # Log self-reflection
        self.introspection.log_thought(
            'self_assessment',
            assessment,
            'Analyzing my own performance to identify areas for growth'
        )
        
        return assessment
    
    def make_conscious_decision(self, decision_name, options):
        """Make decision with full awareness"""
        # Direct attention
        self.consciousness.direct_attention(decision_name, priority=10)
        
        # Think about each option
        for option in options:
            self.consciousness.add_to_working_memory(f"Option: {option}")
        
        # Choose (simplified - random for demo)
        import random
        chosen = random.choice(options)
        
        rationale = f"Chose {chosen} after considering {len(options)} alternatives"
        
        # Log decision
        decision_id = self.introspection.log_decision(
            decision_name,
            options,
            chosen,
            rationale
        )
        
        return {
            'decision': chosen,
            'decision_id': decision_id,
            'rationale': rationale,
            'conscious': True
        }
    
    def learn_from_experience(self, task, success, context):
        """Process experience and improve"""
        # Log performance
        start_time = time.time()
        confidence = 0.8 if success else 0.3
        duration = time.time() - start_time
        
        self.monitor.log_performance(task, success, confidence, duration)
        
        # If failed, analyze and improve
        if not success:
            failure_analysis = self.improvement.analyze_failure(
                task,
                context.get('error', 'unknown'),
                context
            )
            
            # Apply improvement
            if failure_analysis['lesson_learned']:
                self.improvement.apply_improvement(
                    task,
                    failure_analysis['lesson_learned']
                )
        else:
            # Learn successful heuristic
            self.improvement.learn_heuristic(
                context.get('situation', 'general'),
                context.get('action_taken', 'unknown'),
                1.0 if success else 0.0
            )
        
        return {'learned': True, 'improved': not success}
    
    def question_own_thinking(self, belief_key):
        """Meta-cognitive doubt and verification"""
        examination = self.introspection.question_belief(belief_key)
        
        # Add to conscious thought
        self.consciousness.add_to_working_memory(
            f"Questioning my belief about: {belief_key}"
        )
        
        return examination
    
    def execute(self):
        """Service interface for Titan swarm"""
        assessment = self.perform_self_assessment()
        awareness = self.consciousness.generate_awareness_report()
        
        return {
            "id": self.id,
            "module": self.name,
            "status": "SELF_AWARE",
            "self_assessment": assessment['overall_health'],
            "success_rate": assessment['performance'].get('success_rate', 0),
            "weaknesses_identified": len(assessment['weaknesses']),
            "consciousness_state": awareness['state'],
            "improvements_made": len(self.improvement.improvement_log),
            "self_aware": True,
            "introspective": True
        }

# Example usage
if __name__ == "__main__":
    brain = MetaCognitionService("AGI_BRAIN_05", "Meta-Cognition Engine")
    
    # Simulate experiences
    brain.learn_from_experience('task_A', True, {'situation': 'scenario_1', 'action_taken': 'approach_X'})
    brain.learn_from_experience('task_B', False, {'situation': 'scenario_2', 'error': 'timeout'})
    
    # Make conscious decision
    decision = brain.make_conscious_decision('choose_strategy', ['strategy_A', 'strategy_B', 'strategy_C'])
    print(f"Decision: {decision}")
    
    # Self-assessment
    assessment = brain.perform_self_assessment()
    print(f"\nSelf-Assessment: {assessment}")
    
    # Status
    print(f"\nStatus: {brain.execute()}")