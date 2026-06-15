"""
TITAN AGI - TRANSFER LEARNING & GENERALIZATION SYSTEM
Add this to backend/modules/agi_brain_06.py
"""

import json
import numpy as np
from datetime import datetime
from collections import defaultdict, Counter

class DomainKnowledge:
    """Represents knowledge in a specific domain"""
    def __init__(self, domain_name):
        self.name = domain_name
        self.concepts = {}
        self.patterns = []
        self.skills = []
        self.relationships = defaultdict(list)
        
    def add_concept(self, concept_id, properties):
        """Store domain-specific concept"""
        self.concepts[concept_id] = {
            'properties': properties,
            'learned': datetime.now().isoformat(),
            'domain': self.name
        }
    
    def add_pattern(self, pattern, success_rate):
        """Record successful pattern in this domain"""
        self.patterns.append({
            'pattern': pattern,
            'success_rate': success_rate,
            'applications': 0
        })
    
    def add_skill(self, skill_name, proficiency):
        """Track skills acquired in this domain"""
        self.skills.append({
            'skill': skill_name,
            'proficiency': proficiency,
            'domain': self.name
        })
    
    def extract_abstract_structure(self):
        """Extract generalizable structure from domain"""
        # Find common patterns across concepts
        if not self.concepts:
            return None
        
        all_properties = []
        for concept in self.concepts.values():
            all_properties.extend(concept['properties'].keys())
        
        common_properties = [p for p, count in Counter(all_properties).items() if count > 1]
        
        return {
            'domain': self.name,
            'abstract_properties': common_properties,
            'pattern_count': len(self.patterns),
            'generalizable': len(common_properties) > 0
        }

class AnalogyEngine:
    """Finds analogies between different domains"""
    def __init__(self):
        self.analogies = []
        self.mapping_cache = {}
        
    def find_structural_similarity(self, domain_a, domain_b):
        """Compare structural patterns between domains"""
        struct_a = domain_a.extract_abstract_structure()
        struct_b = domain_b.extract_abstract_structure()
        
        if not struct_a or not struct_b:
            return 0.0
        
        # Compare abstract properties
        props_a = set(struct_a['abstract_properties'])
        props_b = set(struct_b['abstract_properties'])
        
        if not props_a or not props_b:
            return 0.0
        
        overlap = props_a.intersection(props_b)
        similarity = len(overlap) / max(len(props_a), len(props_b))
        
        return similarity
    
    def create_analogy(self, source_domain, target_domain, mapping):
        """Map concepts from source to target domain"""
        analogy = {
            'source': source_domain.name,
            'target': target_domain.name,
            'mapping': mapping,
            'created': datetime.now().isoformat(),
            'strength': self.find_structural_similarity(source_domain, target_domain)
        }
        
        self.analogies.append(analogy)
        return analogy
    
    def apply_analogy(self, source_concept, source_domain_name, target_domain_name):
        """Transfer concept from one domain to another"""
        # Find relevant analogy
        relevant = None
        for analogy in self.analogies:
            if analogy['source'] == source_domain_name and analogy['target'] == target_domain_name:
                relevant = analogy
                break
        
        if not relevant:
            return None
        
        # Apply mapping
        target_concept = relevant['mapping'].get(source_concept)
        
        return {
            'source_concept': source_concept,
            'target_concept': target_concept,
            'confidence': relevant['strength']
        }

class AbstractionLayer:
    """Extracts and stores abstract patterns"""
    def __init__(self):
        self.abstract_patterns = []
        self.concept_hierarchy = {}
        
    def abstract_from_examples(self, examples):
        """Find common structure across examples"""
        if not examples:
            return None
        
        # Find common features
        all_features = []
        for example in examples:
            all_features.extend(example.get('features', []))
        
        feature_counts = Counter(all_features)
        common_features = [f for f, count in feature_counts.items() 
                          if count >= len(examples) * 0.5]
        
        abstraction = {
            'type': 'pattern',
            'common_features': common_features,
            'examples': len(examples),
            'generality': len(common_features) / len(set(all_features)) if all_features else 0
        }
        
        self.abstract_patterns.append(abstraction)
        return abstraction
    
    def generalize_concept(self, specific_concepts):
        """Create higher-level concept from specific ones"""
        if not specific_concepts:
            return None
        
        # Extract shared properties
        shared = None
        for concept in specific_concepts:
            props = set(concept.get('properties', {}).keys())
            if shared is None:
                shared = props
            else:
                shared = shared.intersection(props)
        
        general_concept = {
            'level': 'abstract',
            'shared_properties': list(shared) if shared else [],
            'specialized_from': len(specific_concepts),
            'created': datetime.now().isoformat()
        }
        
        return general_concept
    
    def find_category(self, instance):
        """Classify instance into abstract category"""
        best_match = None
        best_score = 0
        
        for pattern in self.abstract_patterns:
            instance_features = set(instance.get('features', []))
            pattern_features = set(pattern['common_features'])
            
            if not pattern_features:
                continue
            
            match_score = len(instance_features.intersection(pattern_features)) / len(pattern_features)
            
            if match_score > best_score:
                best_score = match_score
                best_match = pattern
        
        return {
            'category': best_match,
            'confidence': best_score
        }

