# NerdGraph Workflow Template

A foundation for building workflows that leverage New Relic's NerdGraph (GraphQL) API.

## Overview

This template repository provides the basic structure and utilities needed to create workflows that interact with New Relic's GraphQL API (NerdGraph). It's designed to simplify the process of building data extraction, transformation, and automation scripts that work with New Relic data.

## Features

- Pre-configured NerdGraph API client with built-in error handling and retry logic
- Organized directory structure for queries, data, and logs
- Logging utilities that follow best practices
- Ready to extend with your own custom queries and business logic

## Directory Structure

```
nerdgraph-workflow-template/
├── .gitignore                 # Configured to ignore logs, CSV files, etc.
├── LICENSE                    # Apache 2.0 license
├── README.md                  # This file
└── nerdgraph/                 # Main package
    ├── __init__.py            # Package initialization
    ├── main.py                # Entry point for your workflow
    ├── data/                  # Directory for data files
    │   ├── input/             # Place input data files here
    │   └── output/            # Output data will be stored here
    ├── logs/                  # Log files will be stored here
    ├── queries/               # Store your GraphQL queries here
    │   └── __init__.py        # Package initialization
    └── utils/                 # Utility functions and classes
        ├── __init__.py        # Exports utilities
        ├── logger.py          # Logging configuration utility
        └── nerdgraph_client.py # NerdGraph API client
```

## Prerequisites

- Python 3.6+
- New Relic account with an API key

## Setup

1. Clone this repository or use it as a template for your own project

```bash
git clone https://github.com/yourusername/nerdgraph-workflow-template.git
cd nerdgraph-workflow-template
```

2. Set up a Python virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies

```bash
pip install requests
```

4. Set your New Relic API key as an environment variable

```bash
export NEW_RELIC_API_KEY='your-api-key-here'
```

On Windows:
```bash
set NEW_RELIC_API_KEY=your-api-key-here
```

## Usage

1. Define your GraphQL queries in the `nerdgraph/queries/` directory
2. Implement your workflow logic in `nerdgraph/main.py`
3. Run your workflow:

```bash
python -m nerdgraph.main
```

## Example

Here's a simple example of how to use the NerdGraph client to execute a query:

```python
from nerdgraph.utils import NerdGraphClient, Logger

# Initialize logger
logger = Logger(__name__).get_logger()

# Initialize NerdGraph client
client = NerdGraphClient()

# Define a GraphQL query
query = """
query {
  actor {
    user {
      name
      email
    }
  }
}
"""

# Execute the query
response = client.execute_query(query)

# Process the response
if response and 'data' in response:
    user = response['data']['actor']['user']
    logger.info(f"Logged in as: {user['name']} ({user['email']})")
else:
    logger.error("Failed to retrieve user information")
```

## Creating Your Own Workflow

1. Create a new file in the `nerdgraph/queries/` directory for your specific GraphQL queries
2. Update `nerdgraph/main.py` with your workflow logic
3. Add any additional helper functions you need to the utils directory
4. Process and store data in the appropriate directories

## Best Practices

- Keep GraphQL queries in separate files in the `queries` directory
- Use the Logger utility for consistent logging
- Store input/output data in the appropriate directories
- Handle API errors gracefully using the built-in retry logic

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.