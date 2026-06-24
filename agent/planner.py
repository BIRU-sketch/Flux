from ai import AI,IDENTITY
ai = AI()
class Plan:
    def __init__(self):
        self.identity = IDENTITY
        self.planner = self.identity
    def plan(self, prompt):
        response = ai.respond(prompt, self.planner)
        return response
plan=Plan()
print(plan.plan("I want you to clean my desktop folder"))