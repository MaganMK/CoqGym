import json
from abc import ABC, abstractmethod
import eval_helpers

class Agent(ABC):
    def __init__(self, opts):
        self.opts = opts
        with open(self.opts.tactics) as f: self.tactics = json.load(f)
        
        ''' environment and state '''
        self.proof_env = None
        self.state = None # triplet -> (goal, local context, global context)        


    def reset(self, proof_env):
        self.proof_env = proof_env
        local_state = proof_env.init()
        goal, lc = eval_helpers.process_local_env(local_state)
        gc = eval_helpers.process_global_context(local_state)
        self.state = (goal, lc, gc)

    def update_state(self, local_state):
        if local_state['result'] == "PROVING":
            gc = self.state[2]
            goal, lc = eval_helpers.process_local_env(local_state)
            self.state = (goal, lc, gc)
        
        
    def make_action(self, action):
        local_state = self.proof_env.step(f'{action}.')
        result = local_state['result']
        self.update_state(local_state)
        return result


    def prove(self, proof_env):
        res, script = self.prove_DFS(proof_env)
        return res, script

    def prove_DFS(self, proof_env):
        self.reset(proof_env)
        node_ids = set() # keep track of all nodes seen so far
        root_id = eval_helpers.state_id(self.state)
        node_ids.add(root_id)
        
        # initialize the stack
        stack = []
        stack.append(self.get_candidates())
        script = []

        
        # depth-first search starting from the trace
        while stack != [[]]:
            # pick a tactic
            if stack[-1] == []:  # all candidate have been tried, backtrack
                stack.pop()
                script.pop()
                local_state = self.proof_env.step("Undo.")
                self.update_state(local_state)
                continue
            else:
                tac = stack[-1].pop(0)
            
            result = self.make_action(tac)

            if result == "SUCCESS":            
                script.append(tac)
                return True, script
            elif result in ["MAX_NUM_TACTICS_REACHED", "MAX_TIME_REACHED"]:
                return False, script
            elif result in ["ERROR"]:
                continue
            else:                
                assert result == "PROVING"
                script.append(tac)
                sig = eval_helpers.state_id(self.state)

                if sig in node_ids or len(script) >= self.opts.depth_limit:
                    local_state = self.proof_env.step("Undo.")
                    self.update_state(local_state)
                    script.pop()
                    continue

                node_ids.add(sig)
                stack.append(self.get_candidates())

        state = proof_env.step("Admitted.")
        return False, script


    @abstractmethod
    def get_candidates(self):
        pass
