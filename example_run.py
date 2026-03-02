from assistant_framework import Assistant, Request


def main() -> None:
    assistant = Assistant()
    examples = [
        "My checkout page is broken and users see an error.",
        "Can you draft an email announcing our new feature?",
        "I need a strategy and roadmap for onboarding.",
    ]

    for text in examples:
        result = assistant.handle(Request(user_id="demo-user", text=text))
        print(f"Input: {text}")
        print(f"Intent: {result.intent.value} (confidence={result.confidence:.2f})")
        print(f"Response: {result.content}")
        print("-" * 60)


if __name__ == "__main__":
    main()
