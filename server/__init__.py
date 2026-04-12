class EmailEnv:
    def __init__(self, task="easy"):
        self.task = str(task).lower().strip()

        if self.task not in ["easy", "medium", "hard"]:
            self.task = "easy"