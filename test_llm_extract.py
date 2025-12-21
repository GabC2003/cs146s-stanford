
from week2.app.services.extract import extract_action_items_llm

test_text = """
Hey team, we had a great meeting. 
Here are the things we need to do:
1. Finish the design mockup by Tuesday.
2. [ ] Please send the email to the client regarding the contract.
- Fix the bug in the login flow.
Also, Gabriel needs to update the documentation.
Wait, I forgot, we should also schedule a follow-up.
"""

print("Extracting action items via LLM...")
items = extract_action_items_llm(test_text)
print("Extracted Items:")
for i, item in enumerate(items, 1):
    print(f"{i}. {item}")
