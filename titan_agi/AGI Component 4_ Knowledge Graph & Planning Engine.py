"""
TITAN AGI - KNOWLEDGE GRAPH & PLANNING SYSTEM
Add this to backend/modules/agi_brain_04.py
"""

import json
import os
from collections import defaultdict, deque
from datetime import datetime
import heapq

class KnowledgeGraph:
    """Semantic network of concepts and relationships"""
    def __init__(self):
        self.nodes = {}  # entity_id -> {name, type, properties}
        self.edges = defaultdict(list)  # entity_id -> [(relation, target_id, weight)]
        self.reverse_edges = defaultdict(list)  # For backtracking
        
    def add_entity(self, entity_id, name, entity_type, properties=None):
        """Add a concept/entity to knowledge graph"""
        self.nodes[entity_id] = {
            'name': name,
            'type': entity_type,
            'properties': properties or {},
            'created': datetime.now().isoformat()
        }
    
    def add_relation(self, from_id, relation, to_id, weight=1.0):
        """Link two entities with a relationship"""
        if from_id not in self.nodes or to_id not in self.nodes:
            return False
        
        self.edges[from_id].append({
            'relation': relation,
            'target': to_id,
            'weight': weight
        })
        
        self.reverse_edges[to_id].append({
            'relation': relation,
            'source': from_id,
            'weight': weight
        })
        
        return True
    
    def get_entity(self, entity_id):
        """Retrieve entity information"""
        return self.nodes.get(entity_id)
    
    def get_relations(self, entity_id, relation_type=None):
        """Get all relations for an entity"""
        relations = self.edges.get(entity_id, [])
        
        if relation_type:
            relations = [r for r in relations if r['relation'] == relation_type]
        
        return relations
    
    def find_path(self, start_id, end_id, max_depth=5):
        """Find connection path between two entities (BFS)"""
        if start_id not in self.nodes or end_id not in self.nodes:
            return None
        
        queue = deque([(start_id, [start_id])])
        visited = {start_id}
        
        while queue:
            current, path = queue.popleft()
            
            if len(path) > max_depth:
                continue
            
            if current == end_id:
                return path
            
            for edge in self.edges.get(current, []):
                target = edge['target']
                if target not in visited:
                    visited.add(target)
                    queue.append((target, path + [target]))
        
        return None
    
    def query_by_pattern(self, entity_type=None, relation=None, target_type=None):
        """Find entities matching a pattern"""
        results = []
        
        for entity_id, entity in self.nodes.items():
            if entity_type and entity['type'] != entity_type:
                continue
            
            if relation or target_type:
                for edge in self.edges.get(entity_id, []):
                    if relation and edge['relation'] != relation:
                        continue
                    
                    target = self.nodes.get(edge['target'])
                    if target_type and target['type'] != target_type:
                        continue
                    
                    results.append({
                        'entity': entity_id,
                        'relation': edge['relation'],
                        'target': edge['target']
                    })
            else:
                results.append({'entity': entity_id})
        
        return results
    
    def get_neighbors(self, entity_id, hops=1):
        """Get all entities within N hops"""
        if entity_id not in self.nodes:
            return []
        
        neighbors = set([entity_id])
        current_level = {entity_id}
        
        for _ in range(hops):
            next_level = set()
            for node in current_level:
                for edge in self.edges.get(node, []):
                    next_level.add(edge['target'])
            neighbors.update(next_level)
            current_level = next_level
        
        return list(neighbors)

