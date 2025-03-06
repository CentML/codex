## Table of contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)

## Introduction
Here is a simple example demonstrating how to request responses in strictly formatted JSON. Useful when LLM is being used as an API.

You can find more details in [JSON Schema Output documentation](https://docs.centml.ai/resources/json_and_tool#json-schema-output)

## Installation
```zsh
pip install openai
```

## Usage
Supply your API key from https://app.centml.com/user/vault
```zsh
CENTML_API_KEY="Your token" python json-mode-example.py
```