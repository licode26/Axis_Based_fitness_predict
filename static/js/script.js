/*document.getElementById("login-btn").addEventListener("click", function() {
    document.getElementById("login-form").classList.remove("hidden");
    document.getElementById("signup-form").classList.add("hidden");
});

document.getElementById("signup-btn").addEventListener("click", function() {
    document.getElementById("signup-form").classList.remove("hidden");
    document.getElementById("login-form").classList.add("hidden");
});

function login() {
    // Add your login logic here
    alert("Logged in!");
}

function signup() {
    // Add your signup logic here
    alert("Signed up!");
}*/
document.querySelectorAll('.sports-list a').forEach(link => {
    link.addEventListener('mouseover', () => {
        link.style.transform = 'scale(1.1)';
    });
    link.addEventListener('mouseout', () => {
        link.style.transform = 'scale(1)';
    });
});


