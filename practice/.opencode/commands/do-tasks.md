---
description: Solves a sequence of tasks, always pausing for human review (basically a Ralph loop)
---

Tasks are prefixed with the order in which they can be executed

Done tasks are prefixed with "done", ignore them unless you need context from an earlier task

Select the first task that's not done and implement it

When ready, stop and ask the user for review and approval

When approved, add the "done" prefix to the filename and move on to the next task

Keep going like this until all the tasks are done

Do not try to work on multiple tasks in parallel

The location of task descriptions are explicitly provided by the user
