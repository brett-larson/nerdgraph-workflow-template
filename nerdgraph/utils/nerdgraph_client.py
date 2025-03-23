import os
import time
import requests
from nerdgraph.utils import Logger
from typing import Optional, Dict, Any

# Create logger for the module
logger = Logger(__name__).get_logger()

class NerdGraphClient:
    def __init__(self):
        self.api_key = self.get_api_key()
        if not self.api_key:
            logger.error("Missing API key")
            raise ValueError("Missing API key")
        self.headers = {
            "Content-Type": "application/json",
            "API-Key": self.api_key
        }
        logger.info("NerdGraphClient initialized with API key")

    @staticmethod
    def get_api_key() -> Optional[str]:
        """
        Load New Relic API key from local environment variables
        :return: API key
        """
        api_key = os.getenv('NEW_RELIC_API_KEY')
        if api_key:
            logger.debug("API key loaded from environment variables")
        else:
            logger.warning("API key not found in environment variables")
        return api_key

    def execute_query(self, query: str, variables: Dict = None, max_retries: int = 3, backoff_factor: int = 2) -> Any:
        """
        Execute a single GraphQL query with retry logic. If the query fails, retry up to max_retries times.
        :param query: GraphQL query string.
        :param variables: Query variables. Default is an empty dictionary.
        :param max_retries: Maximum number of retries. Default is 3.
        :param backoff_factor: Factor to increase sleep time between retries. Default is 2.

        :return: Query response or None if query fails.
        """
        if variables is None:
            variables = {}

        payload = {
            "query": query,
            "variables": variables
        }

        for attempt in range(max_retries):
            try:
                logger.info(f"Sending GraphQL request, attempt {attempt + 1}")
                response = requests.post(
                    "https://api.newrelic.com/graphql",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                if 'errors' in data:
                    error = data['errors'][0]
                    if error['extensions']['errorClass'] == 'TIMEOUT':
                        logger.warning(f"Timeout error: {error['message']}, retrying...")
                        time.sleep(backoff_factor ** attempt)
                        continue
                    else:
                        logger.error(f"GraphQL error: {error['message']}")
                        return None
                logger.debug("GraphQL request successful")
                return data
            except requests.exceptions.RequestException as e:
                logger.error(f"Query failed to run: {e}, retrying...")
                time.sleep(backoff_factor ** attempt)
        logger.critical("Max retries exceeded for GraphQL query")
        raise Exception("Max retries exceeded for GraphQL query")