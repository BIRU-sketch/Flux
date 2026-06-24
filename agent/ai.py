from openai import OpenAI
import json

class AI:
    def __init__(self, api_key=""):
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key='')
        self.model = "cohere/north-mini-code:free"
        self.IDENTITY = """You are part of desktop automation software in a Linux environment with ubuntu os. When the user has a request, respond ONLY with valid JSON containing: steps (array of bash commands to execute sequentially), explanation (brief reason for these steps), undo (array of bash commands to undo the steps). No other text, only JSON. Create detailed plans—don't assume the executor can infer steps. Do not add '' or "" in at the start and end of the json and make sure you return a clean json."""
    def plan_task(self, user_request):
        """Plan a task from natural language"""
        response = self.respond(user_request, plan=self.IDENTITY)
        with open("plan.json", "w") as f:
            json.dump(json.loads(response), f, indent=4)
        return self._parse_json(response)
    
    def respond(self, prompt, plan=None):
        messages = []
        if plan is not None:
            messages.append({'role': 'system', 'content': plan})
        messages.append({'role': 'user', 'content': prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
    
    def _parse_json(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON", "raw": response}
    
    def refine_plan(self, plan, feedback):
        prompt = f"Refine this plan based on feedback: {feedback}\n\nCurrent plan: {json.dumps(plan)}"
        return self._parse_json(self.respond(prompt, plan=self.IDENTITY))
