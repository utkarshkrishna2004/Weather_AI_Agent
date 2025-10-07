import os
import time
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_weather(city: str):
    """
    Fetch current weather from wttr.in API.
    Returns a human-readable string.
    """
    url = f"https://wttr.in/{city}?format=%C+%t"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"The current weather conditions in {city} are: {response.text}"
        else:
            return f"Sorry, could not fetch weather for {city} at the moment."
    except requests.RequestException:
        return f"Network error while fetching weather for {city}."

available_tools = {
    "get_weather": get_weather
}

SYSTEM_PROMPT = """
You are an expert AI assistant capable of solving user queries using a structured agentic workflow: START → PLAN → TOOL → OBSERVE → OUTPUT.

⚠️ IMPORTANT: You MUST ALWAYS return output strictly as a JSON object with the key "step".
Do NOT provide any free text, explanations, or extra output outside of this JSON format.

Workflow rules:
1. Always begin with START (user input), then PLAN your steps, optionally call TOOLs if needed, then OBSERVE results, and finally OUTPUT.
2. PLAN steps can contain reasoning, but TOOL calls must be in proper JSON.
3. Only call tools from the available list if the information cannot be inferred internally.
4. Respect the following JSON format strictly:

{
    "step": "START" | "PLAN" | "TOOL" | "OBSERVE" | "OUTPUT",
    "content": "string",
    "tool": "string",   # optional, required for TOOL steps
    "input": "string"   # optional, required for TOOL steps
}

Available Tools:
- get_weather(city: str): Returns the current weather for the specified city using wttr.in.

Additional Instructions:
- If multiple cities are mentioned, call get_weather separately for each city and compile the results before OUTPUT.
- Do not assume or hallucinate weather conditions — always call the tool.
- After each TOOL call, wait for OBSERVE before moving on to the next.
- Your output must strictly follow the JSON format, nothing else.
"""

message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

while True:
    print("\n" + "---"*30)
    print("⛅ WEATHER AGENT – Ask me about the current weather in any city!")

    user_query = input("\n> ")
    message_history.append({"role": "user", "content": user_query})

    tool_outputs = []  # buffer to collect results from multiple TOOL calls

    while True:
        time.sleep(1)  # prevent API rate limits

        try:
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                response_format={"type": "json_object"},
                messages=message_history
            )
        except Exception as e:
            print(f"⚠️ LLM request failed: {e}")
            break

        raw_result = response.choices[0].message.content.strip()

        try:
            parsed_result = json.loads(raw_result)
        except json.JSONDecodeError:
            parsed_result = {"step": "OUTPUT", "content": raw_result}

        if not isinstance(parsed_result, dict) and not isinstance(parsed_result, list):
            parsed_result = {"step": "OUTPUT", "content": str(parsed_result)}

        message_history.append({"role": "assistant", "content": raw_result})

        # Handle list of TOOL calls or single TOOL
        tool_steps = []
        if isinstance(parsed_result, list):
            tool_steps = parsed_result
        elif parsed_result.get("step") == "TOOL":
            tool_steps = [parsed_result]

        for tool_step in tool_steps:
            tool_name = tool_step.get("tool")
            tool_input = tool_step.get("input")
            print(f"🔮 {tool_name}({tool_input})")

            if tool_name in available_tools:
                tool_output = available_tools[tool_name](tool_input)
                print(f"🔮 {tool_name}({tool_input}) = {tool_output}")

                tool_outputs.append(tool_output)

                observe_step = {
                    "step": "OBSERVE",
                    "tool": tool_name,
                    "input": tool_input,
                    "output": tool_output
                }
                message_history.append({"role": "developer", "content": json.dumps(observe_step)})
            else:
                print(f"⚠️ Tool {tool_name} not found.")

        # Determine LLM step
        step = parsed_result.get("step") if isinstance(parsed_result, dict) else None

        # Ignore OBSERVE steps
        if step == "OBSERVE":
            continue

        elif step == "START":
            print(f"🔥 {parsed_result.get('content')}")
            continue

        elif step == "PLAN":
            print(f"🧠 {parsed_result.get('content')}")
            continue

        elif step == "TOOL":
            # Already handled above
            continue

        elif step == "OUTPUT":
            if tool_outputs:
                combined_result = "\n".join(tool_outputs)
                print(f"🤖 {combined_result}")
                tool_outputs = []
            else:
                print(f"🤖 {parsed_result.get('content')}")
            break

        elif tool_steps:
            # Wait for next LLM response
            continue

        else:
            # fallback
            if tool_outputs:
                combined_result = "\n".join(tool_outputs)
                print(f"🤖 {combined_result}")
                tool_outputs = []
            else:
                print(f"🤖 {parsed_result.get('content', raw_result)}")
            break

    print("---"*30)
