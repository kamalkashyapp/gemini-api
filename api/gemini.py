import json
import base64
import google.generativeai as genai

def handler(request):
    # GET parameters
    params = request.get("query", {})
    mode = params.get("mode", "text")
    prompt = params.get("prompt", "")

    if not prompt:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Prompt required"})
        }

    # Load API key from Vercel Environment
    import os
    API_KEY = os.getenv("GEMINI_API_KEY")

    genai.configure(api_key=API_KEY)

    # ==========================
    # TEXT GENERATION
    # ==========================
    if mode == "text":
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "prompt": prompt,
                "response": response.text
            })
        }

    # ==========================
    # IMAGE GENERATION
    # ==========================
    elif mode == "image":
        model = genai.GenerativeModel("gemini-2.5-flash")

        result = model.generate_images(
            prompt=prompt,
            size="1024x1024"
        )

        image_b64 = result.images[0].image_bytes

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "prompt": prompt,
                "image_base64": image_b64
            })
        }

    # Invalid mode
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid mode"})
        }
