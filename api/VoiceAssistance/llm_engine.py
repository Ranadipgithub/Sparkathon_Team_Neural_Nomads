from groq import Groq
from VoiceAssistance import API_KEY,MODEL_NAME,TEMPERATURE,MAX_TOKENS

def llm_output(system_prompt):
  
  client = Groq(api_key=API_KEY)
  completion = client.chat.completions.create(
      model=MODEL_NAME,
      messages=[
        {
          "role": "user",
          "content": system_prompt
        }
      ],
      temperature=TEMPERATURE,
      max_completion_tokens=MAX_TOKENS,

  )

  return (completion.choices[0].message.content)