class GoalPlanner:
    """Multi-step planning and goal management"""
    def __init__(self):
        self.goals = []
        self.active_plans = {}
        self.plan_counter = 0
    
    def create_goal(self, description, priority=1):
        """Define a new goal"""
        goal = {
            'id': f"goal_{self.plan_counter}",
            'description': description,
            'priority': priority,
            'status': 'pending',
            'created': datetime.now().isoformat(),
            'plan': None
        }
        self.goals.append(goal)
        self.plan_counter += 1
        return goal['id']
    
    def decompose_goal(self, goal_description):
        """Break goal into actionable sub-goals"""
        # Simple heuristic decomposition
        steps = []
        
        # Parse goal for key verbs
        keywords = {
            'build': ['design', 'implement', 'test', 'deploy'],
            'learn': ['research', 'practice', 'evaluate', 'master'],
            'create': ['plan', 'draft', 'refine', 'finalize'],
            'solve': ['analyze', 'brainstorm', 'implement', 'verify']
        }
        
        goal_lower = goal_description.lower()
        
        for verb, substeps in keywords.items():
            if verb in goal_lower:
                steps = [f"{step} {goal_description.split(verb)[-1]}" 
                        for step in substeps]
                break
        
        if not steps:
            steps = [
                f"Phase 1: {goal_description}",
                f"Phase 2: Execute",
                f"Phase 3: Validate"
            ]
        
        return steps
    
    def create_plan(self, goal_id):
        """Generate execution plan for a goal"""
        goal = next((g for g in self.goals if g['id'] == goal_id), None)
        if not goal:
            return None
        
        steps = self.decompose_goal(goal['description'])
        
        plan = {
            'goal_id': goal_id,
            'steps': [
                {
                    'id': i,
                    'action': step,
                    'status': 'pending',
                    'dependencies': [i-1] if i > 0 else []
                }
                for i, step in enumerate(steps)
            ],
            'current_step': 0,
            'status': 'active'
        }
        
        goal['plan'] = plan
        self.active_plans[goal_id] = plan
        
        return plan
    
    def execute_step(self, goal_id, step_id):
        """Execute a single step of the plan"""
        plan = self.active_plans.get(goal_id)
        if not plan:
            return {'error': 'Plan not found'}
        
        step = plan['steps'][step_id]
        
        # Check dependencies
        for dep in step['dependencies']:
            dep_step = plan['steps'][dep]
            if dep_step['status'] != 'completed':
                return {'error': 'Dependencies not met', 'blocked_by': dep}
        
        # Simulate execution
        step['status'] = 'in_progress'
        step['started'] = datetime.now().isoformat()
        
        # For demo, immediately complete
        step['status'] = 'completed'
        step['completed'] = datetime.now().isoformat()
        
        # Advance plan
        if step_id == len(plan['steps']) - 1:
            plan['status'] = 'completed'
        else:
            plan['current_step'] = step_id + 1
        
        return {'step': step, 'plan_status': plan['status']}
    
    def get_next_action(self, goal_id):
        """Determine what to do next"""
        plan = self.active_plans.get(goal_id)
        if not plan or plan['status'] == 'completed':
            return None
        
        current_step = plan['steps'][plan['current_step']]
        
        return {
            'step_id': current_step['id'],
            'action': current_step['action'],
            'ready': all(
                plan['steps'][dep]['status'] == 'completed' 
                for dep in current_step['dependencies']
            )
        }

class HierarchicalPlanner:
    """HTN (Hierarchical Task Network) Planning"""
    def __init__(self):
        self.task_methods = {}  # task_name -> list of methods to achieve it
        self.primitive_actions = set()
    
    def add_method(self, task_name, method_steps):
        """Define how to achieve a task"""
        if task_name not in self.task_methods:
            self.task_methods[task_name] = []
        
        self.task_methods[task_name].append(method_steps)
    
    def add_primitive(self, action_name):
        """Define a basic executable action"""
        self.primitive_actions.add(action_name)
    
    def decompose(self, task, depth=0, max_depth=5):
        """Recursively decompose task into primitives"""
        if depth > max_depth:
            return None
        
        # If primitive, return as is
        if task in self.primitive_actions:
            return [task]
        
        # If compound, try methods
        if task in self.task_methods:
            for method in self.task_methods[task]:
                plan = []
                for subtask in method:
                    subplan = self.decompose(subtask, depth + 1, max_depth)
                    if subplan is None:
                        break
                    plan.extend(subplan)
                else:
                    return plan
        
        return None

class AStarPlanner:
    """A* pathfinding for state-space planning"""
    def __init__(self):
        self.state_space = {}
        self.actions = []
    
    def add_action(self, name, preconditions, effects, cost=1):
        """Define an action that changes state"""
        self.actions.append({
            'name': name,
            'preconditions': preconditions,
            'effects': effects,
            'cost': cost
        })
    
    def is_applicable(self, action, state):
        """Check if action can be applied in current state"""
        return all(state.get(k) == v for k, v in action['preconditions'].items())
    
    def apply_action(self, action, state):
        """Apply action to get new state"""
        new_state = state.copy()
        new_state.update(action['effects'])
        return new_state
    
    def heuristic(self, state, goal):
        """Estimate distance to goal"""
        return sum(1 for k, v in goal.items() if state.get(k) != v)
    
    def plan(self, initial_state, goal_state):
        """Find plan using A* search"""
        open_set = []
        heapq.heappush(open_set, (0, 0, initial_state, []))
        
        closed_set = set()
        
        while open_set:
            f_score, g_score, state, path = heapq.heappop(open_set)
            
            state_tuple = tuple(sorted(state.items()))
            if state_tuple in closed_set:
                continue
            closed_set.add(state_tuple)
            
            # Goal check
            if all(state.get(k) == v for k, v in goal_state.items()):
                return path
            
            # Expand
            for action in self.actions:
                if self.is_applicable(action, state):
                    new_state = self.apply_action(action, state)
                    new_g = g_score + action['cost']
                    new_f = new_g + self.heuristic(new_state, goal_state)
                    
                    heapq.heappush(open_set, (
                        new_f,
                        new_g,
                        new_state,
                        path + [action['name']]
                    ))
        
        return None

