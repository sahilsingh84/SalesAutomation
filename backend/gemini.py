import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

system_prompt_1 = "You are an AI assistant. You will be provided with the text of a speech from a person. You have to give me the summary of that text in structured and concise manner."

model1 = genai.GenerativeModel(
  model_name="gemini-1.5-flash-8b",
  generation_config=generation_config,
  system_instruction=system_prompt_1,
)

def chat_with_gemini(input_text, history):
  chat_session = model1.start_chat(history=history)
  response = chat_session.send_message(input_text)
  return response.text
