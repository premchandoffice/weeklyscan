#!/usr/bin/env python3
"""
===========================================================
AI-Powered Enterprise SBOM & CBOM Report Generator
===========================================================

Author  : Premchand
Version : 1.0.0

Description:
------------
Reads CycloneDX SBOM and CBOM JSON files, sends them to
Claude for analysis, and generates enterprise-grade
security and compliance reports.

Future Outputs
--------------
- Markdown Report
- HTML Report
- PDF Report
- GitHub Step Summary

"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

import anthropic
# ==========================================================
# Configuration
# ==========================================================

CLAUDE_MODEL = "claude-sonnet-4-20250514"

MAX_TOKENS = 12000

TEMPERATURE = 0

API_KEY_ENV = "CLAUDE_API_KEY"

LOG_LEVEL = logging.INFO
# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)

logger = logging.getLogger("report-generator")
# ==========================================================
# CLI
# ==========================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Enterprise SBOM & CBOM Report Generator"
    )

    parser.add_argument(
        "--sbom",
        required=True,
        help="Path to SBOM JSON",
    )

    parser.add_argument(
        "--cbom",
        required=True,
        help="Path to CBOM JSON",
    )

    parser.add_argument(
        "--repo",
        required=True,
        help="Repository Name",
    )

    return parser.parse_args()
  # ==========================================================
# JSON Loader
# ==========================================================

def load_json(path: str):

    file = Path(path)

    if not file.exists():
        logger.error("File not found: %s", file)
        sys.exit(1)

    logger.info("Loading %s", file)

    try:

        with open(file, "r", encoding="utf-8") as f:

            return json.load(f)

    except json.JSONDecodeError as e:

        logger.exception("Invalid JSON")

        raise e
# ==========================================================
# Validation
# ==========================================================

def validate_sbom(sbom):

    logger.info("Validating SBOM...")

    if sbom.get("bomFormat") != "CycloneDX":
        raise ValueError("Invalid SBOM")

    logger.info("SBOM OK")


def validate_cbom(cbom):

    logger.info("Validating CBOM...")

    if cbom.get("bomFormat") != "CycloneDX":
        raise ValueError("Invalid CBOM")

    logger.info("CBOM OK")
# ==========================================================
# Claude Client
# ==========================================================

def get_claude_client():

    api_key = os.getenv(API_KEY_ENV)

    if not api_key:

        logger.error(
            "Environment variable %s not found",
            API_KEY_ENV,
        )

        sys.exit(1)

    logger.info("Claude API Key Found")

    return anthropic.Anthropic(
        api_key=api_key
    )
# ==========================================================
# Output Directory
# ==========================================================

def create_output_directories():

    Path("reports/SBOM").mkdir(
        parents=True,
        exist_ok=True,
    )

    Path("reports/CBOM").mkdir(
        parents=True,
        exist_ok=True,
    )

    logger.info("Output directories ready")
# ==========================================================
# Main
# ==========================================================

def main():

    args = parse_arguments()

    logger.info("=" * 60)
    logger.info("Enterprise Report Generator")
    logger.info("=" * 60)

    create_output_directories()

    sbom = load_json(args.sbom)

    cbom = load_json(args.cbom)

    validate_sbom(sbom)

    validate_cbom(cbom)

    client = get_claude_client()

    logger.info("Repository : %s", args.repo)

    logger.info("SBOM Loaded")

    logger.info("CBOM Loaded")

    logger.info("Claude Connected")

    logger.info("Ready for Prompt Generation")


if __name__ == "__main__":

    main()
