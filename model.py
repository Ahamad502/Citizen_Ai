"""Model loader with a lightweight fallback.

If `transformers` and `torch` are installed and a model can be loaded,
the real model will be used. Otherwise a small deterministic fallback
response function is provided so the Flask app can run in development
without heavy dependencies.
"""
from typing import Callable

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch

    model_path = "gpt2"  # much smaller and lightweight
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path).to(device)

    def granite_generate_response(prompt: str) -> str:
        """Generate a response using the loaded causal LM.

        Returns a string; on generation error returns a short apology.
        """
        try:
            inputs = tokenizer(prompt, return_tensors="pt").to(device)
            output = model.generate(**inputs, max_new_tokens=100)
            return tokenizer.decode(output[0], skip_special_tokens=True)
        except Exception as e:
            print("Model generation error:", e)
            return "Sorry, I couldn't generate a response right now."

except Exception as _load_err:
    # Fallback if transformers/torch not available or model fails to load
    print("Transformers/Torch not available or failed to load. Using fallback.", _load_err)

    def granite_generate_response(prompt: str) -> str:
        """A deterministic, safe fallback response generator for development.

        This keeps the web app functional without requiring the heavy ML stack.
        """
        p = prompt.strip()
        lower = p.lower()
        if not p:
            return "Please say something so I can respond."
        if "hello" in lower or "hi" in lower:
            return "Hi there! I'm running in fallback mode. How can I help you?"
        if any(x in lower for x in ("problem", "help", "issue", "error")):
            return "I'm sorry to hear you're having an issue. Can you describe it in more detail?"
        # default echo with a short canned completion
        return f"You said: {p}\n\n(Fallback reply) Could you provide more details or ask a specific question?"
