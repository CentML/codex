"""Workflow for fetching and filtering GTC conference sessions.

This workflow orchestrates the process of:
1. Fetching sessions from the GTC conference API in batches
2. Filtering out non-English sessions
3. Evaluating sessions for AI/ML system optimization relevance
4. Maintaining a sorted list of the top most relevant sessions

The workflow uses multiple activities to process the sessions:
- fetch_sessions: Retrieves batches of sessions from the API
- filter_non_english_sessions: Removes non-English language sessions
- filter_sessions: Evaluates sessions for AI/ML optimization relevance
- process_sessions: Maintains sorted list of top relevant sessions

Returns:
    list[Session]: The top most relevant sessions discussing AI/ML system optimization
"""

from datetime import timedelta

from pydantic import BaseModel
from temporalio import workflow

with workflow.unsafe.imports_passed_through(): # Mark activities import as pass-through
    from activities import (FetchSessionsInput, FilterNonEnglishSessionsInput,
                            FilterSessionsInput, ProcessSessionsInput, Prompt,
                            Session, fetch_sessions,
                            filter_non_english_sessions, filter_sessions,
                            process_sessions)


class TopTenGTCSessionsWorkflowInput(BaseModel):
    """Input model for the GTC session filtering workflow.
    
    Contains API key and prompt configurations for filtering and comparing sessions."""
    api_key: str
    filter_prompt: Prompt
    compare_prompt: Prompt


@workflow.defn
class TopTenGTCSessionsWorkflow:
    """Workflow for fetching, filtering, and ranking GTC sessions by AI/ML system optimization relevance."""
    @workflow.run
    async def run(self, workflow_input: TopTenGTCSessionsWorkflowInput) -> list[Session]:
        """Execute workflow to fetch and rank GTC sessions, returning the top most relevant ones."""
        api_key = workflow_input.api_key
        min_sessions = []
        offset = None

        while True:

            print("fetching the next 25 sessions")
            # Workflow ONLY calls the activity            
            new_sessions = await workflow.execute_activity(
                fetch_sessions, # Call the activity
                FetchSessionsInput(from_offset=offset), # Pass the input
                start_to_close_timeout=timedelta(seconds=30),
            )
            if not new_sessions:
                print("no new sessions")
                break

            if offset is None:
                offset = len(new_sessions)
            else:            
                offset += len(new_sessions)

            print('offset in workflow', offset)

            # filter out non english sessions
            english_sessions = await workflow.execute_activity(
                filter_non_english_sessions,
                FilterNonEnglishSessionsInput(sessions=new_sessions),
                start_to_close_timeout=timedelta(seconds=5),
            )

            # save some time by filtering out sessions that are not relevant
            filtered_sessions = await workflow.execute_activity(
                filter_sessions,
                FilterSessionsInput(
                    sessions=english_sessions,
                    api_key=api_key,
                    prompt=workflow_input.filter_prompt
                ),
                start_to_close_timeout=timedelta(seconds=300),
            )

            print("filtered sessions ", len(new_sessions) - len(filtered_sessions))

            # Process the new sessions, comparing them to the existing list of min sessions 
            # and inserting them into the correct position
            min_sessions = await workflow.execute_activity(
                process_sessions,
                ProcessSessionsInput(
                    min_sessions=min_sessions,
                    new_sessions=filtered_sessions,
                    api_key=api_key,
                    prompt=workflow_input.compare_prompt
                ),
                start_to_close_timeout=timedelta(seconds=600),
            )

            print("processed sessions ", offset) 

        return min_sessions