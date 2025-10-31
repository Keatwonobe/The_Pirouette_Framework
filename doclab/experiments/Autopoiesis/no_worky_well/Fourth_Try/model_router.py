# model_router.py (v2)
from __future__ import annotations
import os, time, json, sys
from typing import Tuple
from tenacity import retry, wait_exponential_jitter, stop_after_attempt

class GenError(RuntimeError):
    pass

# --- OpenAI detection (new vs legacy) ---
_openai_mode = "none"
_openai_pkg = None
try:
    import openai as _openai_pkg
    _openai_pkg = _openai_pkg
    _has_client = hasattr(_openai_pkg, "OpenAI")  # new API
    if _has_client:
        from openai import OpenAI
        _oa = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        _openai_mode = "responses"  # new API
    else:
        # legacy 0.27/0.28 style; will try to use ChatCompletion as a fallback
        import openai as openai_legacy
        if not os.getenv("OPENAI_API_KEY"):
            raise GenError("OPENAI_API_KEY not set for legacy client.")
        openai_legacy.api_key = os.getenv("OPENAI_API_KEY")
        _openai_mode = "legacy"
except Exception:
    _oa = None
    _openai_mode = "none"

# --- Gemini (optional) ---
try:
    import google.generativeai as genai
    if os.getenv("GOOGLE_API_KEY"):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        _gm_ready = True
    else:
        _gm_ready = False
except Exception:
    _gm_ready = False


def _sidecar_log(provider: str, model: str, usage: dict):
    try:
        os.makedirs(".usage", exist_ok=True)
        stamp = str(int(time.time() * 1000))
        with open(f".usage/{provider}__{model or 'unknown'}__{stamp}.json", "w", encoding="utf-8") as f:
            json.dump({"provider": provider, "usage": usage}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


@retry(wait=wait_exponential_jitter(initial=1, max=20), stop=stop_after_attempt(5))
def _openai_generate(model: str, prompt: str, max_output_tokens: int, temperature: float) -> Tuple[str, dict]:
    if _openai_mode not in {"responses", "legacy"}:
        raise GenError("OpenAI client not initialized (upgrade/openai import issue).")

    try:
        if _openai_mode == "responses":
            # --- FINAL ROBUST CODE ---
            
            # Check if the model is a special reasoning model that rejects creative parameters.
            is_reasoning_model = 'gpt-5' in model.lower() # Add other models here if needed

            # Start with the base parameters required by all models
            params = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_completion_tokens": max_output_tokens,
            }

            # Only add creative-tuning parameters for non-reasoning models
            if not is_reasoning_model:
                params["temperature"] = temperature
                # You could also add other standard parameters here, like:
                # params["top_p"] = top_p_value

            resp = _oa.chat.completions.create(**params)
            # ADD THIS LINE FOR DEBUGGING:
            print(f"DEBUG: Finish reason = {resp.choices[0].finish_reason}")
            text = resp.choices[0].message.content or ""
            
            usage = {
                "mode": _openai_mode,
                "model": model,
                "input_tokens": resp.usage.prompt_tokens,
                "output_tokens": resp.usage.completion_tokens,
                "total_tokens": resp.usage.total_tokens,
            }
            return text, usage
            # --- END OF FINAL CODE ---

        else: # Legacy fallback
            # (No changes needed for the legacy part)
            import openai as openai_legacy
            is_reasoning_model = 'gpt-5' in model.lower()
            
            # Build params dict for legacy call
            legacy_params = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_output_tokens,
            }
            if not is_reasoning_model:
                legacy_params["temperature"] = temperature

            comp = openai_legacy.ChatCompletion.create(**legacy_params)
            text = comp["choices"][0]["message"]["content"]
            usage = {
                "mode": _openai_mode,
                "model": model,
                "input_tokens": comp.get("usage", {}).get("prompt_tokens"),
                "output_tokens": comp.get("usage", {}).get("completion_tokens"),
                "total_tokens": comp.get("usage", {}).get("total_tokens"),
            }
            return text, usage

    except Exception as e:
        try:
            from openai import BadRequestError, AuthenticationError, PermissionDeniedError, RateLimitError
            if isinstance(e, (BadRequestError, AuthenticationError, PermissionDeniedError, RateLimitError)):
                raise GenError(f"OpenAI API Error: {e}") from e
        except ImportError:
            pass
        raise


@retry(wait=wait_exponential_jitter(initial=1, max=20), stop=stop_after_attempt(5))
def _gemini_generate(model: str, prompt: str, max_output_tokens: int, temperature: float) -> Tuple[str, dict]:
    if not _gm_ready:
        raise GenError("Gemini client not initialized (set GOOGLE_API_KEY and install google-generativeai).")
    
    m = genai.GenerativeModel(model_name=model)
    resp = m.generate_content(
        prompt,
        generation_config={"temperature": temperature, "max_output_tokens": max_output_tokens},
    )

    # --- NEW ROBUST HANDLING ---
    text = ""
    try:
        # This is the modern, safe way to get text from a Gemini response
        text = ''.join(part.text for part in resp.parts)
    except (ValueError, IndexError):
        # This block runs if resp.parts is empty or invalid
        
        # Check if the prompt itself was blocked
        if resp.prompt_feedback and resp.prompt_feedback.block_reason:
            reason = resp.prompt_feedback.block_reason.name
            raise GenError(f"Gemini prompt was blocked due to: {reason}")
        
        # Check if any generated candidates were blocked
        if resp.candidates and resp.candidates[0].finish_reason.name != "STOP":
            reason = resp.candidates[0].finish_reason.name
            raise GenError(f"Gemini generation stopped unexpectedly due to: {reason}")
        
        # If we still don't know why, return an empty string
        text = ""

    md = getattr(resp, "usage_metadata", None)
    usage = {
        "model": model,
        "input_tokens": getattr(md, "prompt_token_count", None),
        "output_tokens": getattr(md, "candidates_token_count", None),
        "total_tokens": getattr(md, "total_token_count", None), # Added total_token_count
    }
    return text, usage


def generate_text(provider: str, model: str, prompt: str, max_output_tokens: int = 1024, temperature: float = 0.7) -> str:
    if provider.lower() in {"openai", "oai"}:
        text, usage = _openai_generate(model, prompt, max_output_tokens, temperature)
        _sidecar_log("openai", model, usage)
        return text
    elif provider.lower() in {"google", "gemini"}:
        text, usage = _gemini_generate(model, prompt, max_output_tokens, temperature)
        _sidecar_log("gemini", model, usage)
        return text
    else:
        raise GenError(f"Unknown provider: {provider}")
