import time
import logging
from typing import List, Dict, Any, Optional
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
    Powered by LLM reasoning with ground-truth data tools.
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
        Executes the assigned task by passing task description, predecessor context,
        and persona to the LLM Service (Gemini/OpenAI or grounded analytical engine).
        """
        t0 = time.time()
        if self.verbose:
            logger.info(f"[{self.role}] Executing: {task.name or task.description[:50]}")

        # Execute using LLM Service
        output_text = llm_service.generate_agent_analysis(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            task_description=task.description,
            expected_output=task.expected_output,
            kpis=task.kpis or {},
            context=context
        )
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
    upstream context dependencies, and tools.
    """
    def __init__(
        self,
        description: str,
        expected_output: str,
        agent: Agent,
        name: Optional[str] = None,
        context: Optional[List['Task']] = None,
        tools: Optional[List[Any]] = None,
        kpis: Optional[Dict[str, Any]] = None
    ):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.name = name or description[:40]
        self.context = context or []
        self.tools = tools or []
        self.kpis = kpis or {}
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
        Kicks off sequential agent execution, gathering output from predecessor tasks
        in context=[...] and passing it into downstream agents.
        """
        tasks_output: List[TaskOutput] = []

        for task in self.tasks:
            # Collect outputs from upstream context tasks
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
