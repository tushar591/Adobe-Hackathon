import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

print("--- Attempting to download the 'punkt' package ---")
try:
    nltk.download('punkt')
    print("\n[SUCCESS] 'punkt' package seems to be installed correctly.")
except Exception as e:
    print(f"\n[ERROR] Could not download 'punkt'. Error: {e}")
    print("--- Trying to download all packages as a fallback (this might take a while) ---")
    try:
        nltk.download('all')
        print("\n[SUCCESS] All NLTK packages downloaded. This should resolve the issue.")
    except Exception as e_all:
        print(f"\n[ERROR] Could not download all packages. Error: {e_all}")
        