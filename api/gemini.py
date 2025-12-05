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

    # TEXT MODE
    if mode == "text":
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "response": response.text
            })
        }

    # IMAGE MODE
    if mode == "image":
        model = genai.GenerativeModel("gemini-2.5-flash")
        result = model.generate_images(prompt=prompt, size="1024x1024")

        img_b64 = result.images[0].image_bytes

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "image_base64": img_b64
            })
        }

    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Invalid mode"})
    }
