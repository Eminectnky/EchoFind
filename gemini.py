def gemini(song_names):
    import os
    import google.generativeai as genai
    from dotenv import load_dotenv

    load_dotenv()

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

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

    song_list_str = ", ".join(song_names)
    response = model.generate_content(f"Bu şarkılardan yola çıkarak motive edici birkaç cümle yaz lütfen. Şarkı listesi: {song_list_str}")


    return response.text