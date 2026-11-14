# Django Car Showroom

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)

"Car World" is a car showroom web app built with Django. Visitors browse cars, filter them by brand and leave comments. Registered users can buy a car and see their purchases on their profile page. The project demonstrates user authentication (registration, login, profile editing, password change), class-based `DetailView`s, slug-based filtering, image uploads with `ImageField`, and many-to-many relationships between users and products.

This repository also contains two smaller practice projects (see [Practice projects](#practice-projects)).

## Features

- **Catalogue**: the home page lists all cars with image, model, price and brand. Brand buttons filter the list (`/brand/<slug>/`).
- **Car details**: a detail page shows the car's image, price and remaining stock, with a comment section. Any visitor can post a comment (name, email, message).
- **Buying**: logged-in users see a "Buy Now" button. Buying lowers the stock by one and records the user as a buyer.
- **Authentication**: registration (with first name, last name and email), login, logout, profile editing and password change, with success messages
- **Profile**: lists the cars the user has bought
- **Admin**: brands (slug auto-filled from the name) and cars are managed in the Django admin

## Practice projects

| Folder | Apps | What it covers |
| --- | --- | --- |
| `practice-18.5/practice_auth` | `user_profile` | Authentication on its own: registration with `UserCreationForm`, a custom `LoginView`, logout, profile editing, and password change with both `PasswordChangeForm` (requires the old password) and `SetPasswordForm` (does not) |
| `practice-19.5/musicians_directory` | `musician`, `album`, `user_profile` | A musicians and albums directory with authentication added; album views rewritten as class-based views protected by `LoginRequiredMixin`, musician view protected by `login_required` |

## Tech stack

| | |
| --- | --- |
| Language | Python 3.10+ |
| Framework | Django 5.0 |
| Database | SQLite |
| Forms | django-crispy-forms with crispy-bootstrap5 |
| Images | Pillow (`ImageField` for car photos) |
| Front end | Django templates, Bootstrap 5.3 (CDN) |

## Project structure

```
django-car-showroom/
├── requirements.txt
├── mid-term/
│   └── car_world/
│       ├── manage.py
│       ├── car_world/      # settings, root URLconf, home view with brand filter
│       ├── brand/          # Brand model
│       ├── car/            # Car and Comment models, detail view, buying
│       ├── user_profile/   # registration, login, profile, password change
│       ├── static/         # site images
│       └── templates/      # base.html, home.html
├── practice-18.5/
│   └── practice_auth/
└── practice-19.5/
    └── musicians_directory/
```

## Getting started

```bash
git clone https://github.com/ratulhasan001/django-car-showroom.git
cd django-car-showroom

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cd mid-term/car_world
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000/. Add brands and cars (with images) in the admin at `/admin/`, then register a user through the site to buy cars. No environment variables are required.

To run a practice project, `cd` into its folder (for example `practice-18.5/practice_auth`) and run the same `migrate` and `runserver` commands.

## Author

Ratul Hasan · [ratulhasan.dev](https://ratulhasan.dev)
