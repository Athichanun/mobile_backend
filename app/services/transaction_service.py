import os
import json
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from app.repository.transaction_repository import TransactionRepository
from openai import OpenAI
import requests
from fastapi import UploadFile
from datetime import datetime, timedelta

# Set matplotlib to non-interactive mode
plt.switch_backend("Agg")

load_dotenv()
TYPHOON_API_URL = os.getenv("TYPHOON_API_URL")
TYPHOON_API_KEY = os.getenv("TYPHOON_API_KEY")


class TransactionService:
    @staticmethod
    def decision_transaction(account_id: int, prompt: str):
        client = OpenAI(
            api_key=TYPHOON_API_KEY,
            base_url=TYPHOON_API_URL,
        )
        today = datetime.now()
        yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        today = today.strftime("%Y-%m-%d")
        system_prompt = """
You are a finance AI assistant for a mobile app. 
if you didn't know the date, use today's date. if the user said yesterday, use {yesterday}. but if the user said today or, use {today}. 
Database Schema:
- Table `accounts`: id (INT), user_id (INT), account_name (VARCHAR), balance (FLOAT)
- Table `transactions`: id (INT), account_id (INT, FK), name (VARCHAR), transaction_type (VARCHAR: 'income'/'expense'), amount (FLOAT), price (FLOAT), date (DATE)

User context: account_id = {account_id}

Intents:
1. `add_transaction`: User wants to record new transactions from a prompt or receipt. 
   - Extract a list of `items`.
   - For each item, extract: name (specific product name, e.g., "ชาเย็น", "ข้าวมันไก่", NOT shop name), amount, price, type (income/expense), date.
2. `query`: User asks a question about their data.
   - Generate a valid PostgreSQL `SELECT` query. 
   - ALWAYS filter by `account_id = {account_id}`.
   - Set `visualize` to `true` ONLY if the user explicitly asks for a graph , กราฟ , chart, or visual summary (e.g., "draw a bar chart", "show a pie graph"). Otherwise, ALWAYS set it to `false`.
   - If `visualize` is true, specify `graph_type`.

Return JSON only:
{{
  "intent": "add_transaction" | "query",
  "items": [
    {{
      "name": "specific product name",
      "amount": ...,
      "price": ...,
      "type": "income" | "expense",
      "date": "YYYY-MM-DD"
    }}
  ],
  "sql": "SELECT ...",
  "visualize": true | false,
  "graph_type": "bar" | "pie" | "line"
}}
        """.format(account_id=account_id, yesterday=yesterday, today=today)

        response = client.chat.completions.create(
            model="typhoon-v2.5-30b-a3b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=4096,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        print(f"LLM Response: {content}")

        # Strip markdown code blocks if present
        if content.startswith("```json"):
            content = content.replace("```json", "", 1).rsplit("```", 1)[0].strip()
        elif content.startswith("```"):
            content = content.replace("```", "", 1).rsplit("```", 1)[0].strip()

        try:
            result = json.loads(content)
        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse LLM response: {e}",
                "raw_content": content,
            }

        intent = result.get("intent")
        print(f"Intent: {intent}")

        if intent == "add_transaction":
            items = result.get("items", [])
            if (
                not items and "name" in result
            ):  # Fallback for old LLM behavior or single item
                items = [result]

            created_transactions = []
            for item in items:
                transaction_date = item.get("date")
                if not transaction_date:
                    transaction_date = datetime.now().strftime("%Y-%m-%d")

                trans = TransactionRepository.create_transaction(
                    account_id=account_id,
                    name=item.get("name"),
                    transaction_type=item.get("type"),
                    amount=item.get("amount"),
                    price=item.get("price"),
                    date=transaction_date,
                )
                created_transactions.append(trans)

            return {
                "type": "add_transaction_result",
                "count": len(created_transactions),
                "items": created_transactions,
            }
        elif intent == "query":
            sql_query = result.get("sql")
            data = TransactionRepository.execute_read_query(sql_query)

            image_url = None
            if result.get("visualize") and data:
                image_url = TransactionService._generate_graph(
                    data, result.get("graph_type"), account_id
                )
            ai_answer = TransactionService.analysis_transaction(prompt, data)
            return {
                "type": "query_result",
                "data": data,
                "visualize": result.get("visualize", False),
                "graph_type": result.get("graph_type"),
                "image_url": image_url,
                "sql": sql_query,  # For debugging
                "ai_answer": ai_answer,
            }
        else:
            return {"error": "Invalid intent"}

    @staticmethod
    def analysis_transaction(prompt: str, data: str):
        client = OpenAI(
            api_key=TYPHOON_API_KEY,
            base_url=TYPHOON_API_URL,
        )
        system_prompt = """
        You are a finance AI assistant
        คุณจะวิเคราะห์ข้อมูลที่ได้มาจาก user และ ตอบเหมือนผู้เชี่ยวชาญด้านการเงิน
        USER INPUT: {prompt}
        DATA ที่ได้จาก ฐานข้อมูล: {data}
        RETURN TEXT ONLY
        """.format(prompt=prompt, data=data)

        response = client.chat.completions.create(
            model="typhoon-v2.5-30b-a3b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=4096,
        )
        content = response.choices[0].message.content
        print(f"LLM Response: {content}")
        return content

    @staticmethod
    def _generate_graph(data, graph_type, account_id):
        if not data:
            return None

        # Create static directory if not exists
        static_dir = Path("app/static/graphs")
        static_dir.mkdir(parents=True, exist_ok=True)

        filename = f"graph_{account_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        filepath = static_dir / filename

        plt.figure(figsize=(10, 6))

        # Simple extraction for demo - in production this would be smarter
        # Assuming first column is categorical/date and second is numeric
        keys = list(data[0].keys())
        x_label = keys[0]
        y_label = keys[1] if len(keys) > 1 else keys[0]

        x_data = [str(row[x_label]) for row in data]
        y_data = [float(row[y_label]) for row in data]

        if graph_type == "pie":
            plt.pie(y_data, labels=x_data, autopct="%1.1f%%")
            plt.title(f"{y_label} by {x_label}")
        elif graph_type == "line":
            plt.plot(x_data, y_data, marker="o")
            plt.xticks(rotation=45)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(f"{y_label} over {x_label}")
        else:  # Default to bar
            plt.bar(x_data, y_data)
            plt.xticks(rotation=45)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(f"{y_label} by {x_label}")

        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()

        return f"/static/graphs/{filename}"

    @staticmethod
    def ocr_transaction(account_id: int, file: UploadFile):
        url = "https://api.opentyphoon.ai/v1/ocr"

        try:
            # Read file content
            file_content = file.file.read()

            files = {"file": (file.filename, file_content, file.content_type)}
            data = {
                "model": "typhoon-ocr",
                "task_type": "default",
                "max_tokens": "16384",
                "temperature": "0.1",
                "top_p": "0.6",
                "repetition_penalty": "1.2",
            }

            headers = {"Authorization": f"Bearer {TYPHOON_API_KEY}"}

            response = requests.post(url, files=files, data=data, headers=headers)

            if response.status_code == 200:
                result = response.json()
                extracted_texts = []
                for page_result in result.get("results", []):
                    if page_result.get("success") and page_result.get("message"):
                        content = page_result["message"]["choices"][0]["message"][
                            "content"
                        ]
                        try:
                            # Try to parse as JSON if it's structured output
                            parsed_content = json.loads(content)
                            text = parsed_content.get("natural_text", content)
                        except json.JSONDecodeError:
                            text = content
                        extracted_texts.append(text)
                    elif not page_result.get("success"):
                        print(
                            f"Error processing {page_result.get('filename', 'unknown')}: {page_result.get('error', 'Unknown error')}"
                        )

                full_text = "\n".join(extracted_texts)
                print(f"OCR Extracted Text: {full_text}")

                if not full_text:
                    return {"error": "OCR did not extract any text from the document."}

                # Now call decision_transaction with the extracted text as a prompt
                return TransactionService.decision_transaction(account_id, full_text)
            else:
                return {
                    "error": f"OCR API call failed with status {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {"error": f"An error occurred during OCR: {str(e)}"}

    @staticmethod
    def get_transactions_by_account_id(account_id: int):
        return TransactionRepository.get_transactions_by_account_id(account_id)

    @staticmethod
    def get_all_transaction_by_user_id(user_id: int):
        return TransactionRepository.get_all_transaction_by_user_id(user_id)
