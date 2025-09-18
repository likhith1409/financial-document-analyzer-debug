import asyncio

class CustomCrew:
    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks

    async def kickoff(self, inputs):
        print(f"Tasks in kickoff: {self.tasks}")
        
        # Run tasks sequentially, passing the output of one to the next
        results = {}
        current_inputs = inputs.copy()

        for task in self.tasks:
            # Run the task with the current inputs
            result = await task.agent.run(current_inputs, task.tools)
            
            # Store the result
            results[task.description] = result
            
            # Update inputs for the next task
            current_inputs['previous_task_result'] = result
            
        return results
