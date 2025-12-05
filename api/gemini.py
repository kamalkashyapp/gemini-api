import json
import google.generativeai as genai
import os

def handler(request):
    query = request.get("query", {})
    mode = query.get("mode", "text")
    prompt = query.get("prompt", "")

    if not prompt:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Prompt is required"})
        }

    API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=API_KEY)

    # TEXT GENERATION
    if mode == "text":
        model = genai.GenerativeModel("gemini-2.5-flash")
        result = model.generate_content(prompt)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "response": result.text
            })
        }

    # IMAGE GENERATION
    if mode == "image":
        model = genai.GenerativeModel("gemini-2.5-flash")
        img = model.generate_images(prompt=prompt, size="1024x1024")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "image_base64": img.images[0].image_bytes
            })
        }

    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Invalid mode"})
        }
