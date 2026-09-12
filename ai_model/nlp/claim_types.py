"""Claim type definitions for claim extraction.

Defines the categories into which sentences can be classified:
- checkable_claim: Potentially verifiable factual statement
- opinion: Personal evaluation or belief
- question: Request for information
- instruction: Directive or command
- general_statement: Neutral factual assertion without strong markers
"""

from enum import Enum


class ClaimType(Enum):
    """Enumeration of possible claim types."""

    CHECKABLE_CLAIM = "checkable_claim"
    OPINION = "opinion"
    QUESTION = "question"
    INSTRUCTION = "instruction"
    GENERAL_STATEMENT = "general_statement"