class KnowledgeTransfer:
    """Transfers learned knowledge to new situations"""
    def __init__(self):
        self.transfer_history = []
        self.adaptation_rules = []
        
    def assess_transferability(self, source_knowledge, target_context):
        """Determine if knowledge can transfer"""
        # Check similarity
        source_features = set(source_knowledge.get('features', []))
        target_features = set(target_context.get('features', []))
        
        overlap = source_features.intersection(target_features)
        
        if not source_features:
            return 0.0
        
        transferability = len(overlap) / len(source_features)
        
        return transferability
    
    def transfer_skill(self, skill, from_domain, to_domain):
        """Apply skill from one domain to another"""
        transfer = {
            'skill': skill['skill'],
            'from_domain': from_domain,
            'to_domain': to_domain,
            'original_proficiency': skill['proficiency'],
            'transferred_proficiency': skill['proficiency'] * 0.7,  # Initial transfer penalty
            'timestamp': datetime.now().isoformat()
        }
        
        self.transfer_history.append(transfer)
        return transfer
    
    def adapt_knowledge(self, knowledge, new_context):
        """Modify knowledge to fit new context"""
        adapted = knowledge.copy()
        
        # Adjust based on context differences
        context_similarity = self.assess_transferability(knowledge, new_context)
        
        adapted['adapted'] = True
        adapted['adaptation_factor'] = context_similarity
        adapted['new_context'] = new_context
        adapted['confidence'] = knowledge.get('confidence', 1.0) * context_similarity
        
        return adapted
    
    def learn_adaptation_rule(self, original, adapted, success):
        """Learn how to better adapt knowledge"""
        rule = {
            'from_type': original.get('type'),
            'to_type': adapted.get('type'),
            'adaptation': 'successful' if success else 'failed',
            'learned': datetime.now().isoformat()
        }
        
        self.adaptation_rules.append(rule)
        return rule

class FewShotLearner:
    """Learn from minimal examples"""
    def __init__(self):
        self.prototypes = {}
        self.learning_curves = defaultdict(list)
        
    def learn_from_examples(self, category, examples):
        """Extract pattern from few examples"""
        if len(examples) < 1:
            return None
        
        # Create prototype by averaging features
        all_features = defaultdict(list)
        
        for example in examples:
            for feature, value in example.items():
                if isinstance(value, (int, float)):
                    all_features[feature].append(value)
        
        prototype = {}
        for feature, values in all_features.items():
            prototype[feature] = np.mean(values)
        
        self.prototypes[category] = {
            'prototype': prototype,
            'examples_seen': len(examples),
            'created': datetime.now().isoformat()
        }
        
        # Track learning
        self.learning_curves[category].append({
            'examples': len(examples),
            'timestamp': datetime.now().isoformat()
        })
        
        return self.prototypes[category]
    
    def classify_new_instance(self, instance):
        """Classify based on learned prototypes"""
        if not self.prototypes:
            return None
        
        best_category = None
        min_distance = float('inf')
        
        for category, proto_data in self.prototypes.items():
            prototype = proto_data['prototype']
            
            # Calculate distance
            distance = 0
            for feature, value in instance.items():
                if feature in prototype and isinstance(value, (int, float)):
                    distance += (value - prototype[feature]) ** 2
            
            distance = np.sqrt(distance)
            
            if distance < min_distance:
                min_distance = distance
                best_category = category
        
        return {
            'category': best_category,
            'confidence': 1.0 / (1.0 + min_distance),
            'distance': float(min_distance)
        }
    
    def update_with_feedback(self, instance, true_category):
        """Improve from feedback"""
        if true_category not in self.prototypes:
            self.prototypes[true_category] = {
                'prototype': instance.copy(),
                'examples_seen': 1,
                'created': datetime.now().isoformat()
            }
        else:
            # Update prototype (running average)
            proto = self.prototypes[true_category]['prototype']
            n = self.prototypes[true_category]['examples_seen']
            
            for feature, value in instance.items():
                if isinstance(value, (int, float)):
                    if feature in proto:
                        proto[feature] = (proto[feature] * n + value) / (n + 1)
                    else:
                        proto[feature] = value
            
            self.prototypes[true_category]['examples_seen'] += 1
        
        return True

