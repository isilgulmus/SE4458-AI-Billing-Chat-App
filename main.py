from fastapi import FastAPI, WebSocket
from ask_openai import ask_openai, build_prompt  # OpenAI modülünü kullanıyoruz
from api_gateway import call_api
import json
from firestore_logger import log_message
import os

app = FastAPI()

def format_api_response(intent: str, raw_text: str, params: dict) -> str:
    month = params.get("month")
    year = params.get("year")

    if intent == "query_detailed_bill":
        lines = raw_text.lower().split("\n")
        phone_minutes = internet_mb = total = "unknown"
        status = "unknown"

        for line in lines:
            try:
                if "phone usage" in line:
                    phone_minutes = line.split(":", 1)[1].split("minutes")[0].strip()
                elif "internet usage" in line:
                    internet_mb = line.split(":", 1)[1].split("mb")[0].strip()
                elif "total amount" in line and "paid status" in line:
                    parts = line.split(",")
                    for part in parts:
                        part = part.strip().lower()
                        if "total amount" in part:
                            total = part.split(":")[1].strip().replace("usd", "").strip()
                        elif "paid status" in part:
                            status_val = part.split(":")[1].strip().lower()
                            if "unpaid" in status_val:
                                status = "unpaid"
                            elif "paid" in status_val and "unpaid" not in status_val:
                                status = "paid"
            except IndexError:
                continue

        message = f"For {month}/{year}, you used {phone_minutes} minutes of phone and {internet_mb} MB of internet.\n"
        message += f"Your total bill is ${total}. "

        if status == "paid":
            message += "And it's already paid. ✅"
        elif status == "unpaid":
            message += "It hasn't been paid yet. ❌"
        else:
            message += "Payment status unknown."

        print("DEBUG > FINAL message:\n", message)
        return message

    elif intent == "query_bill":
        try:
            if "total bill" in raw_text.lower():
                parts = raw_text.lower().split(",")
                amount = parts[0].split(":")[1].strip().replace("usd", "").strip()
                status = parts[1].split(":")[1].strip().capitalize()
                return f"Your bill for {month}/{year} is ${amount}. " + ("It's paid. ✅" if status == "Paid" else "It's unpaid. ❌")
        except IndexError:
            pass
        return raw_text

    elif intent == "make_payment":
        return "I've successfully paid your bill. ✅" if "success" in raw_text.lower() else "Payment failed. ❌ Please try again."

    elif intent == "add_usage":
        usage_type = params.get("usageType", "usage")
        amount = params.get("amount", 0)
        unit = "minutes" if usage_type == "phone" else "GB"
        return f"I've added {amount} {unit} of {usage_type} usage for {month}/{year}. ✅"

    return raw_text

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("How can I help you?")
    #log_message("session-1", "agent", "How can I help you?")

    while True:
        try:
            try:
                user_message = await websocket.receive_text()
                #log_message("session-1", "user", user_message)
            except Exception as e:
                print("🔌 WebSocket closed by client:", e)
                break

            print("🟡 Message received:", user_message)
            prompt = build_prompt(user_message)
            print("🟡 Prompt for LLM:\n", prompt)

            try:
                llm_response = ask_openai(prompt).strip()  # OpenAI API çağrısı
            except Exception as e:
                print("❌ LLM error:", e)
                await websocket.send_text("❌ AI is not responding. Try again later.")
                break

            print("🟢 LLM response:\n", llm_response)

            try:
                data = json.loads(llm_response)
            except json.JSONDecodeError:
                await websocket.send_text("⚠️ AI response was not valid JSON.")
                break

            if data.get("intent") == "missing_info":
                missing = data.get("missing", [])
                await websocket.send_text(f"🛑 I need more information: {', '.join(missing)}")
                continue

            if "actions" not in data and "intent" in data:
                parameters = data["parameters"] if "parameters" in data else {k: v for k, v in data.items() if k != "intent"}
                data = {
                    "actions": [{
                        "intent": data["intent"],
                        "parameters": parameters
                    }]
                }

            if "actions" in data:
                for action in data["actions"]:
                    intent = action["intent"]
                    params = action["parameters"]

                    if intent == "query_detailed_bill":
                        params.setdefault("pageNumber", 1)
                        params.setdefault("pageSize", 50)

                    if intent == "make_payment" and "pay" not in user_message.lower():
                        await websocket.send_text("⚠️ You didn't ask to pay. Skipping payment.")
                        continue

                    print(f"[API LOG] Intent: {intent} → Params: {params}")
                    result = call_api(intent, params)
                    print(f"[API RAW RESULT]:\n{result}")
                    formatted = format_api_response(intent, result, params)
                    await websocket.send_text(formatted)
                    #log_message("session-1", "agent", formatted)


            else:
                await websocket.send_text("⚠️ Sorry, I couldn't understand your request.")

        except Exception as e:
            print("🔥 Fatal error:", e)
            try:
                await websocket.send_text(f"❌ Internal error: {str(e)}")
            except:
                print("⚠️ Could not send error message.")
            break
