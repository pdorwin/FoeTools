# Initial Repo layout

foe-tools/
│
├── .gitignore
├── README.md
├── LICENSE
│
├── python_tools/
│   ├── requirements.txt
│   └── overprime_calculator/
│       ├── __init__.py
│       ├── calculator.py
│       └── test_calculator.py
│
└── docs/                      <-- This will be your website root
    ├── index.html             <-- Landing page (links to all tools)
    ├── assets/
    │   ├── css/
    │   └── js/
    └── overprime/             <-- OverPrime web tool folder
        ├── index.html
        ├── overprime.css
        └── overprime.js

# Web hosting

## How to turn on hosting once your files are pushed:

- Go to your repository on GitHub.
  - Click on Settings (the gear icon at the top).

  - On the left sidebar, click on Pages.

    - Under Build and deployment -> Source, leave it as "Deploy from a branch".

    - Under Branch, select your branch (usually main), and change the folder dropdown from / (root) to /docs.

  - Click Save.

Within a minute or two, GitHub will give you a live URL (usually https://your-username.github.io/foe-tools/).

## Kickstart the deployment

git commit --allow-empty -m "Trigger GitHub Pages build"
git push origin main
