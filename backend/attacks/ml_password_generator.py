import math
import random
import os
from typing import List, Dict, Any

# Common character transition & leet substitution matrix
LEET_MAP = {
    'a': ['4', '@', 'A'],
    'e': ['3', 'E'],
    'i': ['1', '!', 'I'],
    'o': ['0', 'O'],
    's': ['$', '5', 'S'],
    't': ['7', '+', 'T'],
    'b': ['8', 'B'],
    'g': ['9', 'G']
}

COMMON_DELIMITERS = ['@', '#', '$', '!', '_', '.', '-', '&']
COMMON_AFFIXES = ['!', '@', '#', '$', '!!', '123', '2026', '!@#', '01', '99']
COMMON_PREFIXES = ['The', 'My', 'Super', 'Pro', 'Corp', 'Sec']

def calculate_entropy(password: str) -> float:
    """Calculates Shannon entropy in bits for a given password string."""
    if not password:
        return 0.0
    charset_size = 0
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    if has_lower: charset_size += 26
    if has_upper: charset_size += 26
    if has_digit: charset_size += 10
    if has_special: charset_size += 32

    # Shannon bits = L * log2(R)
    return round(len(password) * math.log2(max(charset_size, 2)), 1)

def apply_leet_transform(token: str, mutation_rate: float) -> str:
    """Probabilistically applies character substitutions based on temperature/rate."""
    result = []
    for char in token:
        lower_c = char.lower()
        if lower_c in LEET_MAP and random.random() < mutation_rate:
            result.append(random.choice(LEET_MAP[lower_c]))
        else:
            result.append(char)
    return "".join(result)

class GenerativePasswordMutator:
    """
    Generative Character-level and Context-Free Grammar (PCFG) model for 
    synthesizing targeted credential candidates based on organizational metadata.
    Emulates the behavior of PassGAN and Character-RNN dictionary mutators.
    """
    def __init__(self, seed: int = None):
        if seed:
            random.seed(seed)

    def generate(
        self,
        brand_tokens: List[str] = None,
        user_handle: str = "admin",
        department: str = "Security",
        year: str = "2026",
        temperature: float = 0.7,
        count: int = 15
    ) -> List[Dict[str, Any]]:
        brand_tokens = brand_tokens or ["Sentinel", "Strike"]
        year_str = str(year)
        short_year = year_str[-2:] if len(year_str) == 4 else "26"

        # Core semantic tokens
        all_tokens = list(set([t.strip() for t in brand_tokens if t.strip()] + [user_handle, department]))
        if not all_tokens:
            all_tokens = ["Sentinel", "Admin"]

        candidates = set()
        results = []

        # Archetype structural generation patterns
        patterns = [
            # Pattern 1: TitleCase Base + Delimiter + Full Year + Symbol
            ("TitleCase + Delim + Year + Symbol", 0.95),
            # Pattern 2: Leet-Mutated Brand + Short Year + Bang
            ("Leet Mutation + ShortYear + Symbol", 0.88),
            # Pattern 3: UserHandle + Brand Token + Year
            ("Compound User-Brand + Year", 0.82),
            # Pattern 4: Department + Delimiter + Year + Suffix
            ("Department + Delim + Year + Affix", 0.90),
            # Pattern 5: Prefix + Leet Token + Delim + Symbol
            ("Prefix + Leet Token + Delim", 0.75),
            # Pattern 6: High-Entropy Custom Jitter
            ("Adversarial Jitter Composite", 0.68)
        ]

        # Generate candidates until we reach desired count
        attempts = 0
        while len(candidates) < count and attempts < 150:
            attempts += 1
            archetype, base_likelihood = random.choice(patterns)
            token = random.choice(all_tokens)
            delim = random.choice(COMMON_DELIMITERS) if random.random() < 0.85 else ""
            symbol = random.choice(COMMON_AFFIXES)

            # Mutation probability scales with temperature (0.1 to 1.0)
            mutation_prob = max(0.1, min(0.9, temperature * 0.8))

            if archetype == "TitleCase + Delim + Year + Symbol":
                pwd = f"{token.capitalize()}{delim}{year_str}{random.choice(['!', '@', '#'])}"
            elif archetype == "Leet Mutation + ShortYear + Symbol":
                mutated = apply_leet_transform(token.capitalize(), mutation_prob)
                pwd = f"{mutated}{delim}{short_year}{symbol}"
            elif archetype == "Compound User-Brand + Year":
                other = random.choice(all_tokens)
                pwd = f"{token.capitalize()}{other.capitalize()}{year_str}"
            elif archetype == "Department + Delim + Year + Affix":
                pwd = f"{department.capitalize()}{delim}{year_str}!"
            elif archetype == "Prefix + Leet Token + Delim":
                prefix = random.choice(COMMON_PREFIXES)
                mutated = apply_leet_transform(token, mutation_prob)
                pwd = f"{prefix}_{mutated}{short_year}"
            else:
                # High-entropy adversarial mutation
                mutated = apply_leet_transform(token, 0.8)
                pwd = f"{random.choice(['$', '#'])}{mutated}@{year_str}!"

            if pwd not in candidates and len(pwd) >= 6:
                candidates.add(pwd)
                entropy = calculate_entropy(pwd)
                # Likelihood adjusts slightly with temperature
                likelihood = max(0.40, min(0.98, base_likelihood - (temperature - 0.5) * 0.2 + random.uniform(-0.03, 0.03)))

                results.append({
                    "password": pwd,
                    "pattern": archetype,
                    "entropy_bits": entropy,
                    "human_likelihood": round(likelihood * 100, 1),
                    "base_token": token
                })

        # Sort by human likelihood descending
        results.sort(key=lambda x: x["human_likelihood"], reverse=True)
        return results[:count]


def write_candidates_to_wordlist(candidates: List[str]) -> str:
    """Overwrites or appends the generated candidates to the active attack wordlist."""
    wordlist_dir = os.path.join(os.path.dirname(__file__), "wordlists")
    os.makedirs(wordlist_dir, exist_ok=True)
    passwords_file = os.path.join(wordlist_dir, "passwords.txt")

    # Keep unique passwords
    existing = []
    if os.path.exists(passwords_file):
        with open(passwords_file, "r") as f:
            existing = [l.strip() for l in f if l.strip()]

    # Combine: new candidates first, followed by previous
    combined = list(dict.fromkeys(candidates + existing))

    with open(passwords_file, "w") as f:
        f.write("\n".join(combined) + "\n")

    return passwords_file
