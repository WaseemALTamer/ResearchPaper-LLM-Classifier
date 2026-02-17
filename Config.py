



# this section is for the data



RELEVENT_DATA_PATH = "filtered_data/relevant_data.jsonl" # this contain all the data that has been filtered
DISCARDED_DATA_PATH = "filtered_data/discarded_data.jsonl" # this contain all the data that is discarded
ERROR_DATA_PATH = "filtered_data/error_data.jsonl"







TAGS = [
    "CIVIL_ENGINEERING",
    "ARTIFICIAL_INTELLIGENCE"
]



# this section is for the llm and ollama ai model 


OLLAMA_BASE_URL = "http://127.0.0.1:11434/"



DEFULT_LLM_MODEL = "llama3.1:8b-instruct-q8_0"  # make sure that the ollama server is on and also the 
                                                # model actually exist on your server it self
            
DEFULT_LLM_TEMPRETURE = 0   
DEFULT_LLM_TOP_P = 1   
DEFULT_LLM_TOP_K = 0
DEFULT_LLM_FORMAT = "json"
DEFULT_LLM_RPEAT_PENLETY = 1

# this is instruction/promet that you want to give to your LLM
DEFULT_LLM_PROMT = f"""
You are a strict academic paper classification engine.

Output Rules:
- Output MUST be valid JSON only.
- Output must be a JSON array.
- If unrelated to all allowed domains, return [].
- Each object must contain:
    "Reason": string
    "Tags": array
- Allowed tags: {TAGS}
- Only include a tag if the paper is clearly related to that domain.

Domain Definitions:

CIVIL_ENGINEERING includes:
- Structural engineering (bridges, buildings, dams)
- Transportation systems
- Water resources and hydraulics
- Geotechnical engineering
- Construction engineering
- Infrastructure systems
- Building materials (concrete, steel, facades)

ARTIFICIAL_INTELLIGENCE includes:
- Machine learning and deep learning
- Neural networks and optimization
- Computer vision and NLP
- Reinforcement learning
- Generative models
- AI model training and evaluation

IMPORTANT:
- Do NOT explain outside JSON.
- If no domain applies, return [].
- Reason must appear before Tags.

Example:
[
  {{
    "Reason": "The paper analyzes load distribution in reinforced concrete bridges.",
    "Tags": ["CIVIL_ENGINEERING"]
  }}
]
"""