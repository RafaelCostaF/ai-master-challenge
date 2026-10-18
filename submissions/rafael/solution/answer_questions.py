"""CLI: answers the four Challenge 004 questions and writes a Markdown report.

Usage (from submissions/rafael): .venv/bin/python solution/answer_questions.py [--out docs/respostas.md]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from social_insights import data, questions  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Markdown file to write (prints to stdout if omitted)")
    args = parser.parse_args()

    df = data.load_posts()
    report = "# Respostas — Challenge 004\n\n" + "\n\n---\n\n".join(a.to_markdown() for a in questions.answer_all(df))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"Relatório salvo em {args.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