class KnowledgePlanningService:
    """Main AGI Knowledge & Planning Service"""
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.knowledge = KnowledgeGraph()
        self.planner = GoalPlanner()
        self.htn = HierarchicalPlanner()
        self.astar = AStarPlanner()
        
        self._bootstrap_knowledge()
    
    def _bootstrap_knowledge(self):
        """Load initial knowledge"""
        # Entities
        self.knowledge.add_entity('ai', 'Artificial Intelligence', 'concept')
        self.knowledge.add_entity('ml', 'Machine Learning', 'concept')
        self.knowledge.add_entity('dl', 'Deep Learning', 'concept')
        self.knowledge.add_entity('nn', 'Neural Networks', 'technology')
        
        # Relations
        self.knowledge.add_relation('dl', 'is_subset_of', 'ml', 0.9)
        self.knowledge.add_relation('ml', 'is_subset_of', 'ai', 0.9)
        self.knowledge.add_relation('nn', 'enables', 'dl', 0.95)
        
        # HTN methods
        self.htn.add_primitive('code')
        self.htn.add_primitive('test')
        self.htn.add_primitive('deploy')
        self.htn.add_method('build_app', ['code', 'test', 'deploy'])
        
        # Planning actions
        self.astar.add_action('write_code', {'idea': True}, {'code': True}, 2)
        self.astar.add_action('test_code', {'code': True}, {'tested': True}, 1)
        self.astar.add_action('deploy_code', {'tested': True}, {'deployed': True}, 1)
    
    def learn_concept(self, concept_id, name, related_to=None):
        """Add new concept to knowledge base"""
        self.knowledge.add_entity(concept_id, name, 'concept')
        
        if related_to:
            self.knowledge.add_relation(concept_id, 'related_to', related_to, 0.7)
        
        return {'learned': True, 'concept': concept_id}
    
    def reason_about(self, entity_id):
        """Use knowledge graph to reason"""
        entity = self.knowledge.get_entity(entity_id)
        if not entity:
            return {'found': False}
        
        relations = self.knowledge.get_relations(entity_id)
        neighbors = self.knowledge.get_neighbors(entity_id, hops=2)
        
        return {
            'entity': entity,
            'direct_relations': len(relations),
            'knowledge_neighborhood': len(neighbors),
            'relations': relations[:5]  # Top 5
        }
    
    def plan_goal(self, goal_description):
        """Create and plan a goal"""
        goal_id = self.planner.create_goal(goal_description, priority=1)
        plan = self.planner.create_plan(goal_id)
        
        return {
            'goal_id': goal_id,
            'plan': plan,
            'steps': len(plan['steps']) if plan else 0
        }
    
    def execute(self):
        """Service interface for Titan swarm"""
        return {
            "id": self.id,
            "module": self.name,
            "status": "PLANNING",
            "entities_known": len(self.knowledge.nodes),
            "relations_known": sum(len(edges) for edges in self.knowledge.edges.values()),
            "active_goals": len(self.planner.goals),
            "active_plans": len(self.planner.active_plans),
            "planning_active": True
        }

# Example usage
if __name__ == "__main__":
    brain = KnowledgePlanningService("AGI_BRAIN_04", "Knowledge & Planning Engine")
    
    # Test knowledge
    brain.learn_concept('agi', 'Artificial General Intelligence', 'ai')
    reasoning = brain.reason_about('ai')
    print(f"Knowledge: {reasoning}")
    
    # Test planning
    plan = brain.plan_goal("Build a web application")
    print(f"\nPlan: {plan}")
    
    print(f"\nStatus: {brain.execute()}")