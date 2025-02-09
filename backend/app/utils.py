from app.tools.intent_classifier import classify_intent
from app.tools.memory import add_to_memory,retrieve_memory
from prompts import qa_prompt,followup_prompt,ContextQueryResponse


def qa_handler(user_message: str, llm: Any) -> str:
    response = llm(qa_prompt.format(user_message=user_message))
    return response.strip()

def handle_followup_intent(current_question: str, llm: Any) -> str:
    # Retrieve conversation history
    history = retrieve_memory()
    history_text = "\n".join(
        [f"User: {entry['user']}\nAssistant: {entry['assistant']}" for entry in history]
    )

    # Assess relevance of history
    context_check = ContextQueryResponse.model_validate(
        llm(f"""
            Does the following conversation history provide relevant context to the user's query?

            History: {history_text}
            Query: {current_question}

            Provide a JSON response with "relevant" and "query" keys.
        """)
    )

    if not context_check.relevant:
        history_text = ""  # Exclude irrelevant history

    # Generate a response
    metadata = "No specific metadata available."  # Default metadata for now
    response = llm(followup_prompt.format(
        history=history_text,
        current_question=current_question,
        metadata=metadata
    ))

    return response.strip()


def handle_query(user_message: str, llm: Any):
    intent = classify_intent(user_message, llm)

    # Get conversation history from memory
    history = get_conversation_history()

    if intent == "QA":
        response = qa_handler(user_message, llm)
    elif intent == "Follow-up":
        # Handle Follow-up intent with history
        metadata = history.get("metadata", {})  # Fetch metadata if any
        response = followup_handler(user_message, llm, metadata)
    elif intent == "Recommendation":
        # Handle Recommendation intent using vector search
        embeddings = perform_vector_search(user_message)
        response = recommendation_handler(user_message, embeddings, llm)
    else:
        response = "Sorry, I couldn't classify your query. Please try again."

    # Store the interaction in memory
    add_to_memory(user_message, response)

    return response
