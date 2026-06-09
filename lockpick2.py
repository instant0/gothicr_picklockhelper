#!/usr/bin/env python3
"""
State-Transition Puzzle Solver v6
Correctly handles ONE-WAY rules with proper side-effect calculation.
No automatic inverse rules - only what's explicitly stated.
"""

import sys
import heapq

MIN_VAL = 1
MAX_VAL = 7
GOAL_VALUE = 4

class SliderPuzzleSolver:
    def __init__(self):
        self.rules = {}  # {source_id: [(target_id, multiplier), ...]}
        self.sliders = set()
        
    def parse_rules(self):
        print("\n=== RULE INPUT ===")
        print("Format: Source +/-, Target1 +/- ... (ONE-WAY only)")
        print("Example: S4 +, S1+, S2+, S3+, S5-")
        print("Moving S4- will cause opposite effects:")
        print("  S4- → S1-, S2-, S3-, S5+")
        print("Press ENTER alone when done.\n")
        
        rule_num = 1
        while True:
            try:
                line = input(f"Rule {rule_num}: ").strip()
                if not line:
                    if rule_num > 1:
                        break
                    print("Please enter at least one rule.")
                    continue
                
                parts = line.split(',')
                source_id = None
                source_dir = 1
                affected = []
                
                for part in parts:
                    part = part.strip().replace(' ', '')
                    if not part:
                        continue
                    
                    parsed = self._parse_part(part)
                    if not parsed:
                        continue
                        
                    sid, direction = parsed
                    self.sliders.add(sid)
                    
                    if source_id is None:
                        source_id = sid
                        source_dir = direction
                    else:
                        # Multiplier = direction * source_dir
                        # Example: "S4+, S1+" => mult = 1*1 = +1 (same direction)
                        #          "S4+, S5-" => mult = 1*-1 = -1 (opposite direction)
                        multiplier = direction * source_dir
                        affected.append((sid, multiplier))
                
                if source_id:
                    if source_id not in self.rules:
                        self.rules[source_id] = []
                    self.rules[source_id].extend(affected)

                rule_num += 1
            except EOFError:
                break
        
        independent = self.sliders - set(self.rules.keys())
        print(f"\n[INFO] Rules loaded. Sliders: {sorted(self.sliders)}")
        print(f"[INFO] Independent sliders: {sorted(independent)}")
        print("[INFO] One-way rules only (no automatic inverses).\n")

    def _parse_part(self, part):
        if not part or not part.startswith('S'):
            return None
        idx = 1
        while idx < len(part) and part[idx].isdigit():
            idx += 1
        num_str = part[1:idx]
        if not num_str:
            return None
        sid = f"S{num_str}"
        sign = 1
        if idx < len(part):
            if part[idx] == '+': sign = 1
            elif part[idx] == '-': sign = -1
        return (sid, sign)

    def get_state(self, label="Current"):
        print(f"\n=== {label} STATE ===")
        line = input(f"{label} State: ").strip()
        state = {}
        if line:
            items = line.split(',')
            for item in items:
                parts = item.strip().split()
                if len(parts) >= 2:
                    sid = parts[0]
                    try:
                        val = int(parts[1])
                        state[sid] = val
                        self.sliders.add(sid)
                    except ValueError:
                        pass
        for s in sorted(self.sliders):
            if s not in state:
                state[s] = 1
        return state

    def apply_move(self, current_state, slider, delta):
        """Apply move with side effects (ONE-WAY rules)."""
        new_state = dict(current_state)
        
        # Direct change to moved slider
        new_state[slider] = new_state.get(slider, 1) + delta
        
        # Linked effects ONLY if this slider has rules defined
        if slider in self.rules:
            for target, mult in self.rules[slider]:
                if target in new_state:
                    # delta * mult applies the effect
                    # Example: S4- (delta=-1) with S4+→S1+ (mult=+1) => S1 gets -1*1 = -1
                    new_state[target] = new_state[target] + (delta * mult)
        
        return new_state

    def is_valid(self, state):
        return all(MIN_VAL <= v <= MAX_VAL for v in state.values())

    def is_goal(self, state):
        return all(v == GOAL_VALUE for v in state.values())

    def heuristic(self, state):
        dist = 0
        for s in self.sliders:
            dist += abs(state.get(s, 1) - GOAL_VALUE)
        return dist

    def solve_astar(self, start_state, max_iterations=100000):
        tiebreaker = 0
        start_h = self.heuristic(start_state)
        state_hash = tuple(sorted(start_state.items()))
        heap = [(start_h, 0, tiebreaker, state_hash, start_state, [])]
        
        visited = {state_hash}
        iterations = 0
        
        while heap:
            f, g, _, _, current, path = heapq.heappop(heap)
            
            if self.is_goal(current):
                return path
            
            iterations += 1
            if iterations > max_iterations:
                break
            
            for s in sorted(self.sliders):
                for d in [-1, 1]:
                    next_state = self.apply_move(current, s, d)
                    
                    if not self.is_valid(next_state):
                        continue
                    
                    key = tuple(sorted(next_state.items()))
                    if key not in visited:
                        visited.add(key)
                        action_desc = f"{s} {'+' if d > 0 else '-'}"
                        new_g = g + 1
                        new_h = self.heuristic(next_state)
                        new_f = new_g + new_h
                        tiebreaker += 1
                        heapq.heappush(heap, (new_f, new_g, tiebreaker, key, next_state, path + [(action_desc, next_state)]))
        
        return None

    def run(self):
        self.parse_rules()
        initial = self.get_state("Current")
        
        print("\n" + "="*60)
        print("SOLVING WITH A* SEARCH...")
        print(f"Initial: {initial}")
        print(f"Goal: All sliders = {GOAL_VALUE}")
        print("="*60 + "\n")
        
        solution = self.solve_astar(initial)
        
        if solution:
            print("="*60)
            print("OPTIMIZED SOLUTION FOUND")
            print("="*60)
            print(f"{'Move':<15} | {'State After Move'}")
            print("-"*60)
            
            for i, (move, state) in enumerate(solution, 1):
                sorted_keys = sorted(state.keys(), key=lambda x: int(x[1:]))
                state_str = ", ".join([f"{k}={state[k]}" for k in sorted_keys])
                print(f"{i}. {move:<14} | {state_str}")
            
            print("-"*60)
            print(f"Total Moves: {len(solution)}")
            print("="*60)
        else:
            print("\n✗ No solution found within iteration limit.")
            print("Try increasing max_iterations or check constraints.")

if __name__ == "__main__":
    print("="*60)
    print("STATE-TRANSITION PUZZLE SOLVER v6 (Fixed Side Effects)")
    print("="*60)
    
    solver = SliderPuzzleSolver()
    solver.run()