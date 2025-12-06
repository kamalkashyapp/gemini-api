import json
import google.generativeai as genai
import os

def handler(request):
    try:
        query = request.get("query", {})
        mode = query.get("mode", "text")
        prompt = query.get("prompt", None)
    except:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Invalid request format"})
        }

    if not prompt:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Prompt required"})
        }

    API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=API_KEY)

    # TEXT MODE ONLY (SAFE)
    if mode == "text":
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            result = model.generate_content(prompt)

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "success": True,
                    "response": result.text
                })
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "Gemini text generation failed",
                    "details": str(e)
                })
            }

    # INVALID MODE
    return {
        "statusCode": 400,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": "Invalid mode (only text supported)"})
        }
