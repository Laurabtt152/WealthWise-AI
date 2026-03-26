from google import genai
from google.genai import types
import re
import json

def generate_quiz(demographics, language="en"):
    prompt = (
        f"Make me a financial literacy quiz in '{language}' for someone with the following demographics:\n"
        f"- Country: {demographics['Country']}\n"
        f"- Age: {demographics['Age Range']}\n"
        f"- Education: {demographics['Education']}\n"
        f"- Employment Status: {demographics['Employment Status']}\n"
        f"- Estimated Annual Income: {demographics['Estimated Income']}\n\n"
        f"For each of the following sections, generate 3 yes/no questions in the language selected. Yes or no should also be translated to that language. "
        f"Format the output so that each section starts with its name as a header, followed by the 3 questions. "
        f"Each question should be answerable with Yes or No. "
        f"The format should be as follows:\n"
        f"## Budgeting and Saving\n"
        f"1. [Question text]\n"
        f"2. [Question text]\n"
        f"3. [Question text]\n"
        f"## Taxes\n"
        f"...\n"
        f"## Investing\n"
        f"...\n"
        f"## Debt Management\n"
        f"...\n"
        f"Do not provide answers, only the questions. "
        f"Questions should be suitable for radio button selection (Yes/No) in a web form."
    )

    client = genai.Client(
        vertexai=True,
        project="hack-team-off-the-ledger",
        location="global",
    )

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

    config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=4096,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
        ],
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )

    output = ""
    for chunk in client.models.generate_content_stream(model="gemini-2.5-flash-lite", contents=contents, config=config):
        output += chunk.text
    return output



def generate_roadmap(demographics, quiz_responses, language="en"):
    demo_lines = "\n".join([f"- {key}: {value}" for key, value in demographics.items()])
    quiz_lines = "\n".join([f"- {section}: {response}" for section, response in quiz_responses.items()])

    prompt = (
        f"A user has the following demographics:\n"
        f"{demo_lines}\n\n"
        f"And they answered the following in a financial literacy quiz:\n"
        f"{quiz_lines}\n\n"
        f"Based on this information, create a beginner-friendly financial literacy roadmap in '{language}' "
        f"focusing on their weakest areas.\n\n"
        f"The roadmap must include these four sections: Budgeting, Taxes, Investing, and Debt Management.\n"
        f"For each section, include 2 steps. Each step must have:\n"
        f"- Label: (short title)\n"
        f"- Summary: (1–2 sentence explanation)\n"
        f"- Resources: (1–2 external resources in Markdown link format like [title](url))"
        f"Follow the above response format exactly"
    )

    client = genai.Client(
        vertexai=True,
        project="hack-team-off-the-ledger",
        location="global",
    )

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

    config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=4096,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
        ],
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )

    output = ""
    for chunk in client.models.generate_content_stream(model="gemini-2.5-flash-lite", contents=contents, config=config):
        output += chunk.text

    print("\n=== RAW OUTPUT ===\n")
    print(output)

    roadmap = {
        "Budgeting": {"subtitle": "Budgeting & Emergency Fund", "topics": []},
        "Taxes": {"subtitle": "Tax Filing & Optimization", "topics": []},
        "Investing": {"subtitle": "Stocks, Bonds & Portfolio Building", "topics": []},
        "Debt Management": {"subtitle": "Loans & Repayment Strategies", "topics": []},
    }

    # Extract each section
    section_pattern = r"###\s*(Budgeting|Taxes|Investing|Debt Management)[^\n]*\n+(.*?)(?=\n###|\Z)"
    sections = re.findall(section_pattern, output, re.DOTALL | re.IGNORECASE)

    for section, content in sections:
        section = section.strip().title()

        # Split by label — don't use step numbers
        step_chunks = re.split(r"\*\*\s*Label:\s*\*\*", content)[1:]  # drop preamble

        for chunk in step_chunks:
            lines = chunk.strip().splitlines()
            if not lines:
                continue

            label = lines[0].strip()
            summary = ""
            resources = []

            for line in lines[1:]:
                if "**Summary:**" in line:
                    summary = line.split("**Summary:**", 1)[-1].strip()
                elif "[" in line and "](" in line:
                    matches = re.findall(r"\[(.*?)\]\((https?://[^\s)]+)\)", line)
                    resources.extend(matches)

            roadmap[section]["topics"].append({
                "label": label,
                "summary": summary if summary else "No summary provided.",
                "resources": resources
            })

    print("\n=== STRUCTURED ROADMAP ===\n")
    print(json.dumps(roadmap, indent=2))
    return roadmap

def generate_chat_response(user_query):
    prompt = (
        f"The user has the following question about financial literacy:\n"
        f"{user_query}\n\n"
        f"Please answer in simple and beginner-friendly terms. "
        f"Provide useful links where appropriate in Markdown format like [title](https://example.com). "
        f"Limit your response to 300 words."
    )

    client = genai.Client(
        vertexai=True,
        project="hack-team-off-the-ledger",
        location="global",
    )

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

    config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=1024,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
        ],
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )

    output = ""
    for chunk in client.models.generate_content_stream(model="gemini-2.5-flash-lite", contents=contents, config=config):
        output += chunk.text
    return output
