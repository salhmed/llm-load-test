"""Plugin for the WatsonX.ai remote endpoints."""

import json
import logging
import time
import requests
import urllib3

from llm_load_test.plugins import plugin
from llm_load_test.result import RequestResult

# Disable warnings for unverified HTTPS requests
urllib3.disable_warnings()

logger = logging.getLogger("user")

required_args = ["host", "model_id", "project_id"]

class WatsonXPlugin(plugin.Plugin):
    """Plugin for the WatsonX endpoint."""

    def __init__(self, args):
        """Initialize the plugin."""
        self._parse_args(args)

    def _parse_args(self, args):
        for arg in required_args:
            if arg not in args:
                logger.error("Missing plugin arg: %s", arg)

        self.host = args["host"]
        # Standard streaming endpoint for watsonx text generation
        if not self.host.endswith("generation_stream"):
            if not self.host.endswith("/"):
                self.host += "/"
            self.host += "ml/v1/text/generation_stream?version=2023-05-29"

        self.model_id = args["model_id"]
        self.project_id = args["project_id"]
        self.authorization = args.get("authorization", "")
        self.verify_ssl = args.get("use_tls", False)

    def streaming_request_http(self, query, user_id, test_end_time: float = 0):
        """Make a streaming HTTP request to WatsonX."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        if self.authorization:
            headers["Authorization"] = f"Bearer {self.authorization}"

        data = {
            "input": query["text"],
            "model_id": self.model_id,
            "project_id": self.project_id,
            "parameters": {
                "max_new_tokens": query.get("output_tokens", 100),
                "decoding_method": "greedy"
            }
        }

        result = RequestResult(user_id, query.get("input_id"), query.get("input_tokens"))

        tokens = []
        response = None
        result.start_time = time.time()
        try:
            response = requests.post(
                self.host, headers=headers, json=data, verify=self.verify_ssl, stream=True
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            result.end_time = time.time()
            result.error_text = repr(err)
            if response is not None:
                result.error_code = response.status_code
            return result
        except requests.exceptions.HTTPError as err:
            result.end_time = time.time()
            result.error_text = repr(err)
            if response is not None:
                result.error_code = response.status_code
            return result

        logger.debug("response: %s", response)
        
        for line in response.iter_lines():
            if not line:
                continue
            
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith("data: "):
                try:
                    message = json.loads(decoded_line[6:])
                    
                    results = message.get("results", [])
                    if results:
                        token = results[0].get("generated_text", "")
                        logger.debug("Token: %s", token)
                        
                        # First chunk is not a token, just an acknowledgement of connection
                        if not result.ack_time:
                            result.ack_time = time.time()

                        # First non-empty chunk is the first token
                        if not result.first_token_time and token != "":
                            result.first_token_time = time.time()
                            
                        tokens.append(token)
                except json.JSONDecodeError:
                    logger.error("Response line could not be json decoded: %s", decoded_line)
                    continue

        # Response received, return
        result.end_time = time.time()
        result.output_text = "".join(tokens)
        result.output_tokens = len(tokens)

        # TODO: Calculate correct output tokens before test timeout duration for streaming requests
        result.output_tokens_before_timeout = result.output_tokens

        result.calculate_results()
        return result
