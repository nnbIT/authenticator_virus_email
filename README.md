# authenticator_virus_email
I’m trying to create a program that can estimate the probability (in %) that an email containing links or documents might be a virus or malware.


## STRUCTURE V.0.1
authenticator_virus_email/
│
├── main.py
├── routers/
│     ├── url_scanner.py
│     ├── file_scanner.py
│     └── email_scanner.py
│
├── utils/
│     ├── analyzer.py   (risk scoring logic)
│     └── validators.py (input validation)
│
└── models/
      └── models.py (optional)

