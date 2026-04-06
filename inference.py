import asyncio
from email_env import EmailEnv, Action

TASK_NAME = "hard"
BENCHMARK = "email_triage_env"
MODEL_NAME = "dummy-model"

async def main():
    env = EmailEnv(task=TASK_NAME)

    # START log
    print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}")

    obs = env.reset()

    # For now we simulate AI (later real model)
    action = Action(label="spam", response="I will block this spam email")

    result = env.step(action)

    reward = result[1]
    done = result[2]

    # STEP log
    print(f"[STEP] step=1 action={action.label} reward={reward:.2f} done={str(done).lower()} error=null")

    # END log
    success = reward >= 0.5
    print(f"[END] success={str(success).lower()} steps=1 rewards={reward:.2f}")

if __name__ == "__main__":
    asyncio.run(main())