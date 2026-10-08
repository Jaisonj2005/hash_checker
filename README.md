# File Integrity Hash Checker 🛡️

A Python-based cryptographic utility designed for Security Operations Center (SOC) analysts to verify file integrity and generate signatures for malware triage.

**Features:**
* Utilizes Python's `hashlib` to concurrently generate MD5, SHA-1, and SHA-256 cryptographic hashes from a single target file.
* Employs memory-safe chunking (8KB blocks) to process massive files (e.g., ISOs, memory dumps) without exhausting system RAM.
* Includes a real-time comparison engine to instantly validate a generated hash against an expected vendor signature or an Indicator of Compromise (IoC).
* Multi-threaded architecture ensures the Tkinter GUI remains fully responsive during heavy cryptographic computations.

*Built as Day 23 of a 30-Day Network Engineering & Security portfolio streak.*
