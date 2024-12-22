import openai

class OperationsHandler:
    def __init__(self, gpt4_api_key="api-key"):
        self.gpt4_api_key = gpt4_api_key
        openai.api_key = self.gpt4_api_key

    @staticmethod
    def parse_llm_code(llm_code):
        # Extract the function code
        function_code = llm_code.split('\n')[1:-1]
        return '\n'.join(function_code)

    def generate_operation_code(self, column, operation):
        prompt = (
            f"Write a Python function to calculate the {operation} of a list of numbers. "
            "The function should be named 'operation' and take a single argument 'values'. "
            "Give only the python code for the function. The function should be named 'operation' and should take a single argument 'values' which is a list of numbers."
            "The function should return the {operation} of the list of numbers. The list of numbers is stored in the variable 'values'. "
            "Do not include any import statements or code to read the input list of numbers. do not include any code to print the output."
            "The function should be defined as follows:\n\n def operation(values):\n   # Write your code here\n    pass\n\nThe list of numbers is stored in the variable 'values'. The function should return the {operation} of the list of numbers."
        )
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.5
        )
        generated_code = response.choices[0].message["content"]
        return self.parse_llm_code(generated_code)

    def execute_operation(self, code, values):
        local_scope = {}
        try:
            exec(code, {}, local_scope)
            operation_func = local_scope.get("operation")
            if operation_func:
                return operation_func(values)
        except Exception as e:
            print(e)
            raise RuntimeError(f"Execution error: {e}")
        return None

    def process_operation(self, column, operation, values):
        code = self.generate_operation_code(column, operation)
        return self.execute_operation(code, values)
