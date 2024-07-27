import pandas as pd
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

class ExcelAgent:

    def __init__(self, model_name: str, temperature: float, api_key: str) -> None:
        llm = ChatGoogleGenerativeAI(
            model=model_name, temperature=temperature,
            api_key=api_key
        )
        self.llm = llm
        self.tools = {
            "menu_makanan": self._agent_menu(df_location="temporary-data/menu.xlsx"),
            "restoran": self._agent_restoran(df_location="temporary-data/restaurant.xlsx"),
            "common_conversation": llm
        }
    
    def result_parser_tool(self, result: str) -> List[str]:
        print("[Result w/o Parsing]", result)
        result_parse = {'output': '', 'description': ''}
        if isinstance(result, dict):
            result_parse['output'] = result['output']
            result_parse['description'] = result['description']
        if "," in result_parse["output"]:
            result_parse["output"] = list(map(lambda char: char.strip(), result_parse['output'].split(",")))
        return result_parse

    def invoke(self, query: str, inst_prompt: str):
        tool_choosen = self.agent_routing(query=query)
        tool_agent = self.tools[tool_choosen]
        if tool_agent is not None:
            additional_query = self._additional_prompt(tool_name=tool_choosen, query=query)
            _result = tool_agent.invoke("System Instruct: " + inst_prompt + additional_query)
            print("[Result Query / LLM Raw]", _result)
            if isinstance(_result, dict):
                # _result_desc = tool_agent.invoke(
                #     # query +
                #     # "Pada query sebelumnya sudah di dapatkan ID yang ditentukan yaitu: " +
                #     # _result['output'] +
                #     "Hasilkan deskripsi berdasarkan informasi" + 
                #     "nama makanan" if tool_choosen == "menu_makanan" else "nama restoran" + 
                #     "dari ID yang telah diberikan berdasarkan kolom " +
                #     "menu_id" if tool_choosen == "menu_makanan" else "zomato_id" + 
                #     "Berdasarkan informasi yang ditemukan, jawab pertanyaan user dengan ramah, intuitif, dan naratif tanpa mention informasi terkait ID yang diberikan."
                # )
                # _result["description"] = _result_desc["output"]
                df_string = ...
                result = self.result_parser_tool(result=_result)
            else:
                result = {"output": _result.content, "description": ""}
            return result

    def agent_routing(self, query):
        list_tools = '\n'.join(self.tools)
        base_prompt_routing = \
            f"""
            Based on provided question, please choose which action / tools should be used to fulfill the question objective

            tools provided:
            {list_tools}

            Example
            -----------------------
            question: Saya mau pesan makanan hangat dan berkuah
            tools_choosen: menu_makanan

            question: saya ingin rute perjalanan hemat dari kantor ke rumah dengan menggunakan grab car / transportasi umum
            tools_choosen: rute_bus
            -----------------------
            question: {query}
            tools_choosen: 
            """
        result = self.llm.invoke(input=base_prompt_routing)
        parse_result = result.content.split(":")[1].strip()
        print("[Tool Choosen]", parse_result)
        return parse_result
    
    def _additional_prompt(self, tool_name: str, query: str) -> str:
        result_query = query
        if tool_name == "menu_makanan":
            result_query += " Cukup berikan menu_id dengan maksimal 3 item yang dipisah dengan koma (,)"
        elif tool_name == "restoran":
            result_query += " Cukup berikan id_zomato dengan maksimal 3 item yang dipisah dengan koma (,)"
        elif tool_name == "rute_bus":
            # TODO: transID
            pass
        return result_query

    def _agent_menu(self, df_location: str):
        data_menu = pd.read_excel(df_location)
        data_menu = data_menu.head(100)
        agent_menu = create_pandas_dataframe_agent(
            llm=self.llm, df=data_menu, verbose=True,
            max_iterations=5, allow_dangerous_code=True
        )
        return agent_menu

    def _agent_restoran(self, df_location: str):
        data_restoran = pd.read_excel(df_location)
        data_restoran = data_restoran.head(100)
        data_restoran.columns = list(map(lambda name: name.strip(), data_restoran.columns))
        agent_restorant = create_pandas_dataframe_agent(
            llm=self.llm, df=data_restoran, verbose=True,
            max_iterations=5, allow_dangerous_code=True
        )
        return agent_restorant