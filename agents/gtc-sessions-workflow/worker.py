from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.contrib.pydantic import pydantic_data_converter
from workflows import TopTenGTCSessionsWorkflow
from activities import fetch_sessions, filter_sessions, process_sessions, filter_non_english_sessions, Session
import asyncio


async def run_worker():
    # Connect to the Temporal server (default: localhost:7233)
    client = await Client.connect("localhost:7233", data_converter=pydantic_data_converter)

    # Create a worker that runs the workflow and activity
    worker = Worker(
        client,
        task_queue="fetch-sessions-queue",
        workflows=[TopTenGTCSessionsWorkflow], # Workflow class
        activities=[fetch_sessions, process_sessions, filter_sessions, filter_non_english_sessions], # Activity function
    )

    # Start the worker and run indefinitely
    print("Starting worker...")
    try:
        await worker.run()
    except asyncio.CancelledError:
        print("Worker shut down.")
    except Exception as e:
        print(f"Worker failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_worker())