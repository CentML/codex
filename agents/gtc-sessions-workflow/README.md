# DeepSeek-ing a Needle in a Haystack

Leveraging Agentic Workflows to Find the Best GTC 2025 Sessions with CentML

For more background, you can finFind the blog post [here](https://centml.ai/blog/best-gtc-sessions-with-centml/).

## Quick Start

1. [Install temporal and setup the sdk](https://learn.temporal.io/getting_started/python/dev_environment/).
    ```bash
    temporal server start-dev
    ```
1. In a separate terminal, start the worker:
    ```bash
    pip install -r requirements.txt
    python worker.py
    ```
1. In another separate terminal, start the workflow after exporting your [CentML API key](https://app.centml.com/user/vault):
    ```bash
    export CENTML_API_KEY=your_api_key
    python starter.py
    ```

You should now see the workflow running in the worker terminal.
