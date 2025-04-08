from baml_client import b
from baml_client.types import WeatherAPI, CalculatorAPI, FinishAction, Observation
import sys


def weather_api_call(weather: WeatherAPI):
    # Simulate weather API call, but you can implement this with a real API call
    return f"The weather in {weather.city} at {weather.time} is 72."


def calculator_api_call(calc: CalculatorAPI):
    numbers = calc.numbers
    if calc.operation == "add":
        result = sum(numbers)
    elif calc.operation == "subtract":
        result = numbers[0] - sum(numbers[1:])
    elif calc.operation == "multiply":
        result = 1
        for n in numbers:
            result *= n
    elif calc.operation == "divide":
        result = numbers[0]
        for n in numbers[1:]:
            result /= n
    return f"The result is {result}"


def main():
    observations = []

    user_input = "Find the current weather in Seattle and multiply by 2."

    while True:
        # Call the BAML function to select tool
        tool_response = b.React(user_input, observations)

        if isinstance(tool_response.action, FinishAction):
            print(f"Agent (Finish): {tool_response.action.value}")
            break

        current_module = sys.modules[__name__]

        result = getattr(current_module, tool_response.action.tool_name)(tool_response.action)
        obs = Observation(result=result)
        # Call the function dynamically
        observations.append(obs)


if __name__ == "__main__":
    main()
