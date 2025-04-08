from baml_client.async_client import b
from baml_client.types import Resume
from dotenv import load_dotenv

load_dotenv()

async def example(raw_resume: str) -> Resume: 
  # BAML's internal parser guarantees ExtractResume
  # to be always return a Resume type
  response = await b.ExtractResume(raw_resume)
  return response

async def example_stream(raw_resume: str) -> Resume:
  stream = b.stream.ExtractResume(raw_resume)
  async for msg in stream:
    print(msg) # This will be a PartialResume type
  
  # This will be a Resume type
  final = await stream.get_final_response()

  return final

if __name__ == "__main__":
  import asyncio
  asyncio.run(example_stream("""
  Vaibhav Gupta
      vbv@boundaryml.com

      Experience:
      - Founder at BoundaryML
      - CV Engineer at Google
      - CV Engineer at Microsoft

      Skills:
      - Rust
      - C++
  """))