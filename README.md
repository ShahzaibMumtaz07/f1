# F1

F1 (Formula One) is a Django REST project for visualizing data using a Orthographic map projection (globe).


## Installation

Clone the project and start installing requirements in a virtualenv

```bash
pip install requirements.txt
```

## Note
- Do not forget to create an .env file with a 'SECRET' variable before starting project.
- This project includes a dataset of F1 (1950-2020) in "media/csv/" folder.
Datasets for F1 can be downloaded from https://www.kaggle.com/rohanrao/formula-1-world-championship-1950-2020 upon updates.

## Usage
After activating your environment and installing requirements, use:
```bash
python manage.py runserver 0.0.0.0:8000
```
You can view the globe at link http://localhost:8000/api/world/

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
