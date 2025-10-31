
import sys, os
print("PY:", sys.executable)
try:
    import openai
    print("openai.__version__ =", getattr(openai, "__version__", "<none>"))
    print("openai module file =", getattr(openai, "__file__", "<none>"))
    print("Has OpenAI client?  ", hasattr(openai, "OpenAI"))
except Exception as e:
    print("Import error:", e)
print("OPENAI_API_KEY set?  ", bool(os.getenv("OPENAI_API_KEY")))
