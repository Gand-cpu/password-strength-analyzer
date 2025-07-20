#  Password Strength Analyzer (CLI)

Analyze the strength of your passwords with entropy estimation and improvement tips.

#Features
- Score passwords from 0 to 100
- Entropy estimation
- Suggests improvements
- Supports single and bulk analysis
- Detects common weak passwords

#Installation

```bash
pip install -r requirements.txt
```
# Usage
Single Password:
```bash
python password_analyzer.py --password "MyPass123!"
```
From File:
```bash
python password_analyzer.py --file passwords.txt
```
