"""Role specialists — each module exposes:
  - render_prompt(input: dict) -> str
  - parse_output(raw: str, input: dict) -> dict | None  (None on parse fail)

Loaded by agents._agent.agent_call. Each role has fixed contract — see
config/agents_governance.yaml for input/output schemas.
"""
