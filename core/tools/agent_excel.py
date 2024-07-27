import pandas as pd
from prompt import Prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

class ExcelAgent:

    def __init__(self, model_name: str, temperature: float, api_key: str) -> None:
        llm = ChatGoogleGenerativeAI(
            model=model_name, temperature=temperature,
            api_key=api_key
        )
        self.llm = llm
        self.data_grabfood = None
        agent_grabfood = self._agent_grab_food()
        self.tools = {
            "menu_makanan": agent_grabfood,
            "restoran": agent_grabfood,
            "common_conversation": llm
        }
        self._agent_grab_food()

    def direct_invoke(self, query: str, context_data: str):
        df_context = pd.DataFrame(context_data)
        list_menu_id = df_context["menu_id"].tolist()
        df_filter = self.data_grabfood[self.data_grabfood["menu_id"].isin(list_menu_id)]
        result_description = self.llm.invoke(Prompt.desc_food_prompt.format(context_data=df_filter, question=query)).content
        result = {"input": query, "output": list_menu_id, "description": result_description}
        return result

    def invoke(self, query: str, inst_prompt: str):
        tool_choosen = self.agent_routing(query=query)
        tool_agent = self.tools[tool_choosen]
        if tool_agent is not None:
            additional_query = self._additional_prompt(tool_name=tool_choosen, query=query)
            _result = tool_agent.invoke("System Instruct: " + inst_prompt + additional_query + "ambil dari nilai menu_id")
            if "," in _result["output"]:
                _result["output"] = list(map(lambda char: int(char.strip()), _result['output'].split(",")))
            print("[Result Query / LLM Raw]", _result)
            if isinstance(_result, dict):
                if tool_choosen == "menu_makanan":
                    df_filter = self.data_grabfood[self.data_grabfood['menu_id'].isin(_result["output"])].to_string()
                    result_description = self.llm.invoke(Prompt.desc_food_prompt.format(context_data=df_filter, question=query)).content
                elif tool_choosen == "restoran":
                    df_filter = self.data_grabfood[self.data_grabfood['id_zomato'].isin(_result["output"])].to_string()
                    result_description = self.llm.invoke(Prompt.desc_food_prompt.format(context_data=df_filter, question=query)).content
                _result["description"] = result_description
                _result["type"] = tool_choosen
                result = _result
            else:
                result = {"input": "System Instruct: " + inst_prompt + additional_query, "output": _result.content, "description": ""}
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
            result_query += " Cukup berikan restaurant_id dengan maksimal 3 item yang dipisah dengan koma (,)"
        elif tool_name == "rute_bus":
            # TODO: transID
            pass
        return result_query
    
    def _agent_grab_food(self):
        data_menu = pd.read_excel("temporary-data/menu.xlsx")
        data_menu = data_menu.head(100)    
        data_restoran = pd.read_excel("temporary-data/restaurant.xlsx")
        data_restoran = data_restoran.head(100)
        column_names = list(map(lambda name: name.strip(), data_restoran.columns))
        data_restoran.columns = ['restaurant_id'] + column_names[1:]
        data_agg = data_menu.merge(right=data_restoran, on="restaurant_id")
        data_agg = data_agg.drop("average_cost_for_two", axis=1)
        self.data_grabfood = data_agg
        agent_grabfood = create_pandas_dataframe_agent(
            llm=self.llm, df=data_menu, verbose=True,
            max_iterations=5, allow_dangerous_code=True
        )
        return agent_grabfood