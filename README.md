# Students Points Reward System
## The Story Behind the Points
Welcome to the Students' Points Reward System, where each line of code narrates a story of passion, challenges, and the dedication to creating a meaningful impact in the educational environment. This isn't just a point-based reward system; it's a reflection of our journey and a testament to the human touch behind the keyboard.
## Project Description:
The Student Point Reward System is a web-based application designed to incentivize and reward students for their academic achievements and positive contributions. This system allows educators to allocate points to students based on various criteria, fostering a positive learning environment.

Students earn points for attending classes, participating in extracurricular activities, helping peers, achieving academic milestones etc. 
Students can redeem these points for rewards like books, school supplies, or privileges within the school.

## The Human Touch
This project goes beyond the technicalities. It's about students earning points, teachers recognizing achievements, and a digital platform fostering a positive learning atmosphere. We believe that behind every line of code, there's a student, a teacher, and a developer with a shared goal of making education not just informative but also rewarding.

## Team of Developers
- Chris Saka
* Anzellah Jepkoech
+ Peter Thuo

**Authors LinkedIn:**
- [Saka](https://www.linkedin.com/in/chris-saka/)
- [Peter](https://www.linkedin.com/in/peter-rigii-b78b2968/)
- [Anzellah](https://www.linkedin.com/in/anzellah-jepkoech-502424153)

**Landing page:** [Landing Page](https://anzelah.github.io/Landing_page/) 

**Deployed Site:** [Student Point Reward System](https://www.pointsystem.tech/)

**Final Project Blog Article:** [Blog](https://medium.com/@sakachris90/unveiling-the-student-point-reward-system-a-portfolio-project-showcase-00e7501bc9d3)

## Technologies
### Front-end:
+ HTML/CSS
+ Bootstrap
### Back-end:
+ Python
+ Django
### Database:
+ PostgreSQL

## Technical Challenges: Django Tenancy and Custom User Creation

Embarking on this project, we faced intricate technical challenges that shaped the robustness of the Students' Points Reward System. One of the major hurdles was the seamless integration of Django tenancy and the implementation of custom user creation with user profiles.

### Django Tenancy

The challenge lay in creating an architecture that allows the system to serve multiple schools, each with its own isolated database schema. Django tenancy, a powerful solution, required careful implementation to ensure scalability, security, and efficient management of data across different educational institutions.

### Custom User Creation and Profiles

Recognizing that a one-size-fits-all user model wouldn't suffice, we ventured into the realm of custom user creation and profiles. This involved designing a system that accommodates various user roles, captures essential user information, and provides a personalized experience for both students and educators.

## Algorithmic Journey

At the heart of the system lies the algorithms that power the point allocation and redemption process. These algorithms not only ensure efficient data handling but also resonate with the overall theme of fostering positive student-teacher interactions.

## Next Steps

As we reflect on this project, we envision its future iterations. The roadmap includes refining the user experience, enhancing the visual appeal, and exploring additional features to further enrich the educational journey.

## Behind the Scenes

Explore the 'screenshots' section to witness the evolution of the project visually. Each image tells a story of a technical challenge tackled, a feature implemented, and a moment of accomplishment.

## Timeline

This project is a timeline of growth:

- **Project Inception:** 2nd November, 2023
- **First Commit:** 6th November, 2023
- **Deployment:** 15th December, 2023

## Installation

To set up the Student Point Reward System locally, follow these steps:

1. Clone the repository: 
   ```bash
   git clone [repository_url]
2. Navigate to the project directory:
   ```bash
   cd Reward_System
3. Configure the Django settings:
   ```
   python3 -m venv venv
   source venv/bin/activate
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
5. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
6. Start the Django development server:
   ```bash
   python manage.py runserver
7. Access the application in your browser at http://localhost:8000.

## Usage
1. Create superuser:
   ```bash
   python manage.py createsuperuser
2. Create tenant:
   ```bash
   python manage.py create_tenant
3. Create tenant superuser:
   ```bash
   python manage.py create_tenant_superuser
4. Login to the system with your tenant admin credentials.
5. Create users (teachers and students), point award categories and award items.
6. Respective users can now log in with the created credentials.

## Contributing
We welcome contributions from the community to enhance the Students Points Reward System. If you would like to contribute, please follow these steps:
1. Fork the repository
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/new-feature
3. Make your changes and commit them:
   ```bash
   git commit -m "Description of changes"
4. Push your changes to your fork:
   ```bash
   git push origin feature/new-feature
5. Open a pull request to the main branch of the original repository.

## Screenshots
### Data Model

![Point Reward System (1)](https://github.com/sakachris/Reward_System/assets/122869546/9c416393-172a-4ab1-9cfe-a917215c2ad0)

### Landing page
![landing page](https://github.com/sakachris/Reward_System/assets/122869546/0dd7f2ed-1246-4829-b6f3-5dc41d60cb74)


### Login Page
![login](https://github.com/sakachris/Reward_System/assets/122869546/9373385a-4966-493e-80c3-659e5d11feba)


### Teachers' Dashboard
![teacher](https://github.com/sakachris/Reward_System/assets/122869546/87cf6c4d-5833-4fe8-aa4d-af3a618e8e66)


### Students' Dashboard
![stud_dashboard](https://github.com/sakachris/Reward_System/assets/122869546/06267bbd-6d92-4b43-bde7-71d1ee2c68cb)


![stud2](https://github.com/sakachris/Reward_System/assets/122869546/dbd6f6d6-f2d1-4402-a7a1-bc05f9f8db9d)

Thank you for exploring the Students' Points Reward System. May it not only reflect the technical prowess but also the commitment to creating a positive educational experience.

🌟 Happy Learning and Rewarding!
