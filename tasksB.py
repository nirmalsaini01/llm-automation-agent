import requests
import sqlite3
import duckdb
import markdown
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def B3(url: str, save_path: str) -> None:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        with open(save_path, 'w') as file:
            file.write(response.text)
        logging.info(f"Downloaded {url} to {save_path}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading {url}: {e}")
    except Exception as e:
        logging.exception(f"Error in B3: {e}")


def B5(db_path, query, output_filename):
    try:
        conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        conn.close()
        with open(output_filename, 'w') as file:
            file.write(str(result))
        logging.info(f"Executed query on {db_path}, result saved to {output_filename}")
        return result
    except Exception as e:
        logging.exception(f"Error in B5: {e}")
        return None


def B6(url, output_filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        result = response.text
        with open(output_filename, 'w') as file:
            file.write(str(result))
        logging.info(f"Fetched {url}, content saved to {output_filename}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
    except Exception as e:
        logging.exception(f"Error in B6: {e}")


from PIL import Image


def B7(image_path, output_path, resize=None):
    try:
        img = Image.open(image_path)
        if resize:
            img = img.resize((resize[0], resize[1]))  # Ensure resize is a tuple
        img.save(output_path)
        logging.info(f"Processed {image_path}, saved to {output_path}")
    except FileNotFoundError:
        logging.error(f"File not found: {image_path}")
    except Exception as e:
        logging.exception(f"Error in B7: {e}")


def B9(md_path, output_path):
    try:
        with open(md_path, 'r') as file:
            html = markdown.markdown(file.read())
        with open(output_path, 'w') as file:
            file.write(html)
        logging.info(f"Converted {md_path} to HTML, saved to {output_path}")
    except FileNotFoundError:
        logging.error(f"File not found: {md_path}")
    except Exception as e:
        logging.exception(f"Error in B9: {e}")
