# Django Car Showroom

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)

One of my early Django projects, built in 2024 while I was learning the framework. It was my mid-term project.

"Car World" is a small car showroom site. Visitors browse cars, filter them by brand and leave comments. Registered users can buy a car and see their purchases on their profile page.

While building it I practised:

- user authentication: registration, login, logout, profile editing and password change
- class-based views (`DetailView`, `LoginView`) alongside function views
- slug-based URL filtering
- image uploads with `ImageField` and serving media files in development
- many-to-many relationships between users and products

This repository also contains two smaller practice projects (see [Practice projects](#practice-projects)).

## Features

- **Catalogue**: the home page lists all cars with image, model, price and brand. Brand buttons filter the list (`/brand/<slug>/`). Brands get a slug automatically if none is entered.
- **Car details**: a detail page shows the car's image, price and remaining stock, with a comment section. Any visitor can post a comment (name, email, message); logged-in users have their name and email filled in.
- **Buying**: logged-in users see a "Buy Now" button. Buying lowers the stock by one and records the user as a buyer. A car cannot be bought when it is out of stock, and each user can buy a given car once.
- **Authentication**: registration (with first name, last name and email), login, logout, profile editing and password change, with success and error messages
- **Profile**: lists the cars the user has bought
- **Admin**: brands (slug auto-filled from the name), cars and comments are managed in the Django admin

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
│       ├── media/          # uploaded car images (created on first upload, not in git)
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

Then open http://127.0.0.1:8000/. Add brands and cars (with images) in the admin at `/admin/`, then register a user through the site to buy cars. Uploaded images are stored in `mid-term/car_world/media/` and served by the development server while `DEBUG` is on.

No environment variables are required. For anything other than local use, set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` and `DJANGO_ALLOWED_HOSTS` (comma-separated).

## Running the tests

```bash
cd mid-term/car_world
python manage.py test
```

The tests cover the catalogue and brand filter, the car page and comments, buying (login required, POST only, stock checks), and the registration, login, logout, profile and password-change flows.

To run a practice project, `cd` into its folder (for example `practice-18.5/practice_auth`) and run the same `migrate` and `runserver` commands.

## Later improvements

The original mid-term version was tidied up later. Changes made then (main project only):

- Buying now requires a logged-in user and a POST request. Before, the buy link was a plain GET URL that also worked for anonymous visitors, and stock could drop below zero.
- Logging out now uses a POST request.
- Unknown brands and cars return a 404 page instead of a server error.
- `MEDIA_ROOT` was missing, so uploads were written relative to the current directory and image URLs did not resolve reliably. Uploads now go to `media/cars/` (migration `0005`). The old sample uploads in `car/media/images/` are no longer used.
- Posting a comment now redirects back to the page (no duplicate comment on refresh) and shows form errors when the input is invalid.
- Login now respects the `?next=` parameter, and failed logins show an error rather than a success message.
- Fixed duplicate HTML ids on the registration form.
- Messages are shown on every page, not only the home page. Added page titles, an active navbar link, a footer, empty states and an out-of-stock badge; profile cards link to the car page.
- The template directory is resolved from the project folder, and `SECRET_KEY`, `DEBUG` and `ALLOWED_HOSTS` can be set through environment variables.
- Added a test suite.

## Author

Ratul Hasan · [ratulhasan.dev](https://ratulhasan.dev)
