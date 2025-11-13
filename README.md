api-divergence-static/
│
├── backend_code/         ← developer will place backend repo here during testing
│
├── swagger/              ← store openapi.json here
│   └── openapi.json
│
├── src/
│   ├── loader/
│   │    ├── load_swagger.py
│   │    ├── load_backend_code.py
│   │
│   ├── ai/
│   │    ├── predict_divergence.py
│   │    ├── generate_testcases.py
│   │
│   └── utils/
│        ├── file_reader.py
│        ├── git_utils.py
│
├── tests/
│   └── generated_tests.json
│
├── README.md
└── requirements.txt
