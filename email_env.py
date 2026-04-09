from pydantic import BaseModel
import random

class Observation(BaseModel):
    email_text: str

class Action(BaseModel):
    label: str
    response: str = "" 

class EmailEnv:

    def __init__(self, task="easy"):
        self.task = task
        self.dataset = [
            {"text": "You won a lottery!!!","label":"spam"},
            {"text": "Meeting at 3 PM tomorrow", "label": "important"},
            {"text": "50% discount on shoes!","label": "promotion"},
            {"text": "Project deadline extended to next week", "label": "important"},
            {"text": "Team meeting postponed to Friday", "label": "important"},
            {"text": "Please review the attached report", "label": "important"},

            {"text": "Flat 70% OFF on all items today!", "label": "promotion"},
            {"text": "Limited time offer, buy 1 get 1 free", "label": "promotion"},
            {"text": "Exclusive deals just for you", "label": "promotion"},

            {"text": "Congratulations! You have won $1000", "label": "spam"},
            {"text": "Click here to claim your reward now", "label": "spam"},
            {"text": "Urgent: Your account has been compromised, send password", "label": "spam"}
        ]
        self.current_email = None

    def get_tasks(self):
        return ["easy", "medium", "hard"]

    def reset(self):
        self.current_email = random.choice(self.dataset)
        return Observation(email_text=self.current_email["text"])
    
    def step(self, action: Action):
        correct_label = self.current_email["label"]

        reward = 0.5  # default safe

        if self.task == "easy":
            reward = self.grade_easy(action.label, correct_label)

        elif self.task == "medium":
            reward = self.grade_medium(action.label, correct_label)

        elif self.task == "hard":
            reward = self.grade_hard(action.label, correct_label, action.response)

        reward = float(reward)

        reward = max(0.01, min(0.99, float(reward)))

        done = True
        observation = Observation(email_text="")
        info = {
            "correct_label": correct_label,
            "agent_label": action.label
        }

        return observation, reward, done, info
    
    def state(self):
        return {
            "task": self.task,
            "current_email": self.current_email["text"]
        }
    
    def grade_easy(self, action_label, correct_label):
        action_label = str(action_label).lower().strip()
        correct_label = str(correct_label).lower().strip()

        if correct_label != "spam":
            correct_label = "not_spam"
        if action_label != "spam":
            action_label = "not_spam"

        reward = 0.8 if action_label == correct_label else 0.2

        return max(0.01, min(0.99, float(reward)))
        
    def grade_medium(self, action_label, correct_label):
        action_label = str(action_label).lower().strip()
        correct_label = str(correct_label).lower().strip()

        reward = 0.75 if action_label == correct_label else 0.25

        return max(0.01, min(0.99, float(reward)))
        
        
    def grade_hard(self, action_label, correct_label, response):
        action_label = str(action_label).lower().strip()
        correct_label = str(correct_label).lower().strip()
        response = str(response).lower()

        classification_reward = 0.6 if action_label == correct_label else 0.2
        response_reward = 0.1

        if correct_label == "important":
            if any(word in response for word in ["sure","will","attend","okay"]):
                response_reward = 0.3

        elif correct_label == "promotion":
            if any(word in response for word in ["not interested","unsubscribe","no thanks"]):
                response_reward = 0.3

        elif correct_label == "spam":
            if any(word in response for word in ["spam","block","report","delete"]):
                response_reward = 0.3

        final = classification_reward + response_reward

        return max(0.01, min(0.99, float(final)))
    
if __name__ == "__main__":
    env = EmailEnv(task="hard")
    print("Task:", env.task)

    obs = env.reset()
    print("Email:", obs.email_text)

    action = Action(label="spam",response="I will block this spam email")
    result = env.step(action)

    print("Result:", result)
    print(env.state())
    
    