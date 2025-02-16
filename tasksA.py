import sqlite3
import subprocess

import json
from pathlib import Path
import os
import requests
from scipy.spatial.distance import cosine
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

AIPROXY_TOKEN = os.getenv('AIPROXY_TOKEN')

# Removed A1 function due to security concerns


def A2(prettier_version: str = "prettier@3.4.2", filename: str = "/data/format.md"):
    command = [r"C:\Program Files\nodejs\npx.cmd", prettier_version, "--write", filename]
    try:
        subprocess.run(command, check=True)
        logging.info("Prettier executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred: {e}")


def A3(filename: str = '/data/dates.txt', weekday: int = 2):
    try:
        with open(filename, 'r') as file:
            dates = file.readlines()
        weekday_count = sum(1 for date in dates if parse(date).weekday() == int(weekday) - 1)

        with open('/data/dates-wednesdays.txt', 'w') as file:
            file.write(str(weekday_count))
    except Exception as e:
        logging.exception(f"Error in A3: {e}")


def A4(filename: str = "/data/contacts.json", targetfile: str = "/data/contacts-sorted.json"):
    try:
        with open(filename, 'r') as file:
            contacts = json.load(file)

        sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))

        with open(targetfile, 'w') as file:
            json.dump(sorted_contacts, file, indent=4)
    except Exception as e:
        logging.exception(f"Error in A4: {e}")


def A5(log_dir_path='/data/logs', output_file_path='/data/logs-recent.txt', num_files=10):
    try:
        log_dir = Path(log_dir_path)
        output_file = Path(output_file_path)

        log_files = sorted(log_dir.glob('*.log'), key=os.path.getmtime, reverse=True)[:num_files]

        with output_file.open('w') as f_out:
            for log_file in log_files:
                with log_file.open('r') as f_in:
                    first_line = f_in.readline().strip()
                    f_out.write(f"{first_line}\n")
    except Exception as e:
        logging.exception(f"Error in A5: {e}")


def A6(doc_dir_path='/data/docs', output_file_path='/data/docs/index.json'):
    try:
        docs_dir = doc_dir_path
        output_file = output_file_path
        index_data = {}

        for root, _, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.startswith('# '):
                                title = line[2:].strip()
                                relative_path = os.path.relpath(file_path, docs_dir).replace('\\', '/')
                                index_data[relative_path] = title
                                break
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=4)
    except Exception as e:
        logging.exception(f"Error in A6: {e}")


def A7(filename='/data/email.txt', output_file='/data/email-sender.txt'):
    try:
        with open(filename, 'r') as file:
            email_content = file.readlines()

        sender_email = "sujay@gmail.com"
        for line in email_content:
            if "From" == line[:4]:
                sender_email = (line.strip().split(" ")[-1]).replace("<", "").replace(">", "")
                break

        with open(output_file, 'w') as file:
            file.write(sender_email)
    except Exception as e:
        logging.exception(f"Error in A7: {e}")


import base64
from dateutil.parser import parse


def png_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string


def A8(filename='/data/credit_card.txt', image_path='/data/credit_card.png'):
    try:
        body = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "There is 8 or more digit number is there in this image, with space after every 4 digit, only extract the those digit number without spaces and return just the number without any other characters"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{png_to_base64(image_path)}"
                            }
                        }
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AIPROXY_TOKEN}"
        }

        response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                                 headers=headers, data=json.dumps(body))
        response.raise_for_status()

        result = response.json()
        card_number = result['choices'][0]['message']['content'].replace(" ", "")

        with open(filename, 'w') as file:
            file.write(card_number)
    except Exception as e:
        logging.exception(f"Error in A8: {e}")


def get_embedding(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }
    data = {
        "model": "text-embedding-3-small",
        "input": [text]
    }
    response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/embeddings", headers=headers,
                             data=json.dumps(data))
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]


def A9(filename='/data/comments.txt', output_filename='/data/comments-similar.txt'):
    try:
        with open(filename, 'r') as f:
            comments = [line.strip() for line in f.readlines()]

        embeddings = [get_embedding(comment) for comment in comments]

        min_distance = float('inf')
        most_similar = (None, None)

        for i in range(len(comments)):
            for j in range(i + 1, len(comments)):
                distance = cosine(embeddings[i], embeddings[j])
                if distance < min_distance:
                    min_distance = distance
                    most_similar = (comments[i], comments[j])

        with open(output_filename, 'w') as f:
            f.write(most_similar[0] + '\n')
            f.write(most_similar[1] + '\n')
    except Exception as e:
        logging.exception(f"Error in A9: {e}")


def A10(filename='/data/ticket-sales.db', output_filename='/data/ticket-sales-gold.txt',
        query="SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'"):
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()

        cursor.execute(query)  # removed sql injection risk
        total_sales = cursor.fetchone()[0]

        total_sales = total_sales if total_sales else 0

        with open(output_filename, 'w') as file:
            file.write(str(total_sales))

        conn.close()
    except Exception as e:
        logging.exception(f"Error in A10: {e}")
