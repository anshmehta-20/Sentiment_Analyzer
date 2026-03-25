import argparse
import re
from pathlib import Path

import pandas as pd

from path_utils import output_file


CONSTRUCT_SEEDS = {
    "Actuation": [
        "autonomous",
        "triggering",
        "executing",
        "responding",
        "scheduling",
        "commanding",
        "regulating",
        "switching",
        "directing",
        "controlling",
    ],
    "Awareness": [
        "sensing",
        "detecting",
        "monitoring",
        "scanning",
        "tracking",
        "recognizing",
        "notifying",
        "capturing",
        "observing",
        "measuring",
    ],
    "Connectivity": [
        "synchronizing",
        "pairing",
        "linking",
        "networking",
        "communicating",
        "interfacing",
        "sharing",
        "integrating",
        "streaming",
        "transmitting",
    ],
    "Dynamism": [
        "adapting",
        "learning",
        "updating",
        "optimizing",
        "personalizing",
        "configuring",
        "evolving",
        "adjusting",
        "upgrading",
        "calibrating",
    ],
    "Novelty": [
        "innovative",
        "unique",
        "stylish",
        "original",
        "creative",
        "trendsetting",
        "experimental",
        "disruptive",
        "cutting edge",
        "eye catching",
    ],
    "Personality": [
        "expressive",
        "playful",
        "conversational",
        "empathetic",
        "relatable",
        "friendly",
        "humorous",
        "motivating",
        "intuitive",
        "social",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate construct scores from a text column."
    )
    parser.add_argument("--input", required=True, help="Path to an input CSV or Excel file.")
    parser.add_argument(
        "--text-column",
        required=True,
        help="Name of the column that contains raw text.",
    )
    parser.add_argument(
        "--output",
        help="Optional path for the scored output file. Defaults to outputs/<input_stem>_scored.xlsx",
    )
    return parser.parse_args()


def load_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError("Unsupported input format. Use CSV or Excel.")


def save_table(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".csv":
        df.to_csv(path, index=False)
        return
    if path.suffix.lower() in {".xlsx", ".xls"}:
        df.to_excel(path, index=False)
        return
    raise ValueError("Unsupported output format. Use CSV or Excel.")


def normalize_text(text: object) -> str:
    cleaned = re.sub(r"[^a-z0-9\s]", " ", str(text).lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def keyword_count(text: str, keyword: str) -> int:
    pattern = r"\b" + re.escape(keyword.lower()).replace(r"\ ", r"\s+") + r"\b"
    return len(re.findall(pattern, text))


def score_text(text: object) -> dict[str, object]:
    normalized_text = normalize_text(text)
    token_count = max(len(normalized_text.split()), 1)

    raw_scores = {}
    normalized_scores = {}

    for construct, keywords in CONSTRUCT_SEEDS.items():
        hits = sum(keyword_count(normalized_text, keyword) for keyword in keywords)
        raw_scores[construct] = hits
        normalized_scores[f"{construct}_Score"] = round(hits / token_count, 4)

    best_construct = max(raw_scores, key=raw_scores.get)
    if raw_scores[best_construct] == 0:
        best_construct = "Unknown"

    return {
        **normalized_scores,
        "most_similar_characteristic": best_construct,
    }


def default_output_path(input_path: Path) -> Path:
    return output_file(f"{input_path.stem}_scored.xlsx")


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else default_output_path(input_path)

    df = load_table(input_path)

    if args.text_column not in df.columns:
        raise KeyError(
            f"Column '{args.text_column}' was not found. Available columns: {list(df.columns)}"
        )

    scored_df = df.copy()
    construct_df = scored_df[args.text_column].fillna("").apply(score_text).apply(pd.Series)
    scored_df = pd.concat([scored_df, construct_df], axis=1)

    save_table(scored_df, output_path)
    print(f"Construct scores saved to: {output_path}")


if __name__ == "__main__":
    main()