class TransferLearningService:
    """Main AGI Transfer Learning & Generalization Service"""
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.domains = {}
        self.analogy_engine = AnalogyEngine()
        self.abstraction = AbstractionLayer()
        self.transfer = KnowledgeTransfer()
        self.few_shot = FewShotLearner()
        self.transfer_count = 0
        
        self._bootstrap_domains()
    
    def _bootstrap_domains(self):
        """Create initial domain knowledge"""
        # Math domain
        math_domain = DomainKnowledge('mathematics')
        math_domain.add_concept('addition', {'operation': 'binary', 'commutative': True})
        math_domain.add_concept('multiplication', {'operation': 'binary', 'commutative': True})
        math_domain.add_pattern('associative_law', 0.95)
        self.domains['mathematics'] = math_domain
        
        # Programming domain
        prog_domain = DomainKnowledge('programming')
        prog_domain.add_concept('function', {'operation': 'transform', 'reusable': True})
        prog_domain.add_concept('loop', {'operation': 'repeat', 'conditional': True})
        prog_domain.add_pattern('modular_design', 0.90)
        self.domains['programming'] = prog_domain
    
    def learn_in_domain(self, domain_name, concept_id, properties):
        """Learn new concept in specific domain"""
        if domain_name not in self.domains:
            self.domains[domain_name] = DomainKnowledge(domain_name)
        
        self.domains[domain_name].add_concept(concept_id, properties)
        
        return {'learned': True, 'domain': domain_name, 'concept': concept_id}
    
    def transfer_knowledge(self, from_domain, to_domain, concept):
        """Transfer knowledge between domains"""
        if from_domain not in self.domains or to_domain not in self.domains:
            return {'error': 'Domain not found'}
        
        # Create analogy if doesn't exist
        existing_analogy = None
        for analogy in self.analogy_engine.analogies:
            if analogy['source'] == from_domain and analogy['target'] == to_domain:
                existing_analogy = analogy
                break
        
        if not existing_analogy:
            mapping = {concept: f"{concept}_in_{to_domain}"}
            self.analogy_engine.create_analogy(
                self.domains[from_domain],
                self.domains[to_domain],
                mapping
            )
        
        # Apply transfer
        result = self.analogy_engine.apply_analogy(concept, from_domain, to_domain)
        self.transfer_count += 1
        
        return result
    
    def generalize_from_examples(self, examples):
        """Create general pattern from specific examples"""
        abstraction = self.abstraction.abstract_from_examples(examples)
        
        return {
            'abstraction': abstraction,
            'generalized': True,
            'from_examples': len(examples)
        }
    
    def quick_learn(self, category, examples):
        """Few-shot learning"""
        result = self.few_shot.learn_from_examples(category, examples)
        
        return {
            'learned': True,
            'category': category,
            'from_examples': len(examples),
            'prototype': result
        }
    
    def apply_to_new_context(self, knowledge, context):
        """Adapt knowledge to new situation"""
        adapted = self.transfer.adapt_knowledge(knowledge, context)
        
        return {
            'adapted': True,
            'original_confidence': knowledge.get('confidence', 1.0),
            'new_confidence': adapted['confidence'],
            'context': context
        }
    
    def execute(self):
        """Service interface for Titan swarm"""
        return {
            "id": self.id,
            "module": self.name,
            "status": "TRANSFERRING",
            "domains_learned": len(self.domains),
            "analogies_created": len(self.analogy_engine.analogies),
            "abstract_patterns": len(self.abstraction.abstract_patterns),
            "transfers_performed": self.transfer_count,
            "few_shot_categories": len(self.few_shot.prototypes),
            "generalizing": True
        }

# Example usage
if __name__ == "__main__":
    brain = TransferLearningService("AGI_BRAIN_06", "Transfer Learning Engine")
    
    # Learn in domain
    brain.learn_in_domain('physics', 'force', {'vector': True, 'measurable': True})
    
    # Transfer knowledge
    transfer = brain.transfer_knowledge('mathematics', 'programming', 'addition')
    print(f"Transfer: {transfer}")
    
    # Few-shot learning
    examples = [
        {'size': 10, 'weight': 5},
        {'size': 12, 'weight': 6},
        {'size': 11, 'weight': 5.5}
    ]
    learned = brain.quick_learn('object_type_A', examples)
    print(f"\nFew-shot: {learned}")
    
    # Classify new instance
    new_instance = {'size': 10.5, 'weight': 5.2}
    classification = brain.few_shot.classify_new_instance(new_instance)
    print(f"\nClassification: {classification}")
    
    print(f"\nStatus: {brain.execute()}")