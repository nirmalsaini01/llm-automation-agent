from fastapi import FastAPI, HTTPException, Query  # noqa: F401
from fastapi.responses import PlainTextResponse  # noqa: F401
from fastapi.middleware.cors import CORSMiddleware  # noqa: F401
from tasksA import *  # noqa: F401, F403
from tasksB import *  # noqa: F401, F403
from dotenv import load_dotenv  # noqa: F401
import os  # noqa: F401
import httpx  # noqa: F401
import json   # type: ignore
import logging  # noqa: F401

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

load_dotenv()

openai_api_chat = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"  # for testing
openai_api_key = os.getenv("AIPROXY_TOKEN")

if not openai_api_key:
    logging.error("AIPROXY_TOKEN not set in environment variables.")
    raise ValueError("AIPROXY_TOKEN not set in environment variables.")

headers = {
    "Authorization": f"Bearer {openai_api_key}",
    "Content-Type": "application/json",
}

from typing import Dict, List, Union, Callable, Any  # type: ignore # noqa: F401

function_definitions_llm: List[Dict[str, Union[str, Dict[str, Union[str, Dict[str, Union[str, int, List[int]]]]]]]] = [
    {
        "name": "A2",
        "description": "Format a markdown file using a specified version of Prettier.",
        "parameters": {
            "type": "object",
            "properties": {
                "prettier_version": {"type": "string", "description": "Prettier version"},
                "filename": {"type": "string", "description": "Path to the markdown file"}
            },
            "required": ["prettier_version", "filename"]
        }
    },
    {
        "name": "A3",
        "description": "Count the number of occurrences of a specific weekday in a date file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Path to the date file"},
                "weekday": {"type": "integer", "description": "Weekday as an integer (1-7, Monday-Sunday)"}
            },
            "required": ["filename", "weekday"]
        }
    },
    {
        "name": "A4",
        "description": "Sort a JSON contacts file and save the sorted version to a target file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Path to the JSON contacts file"},
                "targetfile": {"type": "string", "description": "Path to save the sorted JSON"}
            },
            "required": ["filename", "targetfile"]
        }
    },
    {
        "name": "A5",
        "description": "Retrieve the most recent log files from a directory and save their content to an output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "log_dir_path": {"type": "string", "description": "Path to the log directory"},
                "output_file_path": {"type": "string", "description": "Path to save the recent logs"},
                "num_files": {"type": "integer", "description": "Number of log files to retrieve"}
            },
            "required": ["log_dir_path", "output_file_path", "num_files"]
        }
    },
    {
        "name": "A6",
        "description": "Generate an index of documents from a directory and save it as a JSON file.",
        "parameters": {
            "type": "object",
            "properties": {
                "doc_dir_path": {"type": "string", "description": "Path to the document directory"},
                "output_file_path": {"type": "string", "description": "Path to save the document index"}
            },
            "required": ["doc_dir_path", "output_file_path"]
        }
    },
    {
        "name": "A7",
        "description": "Extract the sender's email address from a text file and save it to an output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Path to the email file"},
                "output_file": {"type": "string", "description": "Path to save the sender's email"}
            },
            "required": ["filename", "output_file"]
        }
    },
    {
        "name": "A8",
        "description": "Generate an image representation of credit card details from a text file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Path to the credit card details file"},
                "image_path": {"type": "string", "description": "Path to save the generated image"}
            },
            "required": ["filename", "image_path"]
        }
    },
    {
        "name": "A9",
        "description": "Find similar comments from a text file and save them to an output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Path to the comments file"},
                "output_filename": {"type": "string", "description": "Path to save the similar comments"}
            },
            "required": ["filename", "output_filename"]
        }
    },
    {
        "name": "A10",
        "description": "Identify high-value (gold) ticket sales from a database and save them to a text file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Path to the database file"},
                "output_filename": {"type": "string", "description": "Path to save the gold ticket sales"},
                "query": {"type": "string", "description": "SQL query to retrieve gold ticket sales"}
            },
            "required": ["filename", "output_filename", "query"]
        }
    },
    {
        "name": "B3",
        "description": "Download content from a URL and save it to the specified path.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to download content from"},
                "save_path": {"type": "string", "description": "Path to save the downloaded content"}
            },
            "required": ["url", "save_path"]
        }
    },
    {
        "name": "B5",
        "description": "Execute a SQL query on a specified database file and save the result to an output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "db_path": {"type": "string", "description": "Path to the SQLite database file"},
                "query": {"type": "string", "description": "SQL query to be executed"},
                "output_filename": {"type": "string", "description": "Path to save the query result"}
            },
            "required": ["db_path", "query", "output_filename"]
        }
    },
    {
        "name": "B6",
        "description": "Fetch content from a URL and save it to the specified output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to fetch content from"},
                "output_filename": {"type": "string", "description": "Path to save the fetched content"}
            },
            "required": ["url", "output_filename"]
        }
    },
    {
        "name": "B7",
        "description": "Process an image by optionally resizing it and saving the result to an output path.",
        "parameters": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string", "description": "Path to the input image file"},
                "output_path": {"type": "string", "description": "Path to save the processed image"},
                "resize": {
                    "type": "array",
                    "items": {"type": "integer", "minimum": 1},
                    "minItems": 2,
                    "maxItems": 2,
                    "description": "Optional. Resize dimensions as [width, height]"
                }
            },
            "required": ["image_path", "output_path"]
        }
    },
    {
        "name": "B9",
        "description": "Convert a Markdown file to another format and save the result to the specified output path.",
        "parameters": {
            "type": "object",
            "properties": {
                "md_path": {"type": "string", "description": "Path to the Markdown file to be converted"},
                "output_path": {"type": "string", "description": "Path where the converted file will be saved"}
            },
            "required": ["md_path", "output_path"]
        }
    }

] # type: ignore

