



# this section is for the data


OUTPUT_DATA_PATH = "filtered_data/"

RELEVENT_DATA_PATH = OUTPUT_DATA_PATH + "relevant_data.jsonl" # this contain all the data that has been filtered it will contain all the tags that you speicified
DISCARDED_DATA_PATH = OUTPUT_DATA_PATH + "discarded_data.jsonl" # this contain all the data that is discarded
ERROR_DATA_PATH = OUTPUT_DATA_PATH + "error_data.jsonl"






TAGS = [
    "CIVIL_ENGINEERING",
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
DEFULT_LLM_PROMT = f"""You are a strict classification engine.

RULES:

1. Output MUST be valid JSON only. No extra text.
2. The JSON must be an array.
3. Each item in the array must have:
- "Reason": string
- "Tags": array
4. The only allowed tags is: {TAGS}
5. Only include the tag if the paper is clearly related to civil engineering (structures, infrastructure, construction, transportation systems, water systems, geotechnical engineering, structural mechanics, etc.)
6. If the paper is NOT related to civil engineering, return: []
7. If the paper is has anything to do with civil engneering then include the civil engineering tag

Civil Engineering Domain Definition Array:

[
  "Structural engineering (buildings, bridges, towers, dams)",
  "Construction engineering and project management",
  "Transportation engineering (roads, highways, railways, traffic systems)",
  "Water resources engineering (hydrology, flood control, drainage systems)",
  "Environmental civil engineering (wastewater treatment, water supply systems)",
  "Coastal and offshore engineering",
  "Earthquake engineering and structural resilience",
  "Urban infrastructure systems",
  "Concrete, steel, and construction materials research",
  "Pavement design and analysis",
  "Tunnel and underground structure design",
  "Hydraulic structures (canals, spillways, reservoirs)",
  "Surveying and geomatics for infrastructure",
  "Infrastructure maintenance and asset management",
  "anyhting has to do with materials of buidlings",
  "facades, discussing architectural, environmental, and structural aspects"
]


IMPORTANT:

- If unrelated, return an empty JSON array [].
- Do NOT explain outside JSON.
- Reason must come before Tags in the object.
- When it comes to tags think if the Tag has any ralation to the paper and if so add the Tag, be lenient

Example (related case):

[
  {{
  "Reason": "The paper studies structural load behavior in reinforced concrete bridges.",
  "Tags": ["CIVIL_ENGINEERING"]
  }}
]
"""