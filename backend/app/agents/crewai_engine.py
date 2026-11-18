import time
import logging
from typing import List, Dict, Any, Optional, Union
from enum import Enum

from app.services.llm_service import llm_service

logger = logging.getLogger("crewai_engine")

class Process(Enum):
    sequential = "sequential"
    hierarchical = "hierarchical"

class TaskOutput:
    def __init__(self, description: str, raw: str, agent_role: str, execution_time_ms: int = 0):
        self.description = description
        self.raw = raw
        self.agent_role = agent_role
        self.execution_time_ms = execution_time_ms

    def __str__(self):
        return self.raw

class CrewOutput:
    def __init__(self, raw: str, tasks_output: List[TaskOutput]):
        self.raw = raw
        self.tasks_output = tasks_output

    def __str__(self):
        return self.raw

class Agent:
    """
    CrewAI-compatible Agent class representing an autonomous banking intelligence specialist.
    """
    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        tools: Optional[List[Any]] = None,
        verbose: bool = True,
        allow_delegation: bool = False,
        llm: Optional[Any] = None
    ):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.verbose = verbose
        self.allow_delegation = allow_delegation
        self.llm = llm

    def execute_task(self, task: 'Task', context: Optional[str] = None) -> TaskOutput:
        """
        Executes an assigned task by combining the agent's backstory, goal,
        task instructions, predecessor context, and tools.
        """
        t0 = time.time()
        if self.verbose:
            logger.info(f"[{self.role}] Starting task: {task.name or task.description[:60]}")

        prompt = (
            f"Role: {self.role}\n"
            f"Goal: {self.goal}\n"
            f"Backstory: {self.backstory}\n\n"
            f"Task: {task.description}\n"
            f"Expected Output: {task.expected_output}\n"
        )
        if context:
            prompt += f"\n--- Context from Previous Collaborative Agents ---\n{context}\n"

        # Execute using LLM Service or grounded domain logic
        output_text = task.execute_fn(prompt, context) if task.execute_fn else task.description
        duration_ms = int((time.time() - t0) * 1000)

        return TaskOutput(
            description=task.description,
            raw=output_text,
            agent_role=self.role,
            execution_time_ms=duration_ms
        )

class Task:
    """
    CrewAI-compatible Task class defining an agent's objective, expected output,
    and upstream context dependencies.
    """
    def __init__(
        self,
        description: str,
        expected_output: str,
        agent: Agent,
        name: Optional[str] = None,
        context: Optional[List['Task']] = None,
        tools: Optional[List[Any]] = None,
        execute_fn: Optional[Any] = None
    ):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.name = name or description[:40]
        self.context = context or []
        self.tools = tools or []
        self.execute_fn = execute_fn
        self.output: Optional[TaskOutput] = None

class Crew:
    """
    CrewAI-compatible Crew class orchestrating collaborative multi-agent execution
    with sequential context passing and execution tracking.
    """
    def __init__(
        self,
        agents: List[Agent],
        tasks: List[Task],
        process: Process = Process.sequential,
        verbose: bool = True
    ):
        self.agents = agents
        self.tasks = tasks
        self.process = process
        self.verbose = verbose

    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> CrewOutput:
        """
        Kicks off sequential agent execution, passing the output of previous tasks
        into the downstream tasks specified in their context dependency list.
        """
        tasks_output: List[TaskOutput] = []

        for idx, task in enumerate(self.tasks):
            # Gather context from predecessor tasks
            context_pieces = []
            for ctx_task in task.context:
                if ctx_task.output:
                    context_pieces.append(
                        f"[{ctx_task.agent.role} Output]:\n{ctx_task.output.raw}"
                    )
            combined_context = "\n\n".join(context_pieces) if context_pieces else None

            # Execute task with agent
            task_out = task.agent.execute_task(task, context=combined_context)
            task.output = task_out
            tasks_output.append(task_out)

        final_raw = tasks_output[-1].raw if tasks_output else "Execution Complete."
        return CrewOutput(raw=final_raw, tasks_output=tasks_output)