def get_completions(prompt: str):
    try:
        with httpx.Client(timeout=20) as client:
            response = client.post(
                f"{openai_api_chat}",
                headers=headers,
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system",
                         "content": "You are a function classifier that extracts structured parameters from queries."},
                        {"role": "user", "content": prompt}
                    ],
                    "tools": [
                        {
                            "type": "function",
                            "function": function
                        } for function in function_definitions_llm
                    ],
                    "tool_choice": "auto"
                }, # type: ignore
            )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        logging.debug(f"get_completions response: {response.json()}")  # Log the full response
        tool_calls = response.json()["choices"][0]["message"].get("tool_calls")
        if tool_calls:
            function_call = tool_calls[0]["function"]
            logging.info(f"Function call: {function_call}")
            return function_call
        else:
            logging.warning("No tool calls in the response.")
            return None  # Or handle the case where no function is called
    except httpx.HTTPError as e:
        logging.error(f"HTTP error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logging.exception("An unexpected error occurred in get_completions")
        raise HTTPException(status_code=500, detail=str(e))


# Placeholder for task execution
@app.post("/run")
async def run_task(task: str):
    try:
        response = get_completions(task)
        if response is None:
            raise HTTPException(status_code=400, detail="No function call was generated")

        task_code = response['name']
        arguments = response['arguments']
        # Sanitize arguments

        # Instead of multiple if statements, use a dictionary to map task_code to functions
        task_mapping: Dict[str, Callable[..., Any]] = {
            "A2": A2,
            "A3": A3,
            "A4": A4,
            "A5": A5,
            "A6": A6,
            "A7": A7,
            "A8": A8,
            "A9": A9,
            "A10": A10,
            "B3": B3,
            "B5": B5,
            "B6": B6,
            "B7": B7,
            "B9": B9,
        }
        if task_code in task_mapping:
            # Execute the task using the mapped function
            # Assuming all functions accept keyword arguments
            task_function = task_mapping[task_code]
            task_function(**arguments)

            return {"message": f"{task_code} Task '{task}' executed successfully"}
        else:
            raise HTTPException(status_code=400, detail=f"Invalid task code: {task_code}")

    except HTTPException as http_exc:
        # Re-raise HTTPExceptions to preserve status code
        raise http_exc
    except Exception as e:
        logging.exception(f"Error executing task {task}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


# Placeholder for file reading
@app.get("/read", response_class=PlainTextResponse)
async def read_file(path: str = Query(..., description="File path to read")):
    try:
        # path = sanitize_path(path) # Sanitize path
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logging.exception(f"Error reading file {path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)