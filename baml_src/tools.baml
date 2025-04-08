class WeatherAPI {
  tool_name "weather_api_call" @description("Use this tool to get weather information")
  city string @description("City for which to get weather")
  time string @description("Current time in ISO8601 format")
  @@description("This tool returns current weather information for a city.")
}

class CalculatorAPI {
  tool_name "calculator_api_call" @description("Use this tool to perform calculations")
  operation "add" | "subtract" | "multiply" | "divide"
  numbers float[]
}

class FinishAction {
  tool_name "finish" @description("This indicates that the agent has finished")
  value float
}

class Observation {
  result string @description("The observed result from taking an action")
}


class Thought {
  reasoning string @description("Reasoning about the current state and next steps")
  action WeatherAPI | CalculatorAPI | FinishAction @description("The next action to take")
}

function React(
  question: string,
  observations: Observation[]
) -> Thought {
  client "openai/gpt-4o"
  prompt #"
    You are a ReAct (Reason, Act, Observe) agent that breaks down problems by thinking step by step and taking actions. 
    Given the question and previous observations, think about what to do next.

    Think carefully about:
    1. What you learned from previous observations
    2. What next action would help answer the question
    3. When you have enough information to finish

    {{ ctx.output_format }}

    {{ _.role("user") }}
    Question: {{ question }}

    Previous observations:
    {% for obs in observations %}
    Observation: {{ obs.result }}
    {% endfor %}
  "#
}

test SimpleQuestion {
  functions [React]
  args {
    question "What is the capital of France?"
    observations []
  }
}

test WithObservations {
  functions [React]
  args {
    question "Find the current weather in Seattle and multiply by 2."
    observations [
      {
        result "The current weather in Seattle is 72 degrees"
      }
    ]
  }
}
