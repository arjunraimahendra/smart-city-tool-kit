##################################
### Import Packages
##################################
import os
import json
import logging
import requests
import openai

from logging.handlers import RotatingFileHandler
from functools import wraps
from bs4 import BeautifulSoup


from tenacity import (
    retry, 
    stop_after_attempt, 
    wait_exponential, 
    retry_if_exception_type,
    before_sleep_log,
    after_log
)
from typing import Optional, Dict, Any, Tuple, List
from requests.exceptions import ConnectionError, Timeout, RequestException


from selenium.common.exceptions import WebDriverException 
from pathlib import Path
from llama_parse import LlamaParse
from urllib.parse import urlparse, unquote
from urllib3.exceptions import ReadTimeoutError


from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

import nest_asyncio
nest_asyncio.apply()

from prompts import ppp_framework_prompt, stakeholder_prompt

from dotenv import load_dotenv
load_dotenv()

##################################
### Langchain Model
##################################

# langchain_llm = ChatOpenAI(model="gpt-4o", temperature=0) 

##################################
### Logging Configuration
##################################

# Configure logging
log_file = "app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s",
    handlers=[
        # logging.StreamHandler(),
        RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=10)  # 5MB files
    ]
)
logger = logging.getLogger(__name__)

# Decorator to log function inputs and outputs
def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Log input arguments
        logger.info(f"Calling function: {func.__name__}, args: {args}, kwargs: {kwargs}")
        try:
            # Call the function
            result = func(*args, **kwargs)
            # Log the result
            logger.info(f"Function {func.__name__} returned: {result}")
            return result
        except Exception as e:
            # Log exceptions
            logger.error(f"Exception in {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper


##################################
### Model Names
##################################

GPT_MODEL = 'gpt-4o'
O1_MODEL = 'o1-mini'

##################################
### Retry decorator for APIs
##################################

my_retry_decorator = retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    retry=retry_if_exception_type(
        (ConnectionError, Timeout, RequestException)
    ),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO),
    reraise=True
)

##################################
### Open AI API call
##################################

@my_retry_decorator
def get_openai_response(model, messages, response_format=None):
    logger.info("function - get_openai_response")
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    logger.info(f"{client}")
    try:
        if response_format:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_schema", "json_schema": response_format}
            )
        else:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")

##################################
### Generate Document
##################################

def generate_document_contents(city: str, 
                               country: str, 
                               policy_levers: str, 
                               stakeholders: str,
                               report_structure: str, 
                               max_num_queries: int=3):
    
    logger.info("function - generate_document_contents")
    
    user_message = ppp_framework_prompt.format(city=city, 
                                               country=country, 
                                               policy_levers=policy_levers, 
                                               stakeholders=stakeholders, 
                                               report_structure=report_structure,
                                               max_num_queries=max_num_queries)


    # Generate question 
    document_contents = get_openai_response(
        model=O1_MODEL,
        messages=[{"role":"user", "content": user_message}]
    )

    return document_contents

##################################
### Generate Document
##################################

def generate_stakeholders(city: str, 
                          country: str):
    

    stakeholders_message = stakeholder_prompt.format(city=city,
                                                     country=country)
    
    # Generate stakeholders 
    stakeholder_contents = get_openai_response(
        model=O1_MODEL,
        messages=[{"role":"user", "content": stakeholders_message}]
    )

    return stakeholder_contents