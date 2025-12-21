# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
After analyzing the 'extract_action_items' function. 
Your task is to implement an LLM-powered alternative, `extract_action_items_llm()`, that utilizes Ollama to perform action item extraction via llama3.1:8b.
You should plan first, for reference you can go to https://ollama.com/blog/structured-outputs for knowing how to produce structured outputs, after writing codes, you should ask for my permission and check the logic carefully to prevent fatal errors.
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
Line 92 - 139
def extract_action_items_llm(text: str) -> List[str]:
    """
    LLM-powered extraction using Ollama and llama3.1:8b.
    Uses structured JSON output to ensure reliable parsing.
    """
    if not text.strip():
        return []

    # Define the expected JSON schema for structured output
    schema = {
        "type": "object",
        "properties": {
            "action_items": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["action_items"]
    }

    try:
        response = chat(
            model='llama3.1:8b',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a task management assistant. Extract a list of actionable items, tasks, or commitments from the provided text. Return ONLY a JSON object.'
                },
                {
                    'role': 'user',
                    'content': f'Extract action items from this text:\n\n{text}'
                }
            ],
            format=schema  # Enforcement of structured output
        )
        
        # Parse the JSON response
        result = json.loads(response.message.content)
        extracted = result.get("action_items", [])
        
        # Simple cleanup: strip results and remove any empty strings
        return [item.strip() for item in extracted if item.strip()]
        
    except Exception as e:
        print(f"Error during LLM extraction: {e}")
        # Optionally fall back to the heuristic version or return an empty list
        return []

```

### Exercise 2: Add Unit Tests
Prompt: 
```
As a powerful coder and helpful assistant,
After finishing code snippets for the function above,
Write unit tests for `extract_action_items_llm()` covering multiple inputs (e.g., bullet lists, keyword-prefixed lines, empty input) in `week2/tests/test_extract.py`.
After that, you 'd better run the unit tests to verify the availability of the llm-powered extract function you have written.
``` 

Generated Code Snippets:
```
def test_extract_llm_empty():
    assert extract_action_items_llm("") == []
    assert extract_action_items_llm("   ") == []


@pytest.mark.skipif(settings.SKIP_LLM_TESTS, reason="Skipping LLM tests")
def test_extract_llm_bullets():
    text = """
    - Finish the report
    * [ ] Send email to team
    1. Update the wiki
    """
    items = extract_action_items_llm(text)
    # LLM might rephrase slightly, but should capture the core
    assert any("report" in item.lower() for item in items)
    assert any("email" in item.lower() for item in items)
    assert any("wiki" in item.lower() for item in items)


@pytest.mark.skipif(settings.SKIP_LLM_TESTS, reason="Skipping LLM tests")
def test_extract_llm_keywords():
    text = """
    todo: buy milk
    action: fix the bug
    next: refactor the code
    """
    items = extract_action_items_llm(text)
    assert any("milk" in item.lower() for item in items)
    assert any("bug" in item.lower() for item in items)
    assert any("refactor" in item.lower() for item in items)


@pytest.mark.skipif(settings.SKIP_LLM_TESTS, reason="Skipping LLM tests")
def test_extract_llm_narrative():
    text = "We had a meeting today. Gabriel should update the documentation by Friday and we need to schedule a follow-up."
    items = extract_action_items_llm(text)
    assert any("documentation" in item.lower() for item in items)
    assert any("follow" in item.lower() for item in items)

```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
week2
 You have done a great job,now as a powerful coding expert and careful developer,you are required to perform a refactor of the code in the backend, focusing in particular on well-defined API contracts/schemas, database layer cleanup, app lifecycle/configuration, error handling.
Before making any changes, ask for my permission and show how you wanna refactor the existing code and why.
``` 

Generated/Modified Code Snippets:
```
TODO: List all modified code files with the relevant line numbers. (We anticipate there may be multiple scattered changes here – just produce as comprehensive of a list as you can.)
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 