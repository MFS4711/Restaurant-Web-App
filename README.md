# Cedar & Flame
<!-- Maybe create a header with html and css and use screenshot  -->

A Restaurant Web-App created using Django

Source code can be found [here](https://github.com/MFS4711/Restaurant-Web-App)

The live project can be viewed [here](Add link)

---

## Table of Contents

[**Purpose of Project**](#purpose-of-project)

[**Features**](#features)
- [All Users](#all-users)
- [Authenticated (Logged in) Users](#authenticated-logged-in-users)
- [Staff (Authenticated)](#staff-authenticated)
- [Future Features](#future-features)

[**User Experience**](#User-Experience)
- [Design](#design)
    - [Fonts](#fonts)
    - [Colour](#colour)
    - [Wireframes](#wireframes)

[**Development Process**](#development-process)
- [Project Planning](#project-planning-and-documentation-using-gitHub)
- [Search Engine Optimization](#search-engine-optimization)
- [Data Model](#data-model)
- [Data Validation](#data-validation)

[**Testing**](#Testing)
- [Manual Testing](#manual-testing)
    - [Feature Testing](#feature-testing)
    - [Responsiveness](#responsiveness)
    - [Lighthouse](#lighthouse)
- [Validation Testing](#validation-testing)
- [User Story Testing](#user-story-testing)
- [Automated Testing](#automated-testing)
    - [Django testing](#testing-django-views-models-and-forms)

[**Bugs**](#Bugs)

[**Libraries and Programs Used**](#libraries-and-programs-used)

[**Deployment**](#Deployment)
- [Making a Local Clone](#making-a-local-clone)
- [Running in Local Environment](#running-in-local-environment)
- [Deploying to Heroku](#deploying-to-heroku)

[**Credits**](#credits)

[**Acknowledgements**](#acknowledgements)

---

# Purpose of Project

The Restaurant Web App is designed to streamline the management of reservations, menu items, and restaurant operations. It aims to enhance the dining experience for customers by providing an intuitive platform for booking tables, while simplifying restaurant tasks for staff and administrators. The app is built to improve efficiency, reduce errors, and foster better communication between customers, staff, and management, ultimately creating a smoother, more enjoyable restaurant experience.

The primary users of the Restaurant Web App are customers, staff, and restaurant administrators. Customers use the platform to easily manage their reservations, browse menu items, and track their reservation status. Staff members interact with the app to manage and update reservations, ensure menu items are available, and assist with operational tasks. Administrators and managers utilise the app to oversee operations and analyse restaurant performance. Each group is provided with tailored functionality based on their role to ensure smooth and efficient restaurant operations.

<!-- Paragraph may change based on functionality achieved at the end -->

<!-- Photo from responsiveness website - check file path -->
![responsivenes_screenshot](/static/doc_images/responsiveness_screenshot.png)

---

[Return to top](#cedar--flame)

# Features

This section outlines the key features available to different types of users within the project. It describes pages and functionalities accessible to all users, authenticated users, and staff, highlighting the significance of each feature. Additionally, it includes a look at potential future features that could further enhance the user experience.

## All Users
The following pages are visible to all users, logged in or not.

<!-- Create dropdowns for different sections following below format -->
<details>
<summary>Homepage (landing page)</summary>

- The landing page presents the user with a choice of ... actions:
    <!-- List actions -->
- The page has a header which has the following elements, from left to right:
    - Site icon, clickable, which links from any page back to this one.
    <!-- Add further elements in nav/header -->
    <!-- give element name and type - description of action when clicked -->
    <!-- Bullet point of any features to note from homepage and describe significance -->
    - The page footer, common to all pages, consists of ...

<!-- Add screenshot of welcome page - maybe different screenshots for different devices -->
![Welcome Page](static/doc_images/feature_screenshots/feature_welcome.png)

</details>

<!-- Any other pages that are visible to all users using same format -->
<details>
<summary>... Page</summary>
<!-- List features and describe significance -->

![... Page](static/doc_images/feature_screenshots/SOME_IMAGE)

</details>

<!-- Repeat for all Pages visible to all users -->

<!-- Below for login and register pages -->
<details>
<summary>Login Page</summary>

![Login Page](static/doc_images/feature_screenshots/feature_login.png)

- This is the standard allauth login page, styled with the site styling, and including social login links for Google and Facebook.

</details>

<details>
<summary>Register Page</summary>

![Register Page](static/doc_images/feature_screenshots/feature_register.png)

- This is the standard allauth signup page, with fields for email, username, and password + password confirmation. All fields are required.

</details>

## Authenticated (Logged in) Users
The following pages are only available to logged in users.

<details>
<summary>... Page</summary>
<!-- List features and describe significance -->

![... Page](static/doc_images/feature_screenshots/SOME_IMAGE)

</details>

<!-- Similar to previous just repeat for each page unique to this user -->

## Staff (Authenticated)
The remaining pages are only accessible to staff
<details>
<summary>... Page</summary>
<!-- List features and describe significance -->

![... Page](static/doc_images/feature_screenshots/SOME_IMAGE)

</details>

<!-- Similar to previous just repeat for each page unique to this staff -->
<!-- Add any other sections for other roles -->

## Future Features
<!-- Bullet point any features that could be added and describe benefit -->
- It would be useful for (user type) to be able to ... This will ... etc
- A feature with added benefit for (user type) would be ...
- Another future feature, which I coonsidered implementing, is ...

---

[Return to top](#cedar--flame)

# User Experience

This section details the key elements of the user experience (UX) design for the project, including visual design choices, color schemes, typography, and wireframes. It provides insight into the aesthetic and functional decisions made to enhance usability across different devices, ensuring a seamless and accessible experience for users.

## Design

### Fonts
<!-- description in style below -->
The Montserrat font was used throughout the project for headings and prominent text. It's a clean, modern sans-serif font with a strong, professional look, making it ideal for a refined restaurant like Cedar and Flame. Its bold, uppercase styling helps convey a sense of sophistication and presence.

For body text, Open Sans was chosen due to its simplicity and high legibility, providing a comfortable reading experience for users. Its versatility and neutral design make it well-suited for longer content while maintaining a polished, cohesive aesthetic across the site.

### Colour
The following colour palette was used in the project:

![colour_palette](/readme_images/colours/cedar_and_flame_colour_palette.png)

- **#F5F5F5 (White Smoke)**: Used for body text to ensure readability on dark backgrounds, enhancing clarity for customers browsing the menu and staff interacting with data.
- **#FFD700 (Gold)**: Highlights important elements like headings and buttons. Gold conveys prestige and grabs attention, guiding users toward key actions like making reservations or submitting forms.
- **#333333 (Jet)**: Applied to buttons and navigation for contrast, ensuring that call-to-action elements are clear but not overwhelming, suitable for both customers and staff.
- **#444444 (Onyx)**: Used for card and form backgrounds to keep the design clean and focused, making menu items and forms stand out in a professional and minimalistic way.
- **#212121 (Eerie Black)**: Used for the footer to separate it from the main content and keep less central information accessible without distraction.

#### _Colour Contrast (Font against Background)_

<details>
<summary>#F5F5F5 (White Smoke) and #333333 (Jet)</summary>

![contrast-white_smoke-jet](/readme_images/colours/contrast-white_smoke-jet.png)

</details>

<details>
<summary>#F5F5F5 (White Smoke) and #444444 (Onyx)</summary>

![contrast-white_smoke-onyx](/readme_images/colours/contrast-white_smoke-onyx.png)

</details>

<details>
<summary>#F5F5F5 (White Smoke) and #212121 (Eerie Black)</summary>

![contrast-white_smoke-eerie_black](/readme_images/colours/contrast-white_smoke-eerie_black.png)

</details>

<details>
<summary>#FFD700 (Gold) and #333333 (Jet)</summary>

![contrast-gold-jet](/readme_images/colours/contrast-gold-jet.png)

</details>

<details>
<summary>#FFD700 (Gold) and #444444 (Onyx)</summary>

![contrast-gold-onyx](/readme_images/colours/contrast-gold-onyx.png)

</details>

<details>
<summary>#FFD700 (Gold) and #212121 (Eerie Black)</summary>

![contrast-gold-eerie_black](/readme_images/colours/contrast-gold-eerie_black.png)

</details>

### Wireframes
These wireframes outline how each page was intended to be displayed on Mobile, Tablet, Desktops and Larger Screens. Generally speaking, the layout is very similar across all viewports, the only difference being the additional space being taken advantage of.

#### _Homepage (Landing Page)_

<details>
<summary>Mobile</summary>

![homepage-mobile wireframe](/readme_images/wireframes/homepage-mobile.png)

</details>

<details>
<summary>Tablet</summary>

![homepage-tablet wireframe](/readme_images/wireframes/homepage-tablet.png)

</details>

<details>
<summary>Desktop</summary>

![homepage-desktop wireframe](/readme_images/wireframes/homepage-desktop.png)

</details>

#### _Menu Page_

<details>
<summary>Mobile</summary>


![menu-mobile wireframe](/readme_images/wireframes/menu-mobile.png)

</details>

<details>
<summary>Tablet</summary>

![menu-tablet wireframe](/readme_images/wireframes/menu-tablet.png)

</details>

<details>
<summary>Desktop</summary>

![menu-desktop wireframe](/readme_images/wireframes/menu-desktop.png)

</details>

#### _Booking Page_

<details>
<summary>Mobile</summary>

![booking-mobile wireframe](/readme_images/wireframes/booking-mobile.png)

</details>

<details>
<summary>Tablet</summary>

![booking-tablet wireframe](/readme_images/wireframes/booking-tablet.png)

</details>

<details>
<summary>Desktop</summary>

![booking-desktop wireframe](/readme_images/wireframes/booking-desktop.png)

</details>

#### _Contact Page_

<details>
<summary>Mobile</summary>

![contact-mobile wireframe](/readme_images/wireframes/contact-mobile.png)

</details>

<details>
<summary>Tablet</summary>

![contact-tablet wireframe](/readme_images/wireframes/contact-tablet.png)

</details>

<details>
<summary>Desktop</summary>

![contact-desktop wireframe](/readme_images/wireframes/contact-desktop.png)

</details>

#### _Customer Dashboard_

<details>
<summary>Mobile</summary>

![welcome_page wireframe](/readme_images/wireframes/customer_dashboard-mobile.png)

</details>

<details>
<summary>Tablet</summary>

![welcome_page wireframe](/readme_images/wireframes/customer_dashboard-tablet.png)

</details>

<details>
<summary>Desktop</summary>

![welcome_page wireframe](/readme_images/wireframes/customer_dashboard-desktop.png)

</details>

#### _Staff Dashboard_

<details>
<summary>Mobile</summary>

![staff_dashboard-mobile wireframe](/readme_images/wireframes/staff_dashboard-mobile.png)

</details>

<details>
<summary>Tablet</summary>

![staff_dashboard-tablet wireframe](/readme_images/wireframes/staff_dashboard-tablet.png)

</details>

<details>
<summary>Desktop</summary>

![staff_dashboard-desktop wireframe](/readme_images/wireframes/staff_dashboard-desktop.png)

</details>

#### _Admin Dashboard_

<details>
<summary>Mobile</summary>

![admin_dashboard-mobile wireframe](/readme_images/wireframes/admin_dashboard-mobile.png)

</details>

<details>
<summary>Tablet</summary>

![admin_dashboard-tablet wireframe](/readme_images/wireframes/admin_dashboard-tablet.png)

</details>

<details>
<summary>Desktop</summary>

![admin_dashboard-desktop wireframe](/readme_images/wireframes/admin_dashboard-desktop.png)

</details>

<!-- Maybe add login/out/register/404 page -->

---

[Return to top](#cedar--flame)

# Development Process

The development process for this project was carefully planned and documented to ensure efficient progress and transparency. This section outlines how the project was broken down into manageable tasks, tracked, and prioritized using GitHub Issues and Projects. It also covers the key steps taken, including project planning, SEO, data modeling, and data validation. Each sub-section provides a detailed look at the tools and methods used to guide development from initial planning to implementation.

## Project Planning and Documentation Using GitHub
GitHub Issues were used to document the development steps undertaken in the project. 
Two issue templates were created: one for [User Epics](https://github.com/MFS4711/Restaurant-Web-App/issues/new?assignees=&labels=&projects=&template=user-epic.md&title=USER+EPIC+%3A+%3CTITLE%3E) and another for [User Stories](https://github.com/MFS4711/Restaurant-Web-App/issues/new?assignees=&labels=&projects=&template=user-story.md&title=USER+STORY+%3A+%3CTITLE%3E).
A variety of labels were applied to categorise issue types, such as Bugs, User Epics and User Stories, with the parent epic and child story being associated with the same label for easy identificaion.
MoSCoW prioritisation was applied using the labels must-have, should-have, and could-have.

The project was broken down into manageable sprints using GitHub Projects, which provided a Kanban board. Issues were posted to the board and moved from "Todo" to "In Progress" to "Done" as they were completed.

The iterations are documented here :
    - [Prerequisites](https://github.com/users/MFS4711/projects/6/views/1)
    - [Iteration 1](https://github.com/users/MFS4711/projects/5)
    - [Iteration 2](link)
    - ...

The User Epics and their related User Stories are as follows:
- Epic : [Set up User Authentication with Django Allauth](https://github.com/MFS4711/Restaurant-Web-App/issues/1)
    - Story : [Implement Email Verification for New Users](https://github.com/MFS4711/Restaurant-Web-App/issues/2)
    - Story : [Configure User Roles (Customer, Staff, Admin](https://github.com/MFS4711/Restaurant-Web-App/issues/3)
    - Story : [Implement Email Verification for New Users](https://github.com/MFS4711/Restaurant-Web-App/issues/4)
- Epic : [Implement Booking Management System](https://github.com/MFS4711/Restaurant-Web-App/issues/5)
    - Story : [Allow Customers to Create, View, and Cancel Bookings](https://github.com/MFS4711/Restaurant-Web-App/issues/6)
    - Story : [Allow Staff to View, Approve, and Reject Bookings](https://github.com/MFS4711/Restaurant-Web-App/issues/7)
    - Story : [Prevent Double Bookings by Validating Date/Time](https://github.com/MFS4711/Restaurant-Web-App/issues/8)
- Epic : [Implement Menu Display System](https://github.com/MFS4711/Restaurant-Web-App/issues/9)
    - Story : [Display Menu Items](https://github.com/MFS4711/Restaurant-Web-App/issues/10)
    - Story : [Add Dietary Tags to Menu Items](https://github.com/MFS4711/Restaurant-Web-App/issues/11)
- Epic : [Implement Table Assignment and Availability Management](https://github.com/MFS4711/Restaurant-Web-App/issues/12)
    - Story : [Allow Staff to Assign Bookings to Tables](https://github.com/MFS4711/Restaurant-Web-App/issues/13)
    - Story : [Automatically Mark Tables as Occupied When Assigned to a Booking](https://github.com/MFS4711/Restaurant-Web-App/issues/14)
    - Story : [Automatically Make Tables Available After Booking Ends](https://github.com/MFS4711/Restaurant-Web-App/issues/15)
    - Story : [Prevent Double Booking of the Same Table](https://github.com/MFS4711/Restaurant-Web-App/issues/16)
    - Story : [Display Available Tables in Staff Dashboard](https://github.com/MFS4711/Restaurant-Web-App/issues/17)
    - Story : [Allow Admin to Manage Table Configurations](https://github.com/MFS4711/Restaurant-Web-App/issues/18)
- Epic : [Implement Customer Order Management System](https://github.com/MFS4711/Restaurant-Web-App/issues/19)
    - Story : [Allow Customers to Add Menu Items to Order](https://github.com/MFS4711/Restaurant-Web-App/issues/20)
    - Story : [Allow Customers to Modify Their Orders](https://github.com/MFS4711/Restaurant-Web-App/issues/21)
    - Story : [Allow Customers to View Order Status](https://github.com/MFS4711/Restaurant-Web-App/issues/22)
    - Story : [Allow Customers to Apply Discount Codes to Orders](https://github.com/MFS4711/Restaurant-Web-App/issues/29)
    - Story : [Allow Customers to Add Special Instructions](https://github.com/MFS4711/Restaurant-Web-App/issues/30)
- Epic : [Implement Staff Order Management System](https://github.com/MFS4711/Restaurant-Web-App/issues/23)
    - Story : [Allow Staff to View and Approve Orders](https://github.com/MFS4711/Restaurant-Web-App/issues/24)
    - Story : [Allow Staff to Update Order Status](https://github.com/MFS4711/Restaurant-Web-App/issues/25)
    - Story : [Allow Staff to Leave Internal Notes on Orders](https://github.com/MFS4711/Restaurant-Web-App/issues/31)
- Epic : [Implement Menu Availability and Stock Management](https://github.com/MFS4711/Restaurant-Web-App/issues/26)
    - Story : [Allow Staff to Mark Menu Items as Out of Stock](https://github.com/MFS4711/Restaurant-Web-App/issues/27)
    - Story : [Allow Staff to Revert Items Back to Stock](https://github.com/MFS4711/Restaurant-Web-App/issues/28)
    - Story : [Allow Staff to Set Prices for Menu Items Dynamically](https://github.com/MFS4711/Restaurant-Web-App/issues/32)
- Epic : [Implement Real-Time Order Status Updates](https://github.com/MFS4711/Restaurant-Web-App/issues/33)
    - Story : [Implement Real-Time Order Status Updates via WebSockets](https://github.com/MFS4711/Restaurant-Web-App/issues/34)
    - Story : [Send SMS or Email Notifications for Order Status Updates](https://github.com/MFS4711/Restaurant-Web-App/issues/35)
- Epic : [Admin Can Manage Menu Items](https://github.com/MFS4711/Restaurant-Web-App/issues/40)
    - Story : [Admin Can Add New Menu Items](https://github.com/MFS4711/Restaurant-Web-App/issues/41)
    - Story : [Admin Can Modify Existing Menu Items](https://github.com/MFS4711/Restaurant-Web-App/issues/42)
    - Story : [Admin Can Remove Menu Items](https://github.com/MFS4711/Restaurant-Web-App/issues/43)

<!-- Include this section and add depth if time at the end -->
## Search Engine Optimization
A set of long and short tail keywords was developed. 
The initial set was generated from a combination of brainstorming and examining the related searches returned by Google for these terms. This was then culled back to a smaller set of more targeted short- and long-tail keywords, which were each trialled on [wordtracker.com](https://wordtracker.com). 
This resulted in the following list of terms, ordered by volume:

|Term|Short/long-tail|Volume|Competition|
|---|---|---|---|
|'Word'|Short|226000|55.44|

After completing this research, I returned to the project's templates, and made the following changes:

- &lt;title> tag in base.html:
    - Set to '....'. This is one of the most important SEO locations ...
<!-- Add any tags in same form and bullet point impact of change -->

## Data Model
This section provides an overview of the data models used in the project, represented through Entity-Relationship Diagrams (ERDs) for each application. Each sub-heading corresponds to a specific app, detailing its database schema and the relationships between key entities. These ERDs were drawn using [Lucidchart](https://www.lucidchart.com/pages/) and offer a clear visualization of how data is structured and flows within the application.

<!-- Add Apps and ERD Diagram for App -->

### ... App

![Entity-relationship diagram for ... App](docs/SOME_FILE_PATH)

### ... App

![Entity-relationship diagram for ... App](docs/SOME_FILE_PATH)

<!-- Repeat for each App -->

## Data Validation
<!-- List places where validators were used in model - i.e.price -->
<!-- If someone tries a negative number, error will occur and some action will happen - describe  -->
The following decimal fields, representing currency amounts, are protected by Django's MinValueValidator, with the minimum value being set at 0.

<!-- Also add any JS checks on form fields etc. to ensure desired action/errors are caught -->

---

[Return to top](#cedar--flame)

# Testing

The Testing section covers various strategies used to ensure the application's functionality and quality. This includes **manual testing** for hands-on verification, **validator testing** to check data integrity, **user story testing** to confirm features meet user requirements, and **automated testing** to streamline repeated tests and ensure consistent performance throughout development. Each approach contributes to a robust, error-free application.

## Manual Testing

### Feature Testing
The manual testing of features is organised by app below. Testing was carried out on a 1920 x 1080 desktop screen, a Samsung tablet and an Samsung S22 Ultra.
<!-- Amend devices as required for testing -->

<details>
<summary>... App</summary>
<!-- Example of how to layout table below -->
|Page|Feature|Action|Effect|
|---|---|---|---|
|/basket/view_basket/|All items appear in list|Add item to list in product_detail page|Item appears on table|
|/basket/view_basket/|Item quantities are correct|Add n items in product_detail page|n items appear on table|
</details>

<!-- Repeat for each app - make sure all buttons/forms/elements in general are tested - be thorough -->
<details>
<summary>... App</summary>
<!-- Example of how to layout table below -->
|Page|Feature|Action|Effect|
|---|---|---|---|
|/basket/view_basket/|All items appear in list|Add item to list in product_detail page|Item appears on table|
|/basket/view_basket/|Item quantities are correct|Add n items in product_detail page|n items appear on table|
</details>

### Responsiveness
All pages on the live site were tested with the default list of devices in Chrome Devtools.
<!-- Add any things to note of interst - i.e some acceptable compromise -->

### Lighthouse
The Lighthouse testing results are displayed by page below:

<details>
<summary>Lighthouse results by page</summary>

<!-- Add page as bullet point and lighthouse result screenshot - Performance, Accessibility and SEO - best practices -->

- Welcome Page (Landing Page)

![welcome_page_lighthouse](static/doc_images/lighthouse_reports/FILE_PATH)

<!-- Repeat for each page -->

- Another Page

![another_page_lighthouse](static/doc_images/lighthouse_reports/FILE_PATH)

</details>

## Validation Testing

<details>
<summary>Python Code</summary>

- All python code is validated by the [Flake8 linter](https://flake8.pycqa.org/en/latest/) (installed in VSCode) and [CI Python Linter](https://pep8ci.herokuapp.com/). The sole exceptions are the test classes, whose function names and implementation can be very verbose.

![Python Validation](SCREENSHOT_PATH)

</details>

<details>
<summary>JavaScript Code</summary>

- All JavaScript code is validated by the [ESLint](https://eslint.org/) (installed in VSCode) and [JS Hinterface](https://mfs4711.github.io/jshint-api/).

![JavaScript Validation](SCREENSHOT_PATH)

</details>

<details>
<summary>HTML Validation</summary>

- All HTML files were validated using the [W3C Markup Validation Service](https://validator.w3.org/)

![HTML Validation](SCREENSHOT_PATH)
</details>

<details>
<summary>CSS Validation</summary>

- All CSS files were validated using the [W3C Validation Service](https://jigsaw.w3.org/css-validator/)

![CSS Validation](SCREENSHOT_PATH)
</details>

## User Story Testing
The User Epics and Stories for this project are documented across ... GitHub Projects, each corresponding to a specific iteration of the development work. You can find them here:

- [Iteration 1](link)
- [Iteration 2](link)
- etc .

Alternitively, the Epics and Stories are individually linked here :

- [Epics and Stories](#development-process)

In both cases, the status of each issue will indicate whether the user story has been completed.

## Automated Testing

### Testing django views, models and forms
A full suite of automated tests is included in the project. The tests for each app are located in the `test/` folder within each respective app and can be run using the following command :

`python3 manage.py test`

The most recent coverage report is available in the `htmlcov/` folder at the project's root. To view it, you can serve the report locally by running Python's built-in HTTP server from the root folder :

`python3 -m http.server`

To generate the coverage HTML report, use the following commands:

`coverage run manage.py test`

`coverage html`

---

[Return to top](#cedar--flame)

# Bugs

This section provides an overview of the bugs encountered during development, along with their resolutions. Any remaining issues or notable fixes are also tracked for reference.

Several bugs encountered during development and their solutions are documented in the GitHub issues tracker. Some notable examples include:
- [BUG - Form not submitting without modifying image field](https://github.com/MFS4711/Restaurant-Web-App/issues/45)
- [ANOTHER BUG](GITHUB_ISSUE_LINK)
- etc.

## Remaining Bugs
There should (hopefully) be no remaining bugs in the project.

---

[Return to top](#cedar--flame)

# Libraries and Programs Used

This section highlights the key libraries, tools, and platforms utilised throughout the development of the project. These technologies played an essential role in various aspects of the project, from wireframing and version control to deployment and testing.

1. [Balsamiq](https://balsamiq.com/)
    - Balsamiq was used to wireframe all the pages in the project.
2. [Git](https://git-scm.com/)
    - Version control was implemented using Git through the GitHub terminal.
3. [Github](https://github.com/)
    - GitHub was used to store the project after being pushed from Git. The cloud service GitHub Pages was used to deploy the project on the web, while GitHub Projects tracked User Stories, Epics, bugs, and other issues throughout the development.
4. [Gitpod](https://www.gitpod.io/)
    - Gitpod was used as the primary IDE for development, with ESLint and Flake8 linters configured for JavaScript and Python code validation, respectively.
5. [Heroku](https://www.heroku.com/)
    - Heroku was used for deploying the project.
6. [pytest](https://docs.pytest.org/en/7.1.x/)
    - Pytest was used for automated testing of the project.

---

[Return to top](#cedar--flame)

# Deployment

This section provides a step-by-step guide for deploying your project to Heroku, ensuring that all necessary configurations and settings are in place for both development and production environments. Before deploying, you'll first clone the repository to your local machine to ensure that the original repo remains untouched during development. Follow these instructions to set up the app locally, deploy it to Heroku, and configure essential services like the database, social logins, and payment processing. By the end of this process, your app will be live and accessible on the web.

## Making a Local Clone
1. Open a terminal/command prompt on your local machine.
2. Navigate to the directory where you want to clone the project.
3. Run the following command to clone the repository :

    `git clone 'REPO_LINK'`

<!-- May need to refactor section as maybe arrange it to first confirm  -->
## Running in Local Environment
<!-- Add steps taken - packages installed to ensure local environment works -->
<!-- Maybe remove common steps from heroku section -->

## Deploying to Heroku
1. **Log into Heroku** and navigate to the Dashboard.
2. Click the **'New'** button.
3. Choose a **unique app name** and select the region relevant to you.
4. **Create a Database** - As a student at Code Institute, I used [CI Database Maker](https://dbs.ci-dbs.net/) but this can also be achieved on Heroku by paying a monthly fee and following the below steps:
<!-- Add steps to create database here - i.e. Procfile and relevant code etc -->

5. Go to the **Settings** tab, and click **Reveal Config Vars**. Add the following config variables, if not already present:
    - **Django secret key**
    - **Database URL**
    - **Cloudinary API**
    - etc
    <!-- List all config vars visible - not giving their values -->
6. In your **local repository**, add a **Procfile** to the root directory with this content:

    `web: gunicorn strings-attached.wsgi`

7. Add your Heroku app URL to the `ALLOWED_HOSTS` list in `settings.py`.
8. Create ... social apps for Facebook and Google login:
    - Add their API keys and Secrets to the database.
    - Configure your application details and callback URLs in the Google and Facebook OAuth dashboards.
    <!-- Amend this step based on if socials are used or not -->

9. Set `DEBUG` to `False` in `settings.py`, then commit and push your changes to GitHub.
10. Navigate to the **Deploy** tab in the Dashboard. Under **Deployment Method**, click the **GitHub** icon to connect your Heroku app to your GitHub repository.
    - Enter your repository name, click **Search**, then click **Connect**.
11. Under the **Manual Deploy** section, click **Deploy Branch**. Once deployed, you should see the message **"Your app was successfully deployed"**.
12. Click **Open App** to open the app in the browser.

---

[Return to top](#cedar--flame)

# Credits
<!-- Add any code credits and give links -->
<!-- Add any image credits -->
<!-- Add any specific research that was beneficial -->

- [Stack Overflow - How can I display a tuple field from a model to a template in Django?](https://stackoverflow.com/questions/67227949/how-can-i-display-a-tuple-field-from-a-model-to-a-template-in-django)
- [Learn how to use the forEach method in JS!](https://dev.to/ziratsu/learn-how-to-use-the-foreach-method-in-js-3im)
- [Manage images in a Django app](https://cloudinary.com/documentation/django_helper_methods_tutorial)
- [Model Meta Options](https://docs.djangoproject.com/en/5.1/ref/models/options/)
- [Time zones](https://docs.djangoproject.com/en/5.1/topics/i18n/timezones/)
- [Form and field validation](https://docs.djangoproject.com/en/5.1/ref/forms/validation/)

# Acknowledgements
<!-- Add a paragraph to show appreciation -->
- SME Kevin - particularly for reviewing and resolving a UX feature related to table filtering
---

[Return to top](#cedar--flame)