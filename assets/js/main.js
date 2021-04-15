var navbar = document.getElementById('navbar');
var sticky = navbar.offsetTop;
var about = document.getElementById('about');
var skills = document.getElementById('skills');
var projects = document.getElementById('projects');
var achievements = document.getElementById('achievements');

about.style.display = 'none';
skills.style.display = 'none';
projects.style.display = 'none';
achievements.style.display = 'none';
window.onscroll = function () { stickNavbar() };

function stickNavbar() {
    if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky");
    }
    else {
        navbar.classList.remove('sticky');
    }
};

function gototop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function displayAbout() {
    projects.style.display = 'none';
    skills.style.display = 'none';
    achievements.style.display = 'none';
    about.style.display = 'block';
    about.scrollIntoView({ behavior: 'smooth' });
};

function displaySkills() {
    projects.style.display = 'none';
    about.style.display = 'none';
    achievements.style.display = 'none';
    skills.style.display = 'block';
    skills.scrollIntoView({ behavior: 'smooth' });
};

function displayProjects() {
    skills.style.display = 'none';
    about.style.display = 'none';
    achievements.style.display = 'none';
    projects.style.display = 'block';
    projects.scrollIntoView({ behavior: 'smooth' });
};

function displayExtras() {
    skills.style.display = 'none';
    about.style.display = 'none';
    projects.style.display = 'none';
    achievements.style.display = 'block';
    achievements.scrollIntoView({ behavior: 'smooth' });
}