# this is the file responsible for loading  the data sets that you give
# it and filtering the data through the LLM though you need to interact
# with this manager through  jupeter notebook  so you can run functions
# on the run

from LLM_API import AIAgent
import pandas as pd
import Config
import json
import copy
import os




class Manager:
    def __init__(self):
        self.data:list[dict] = [] # load the all the data into here


        self.filter_queue:list[dict] = [] # this contain data that are on the queue to be filtered

        self.error_data:list[dict] = [] # this is where the errors will live, they are not loaded up only stored

        self.discarded_data:list[dict] = [] # this is where the data that gets filtered lives
        self.relevant_data:list[dict] = [] # this is where the data we want lives


        self.ai_agent = AIAgent() # we create an instant  for the use later the pramaters
                                  # and  configration are  already set  inside the config
                                  # file please update the pramaters from there if needed

        
        




    def load_data(self, file_path:str) -> None:
        """
            load the data from either .csv file or a .xls or .xlsx file
            this will also load the file for you if it is a json file
        """

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == ".csv":
            df = pd.read_csv(file_path)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(file_path)
        elif ext == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        df.columns = df.columns.str.strip()

        data = df.to_dict(orient="records")

        self.data = data


    def jsonl_save_item(self, file_path:str, item:dict) -> None:
        """
            this saves one item at a time this should be used
            for the ".jsonl" files, dont try to load 
        """

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    
    def jsonl_load(self, file_path:str) -> dict:
        """
            this will load the jsonl file dont load normal json 
            files this function  will not  be able  to and will
            give an error, this  function  will return the data
            it is your job to store it 
        """

        with open(file_path, "r", encoding="utf-8") as f:
            relevant_data = [json.loads(line) for line in f]

        return relevant_data
    



    def load_already_filtered_data(self):

        # loads the files
        _relvent_data = self.jsonl_load(Config.RELEVENT_DATA_PATH)
        _discarded_data = self.jsonl_load(Config.DISCARDED_DATA_PATH)
        
        # adds the data to the public lists
        self.relevant_data = _relvent_data
        self.discarded_data = _discarded_data


    def add_data_to_filter_queue(self):
        self.filter_queue = copy.deepcopy(self.data)
    


    def remove_filtred_from_queue(self):
        """
            Removes data from self.filter_queue if it exists in
            self.discarded_data or self.relevant_data,
            comparing dictionaries while ignoring the "Classification" key.
        """

        def strip_classification(d: dict) -> dict:
            return {k: v for k, v in d.items() if k != "Classification"} # we remove the casification

        # Preprocess comparison sets (faster lookup)
        discarded_stripped = [strip_classification(d) for d in self.discarded_data]
        relevant_stripped = [strip_classification(d) for d in self.relevant_data]

        _filtered_queue = []

        for item in self.filter_queue:
            stripped_item = strip_classification(item)

            if stripped_item not in discarded_stripped and stripped_item not in relevant_stripped:
                _filtered_queue.append(item)

        self.filter_queue = _filtered_queue



    

    def start_filtering(self):
        """
            this function will loop thruogh  the data in the queue
            and will  start filtering the data one at  a time this
            function will  use the LLM to filter out the data that
            and double check  if everything adds  up this function
            is redundednt to  ai outputing garbage if that happens
            then we simply just  discard the item but  add it into
            the error file so you can view it later with the error
            inside the item
        """


        # loop through the queue in reverse and pop the last item
        # from the queue once it gets proccessed 
        for i in range(len(self.filter_queue) - 1, -1, -1):
            item = self.filter_queue[i]
            try:
                item_string = json.dumps(item) # convert the item to string json formate
                response = self.ai_agent.message(item_string) # send it to the ai
                json_response = json.loads(response) # convert the respond to json this will verfy the

                item["Classification"] = json_response # we add the ai classification

                _valid_item = True
                for tag in Config.TAGS:
                    if tag not in json_response["Tags"]:
                        _valid_item = False # if the tag is not in there then it is a not valid item
                        break

                    if tag in json_response["Tags"]:
                        path = Config.OUTPUT_DATA_PATH + f"{tag}.jsonl"
                        self.jsonl_save_item(path, item)
                
                if _valid_item:
                    # valid items gets saved and appended to the saved
                    self.relevant_data.append(item)
                    self.jsonl_save_item(Config.RELEVENT_DATA_PATH, item)
                else:
                    # invalid items get disbanded
                    self.discarded_data.append(item)
                    self.jsonl_save_item(Config.DISCARDED_DATA_PATH, item)
                

            except Exception as e: 
                # add the error to the item then save it in jsonl file
                item["Error"] = f"{e}"
                self.jsonl_save_item(Config.ERROR_DATA_PATH, item)
            

            self.filter_queue.pop(i) # remove the last item from queue

