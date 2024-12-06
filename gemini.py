def gemini():
    import os
    import google.generativeai as genai
    from dotenv import load_dotenv

    load_dotenv()

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    prompt = "Eskişehir hakkında bilgi ver"

    response = model.generate_content("Malatya hakkında bilgi ver")

    print(response.text)

    return response.text

gemini()