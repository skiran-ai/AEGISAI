"""
AEGISAI - AI Malware Detection Engine

Uses scikit-learn RandomForestClassifier to analyse file byte patterns
and structural features to classify files as CLEAN or MALICIOUS.

Features extracted from each file:
  1. file_size          – total bytes
  2. entropy            – Shannon entropy of byte distribution
  3. byte_mean          – mean byte value (0-255)
  4. byte_std           – standard deviation of byte values
  5. printable_ratio    – ratio of printable ASCII chars
  6. null_ratio         – ratio of null (0x00) bytes
  7. high_byte_ratio    – ratio of bytes > 127 (non-ASCII)
  8. unique_byte_ratio  – unique byte values / 256

The model is trained once on synthetic feature vectors that represent
the statistical profiles of benign vs. malicious files and persisted to
disk.  Subsequent calls load the trained model for inference.
"""

import math
import os
import pickle
import string

import numpy as np
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml_models', 'malware_model.pkl')


# ------------------------------------------------------------------
# Feature extraction
# ------------------------------------------------------------------

def _shannon_entropy(data: bytes) -> float:
    """Calculate Shannon entropy of a byte sequence."""
    if not data:
        return 0.0
    length = len(data)
    freq = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1
    entropy = 0.0
    for count in freq.values():
        p = count / length
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def extract_features(file_path: str) -> list:
    """Read a file and return an 8-element feature vector."""
    with open(file_path, 'rb') as f:
        data = f.read()

    if not data:
        return [0, 0, 0, 0, 0, 0, 0, 0]

    byte_arr = np.frombuffer(data, dtype=np.uint8)
    file_size = len(data)
    entropy = _shannon_entropy(data)
    byte_mean = float(np.mean(byte_arr))
    byte_std = float(np.std(byte_arr))

    printable_set = set(string.printable.encode('ascii'))
    printable_count = sum(1 for b in data if b in printable_set)
    printable_ratio = printable_count / file_size

    null_count = data.count(b'\x00')
    null_ratio = null_count / file_size

    high_byte_count = sum(1 for b in byte_arr if b > 127)
    high_byte_ratio = high_byte_count / file_size

    unique_bytes = len(set(byte_arr.tolist()))
    unique_byte_ratio = unique_bytes / 256.0

    return [
        file_size,
        entropy,
        byte_mean,
        byte_std,
        printable_ratio,
        null_ratio,
        high_byte_ratio,
        unique_byte_ratio,
    ]


# ------------------------------------------------------------------
# Model training (synthetic data representing benign / malicious
# statistical profiles)
# ------------------------------------------------------------------

def _train_model() -> RandomForestClassifier:
    """
    Train on synthetic feature vectors.

    Benign files (label 0) – text, images, PDFs:
      - moderate entropy (3-5)
      - high printable ratio for text; moderate for images/PDFs
      - low null ratio

    Malicious files (label 1) – obfuscated payloads, packed binaries:
      - high entropy (6-8)
      - low printable ratio
      - high ratio of non-ASCII / high bytes
      - many unique byte values
    """
    rng = np.random.RandomState(42)
    n_benign = 500
    n_malicious = 500

    # ---------- benign samples ----------
    benign_size = rng.uniform(100, 500_000, n_benign)
    benign_entropy = rng.uniform(2.0, 5.5, n_benign)
    benign_mean = rng.uniform(40, 120, n_benign)
    benign_std = rng.uniform(10, 60, n_benign)
    benign_printable = rng.uniform(0.55, 0.98, n_benign)
    benign_null = rng.uniform(0.0, 0.05, n_benign)
    benign_high = rng.uniform(0.0, 0.25, n_benign)
    benign_unique = rng.uniform(0.1, 0.55, n_benign)

    X_benign = np.column_stack([
        benign_size, benign_entropy, benign_mean, benign_std,
        benign_printable, benign_null, benign_high, benign_unique,
    ])

    # ---------- malicious samples ----------
    mal_size = rng.uniform(500, 2_000_000, n_malicious)
    mal_entropy = rng.uniform(5.8, 7.99, n_malicious)
    mal_mean = rng.uniform(100, 200, n_malicious)
    mal_std = rng.uniform(50, 90, n_malicious)
    mal_printable = rng.uniform(0.05, 0.50, n_malicious)
    mal_null = rng.uniform(0.03, 0.30, n_malicious)
    mal_high = rng.uniform(0.30, 0.70, n_malicious)
    mal_unique = rng.uniform(0.60, 1.0, n_malicious)

    X_malicious = np.column_stack([
        mal_size, mal_entropy, mal_mean, mal_std,
        mal_printable, mal_null, mal_high, mal_unique,
    ])

    X = np.vstack([X_benign, X_malicious])
    y = np.array([0] * n_benign + [1] * n_malicious)

    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
    )
    clf.fit(X, y)
    return clf


def _get_model() -> RandomForestClassifier:
    """Load persisted model or train a new one."""
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)

    clf = _train_model()
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(clf, f)
    return clf


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------

BLOCKED_EXTENSIONS = {'.exe', '.bat', '.js'}
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.pdf', '.txt'}


def scan_file(file_path: str, original_filename: str = '') -> dict:
    """
    Scan a file and return a result dict:
        {
            'is_malicious': bool,
            'confidence': float,      # 0.0 – 1.0
            'threat_type': str,
            'severity': str,
            'details': str,
        }
    """
    ext = os.path.splitext(original_filename or file_path)[1].lower()

    # --- hard block on dangerous extensions ---
    if ext in BLOCKED_EXTENSIONS:
        return {
            'is_malicious': True,
            'confidence': 1.0,
            'threat_type': 'Blocked File Type',
            'severity': 'CRITICAL',
            'details': (
                f'File extension "{ext}" is blocked. '
                'Executable and script files are not permitted.'
            ),
        }

    # --- ML-based analysis ---
    try:
        features = extract_features(file_path)
        clf = _get_model()

        prediction = clf.predict([features])[0]
        probabilities = clf.predict_proba([features])[0]
        malicious_prob = float(probabilities[1])

        if prediction == 1 and malicious_prob >= 0.65:
            severity = 'CRITICAL' if malicious_prob >= 0.90 else (
                'HIGH' if malicious_prob >= 0.75 else 'MEDIUM'
            )
            return {
                'is_malicious': True,
                'confidence': malicious_prob,
                'threat_type': 'Suspicious Byte Pattern',
                'severity': severity,
                'details': (
                    f'AI analysis detected malicious patterns with '
                    f'{malicious_prob:.1%} confidence. '
                    f'Entropy: {features[1]:.2f}, '
                    f'Printable ratio: {features[4]:.2%}, '
                    f'High-byte ratio: {features[6]:.2%}, '
                    f'Unique-byte ratio: {features[7]:.2%}.'
                ),
            }

        return {
            'is_malicious': False,
            'confidence': 1.0 - malicious_prob,
            'threat_type': '',
            'severity': 'LOW',
            'details': (
                f'File appears clean ({1.0 - malicious_prob:.1%} safe). '
                f'Entropy: {features[1]:.2f}, '
                f'Printable ratio: {features[4]:.2%}.'
            ),
        }

    except Exception as exc:
        return {
            'is_malicious': False,
            'confidence': 0.0,
            'threat_type': 'Scan Error',
            'severity': 'LOW',
            'details': f'Error during scan: {str(exc)}',
        }
