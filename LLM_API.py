# this is build ontop of ollama http server, make sure the server actually 
# works and has the model you specified in the config file


# this class is just an example class it is not fully completed as of now
# this file  is responsible  only for  sending message  keeping  track of
# message history if remember_messages is active



import requests
import Config
import copy





class AIAgent:
    def __init__(self):

        """
            the fields are fully changable on the go though they will come
            with the  base defult pramaters  from the  config file and the
            setting that you specifiy in the config file
        """


        self.hostname:str = Config.OLLAMA_BASE_URL
        self.model:str = Config.DEFULT_LLM_MODEL
        self.promet:str = Config.DEFULT_LLM_PROMT
        self.temperature:float = Config.DEFULT_LLM_TEMPRETURE
        self.top_p:float = Config.DEFULT_LLM_TOP_P
        self.top_k:float = Config.DEFULT_LLM_TOP_K

        self.format:str = Config.DEFULT_LLM_FORMAT
        self.repeat_penalty:float = Config.DEFULT_LLM_RPEAT_PENLETY

        self.stream:bool = False


        self.model_name:str = "" # you set the model name
        self.remember_messages:bool = False


        self.message_history = [# this will track the last messages
                {"role": "system", "content": self.promet} # add the promet to the message histroy this how it should be
            ] 



    def message(self, user_message:str) -> str:
        """
            responsible for sendint the message to the user

            tihs function will hold more features later on down the line
        """




        response = self.send_message_request(user_message)

        return response



    def send_message_request(self, message:str) -> str:

        if self.remember_messages:
            _messages = self.message_history
        else:
            _messages = copy.deepcopy(self.message_history) # this right now copies  all the messages consider reversing
                                                            # methode this arguably is not effiecent and up to standards

        _messages.append({"role": "user", "content": message})

        response = requests.post(
            self.hostname + "/api/chat",
            json={
                "model": self.model,
                "messages": _messages,
                "format": self.format,
                "options": {
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "top_k": self.top_k,
                    "repeat_penalty": self.repeat_penalty
                },
                "stream": self.stream
            }
        )

        reply_text = response.json()["message"]["content"]
        _messages.append({"role": "assistant", "content": reply_text})
        return reply_text
        




    





    