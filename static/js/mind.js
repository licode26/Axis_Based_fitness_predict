// Timer management
let timerInterval;

// Start an exercise
function startExercise(exerciseId, duration) {
    // Display instructions and start timer
    document.getElementById(`${exerciseId}-instructions`).textContent = `Exercise in progress...`;
    document.getElementById(`${exerciseId}-timer`).textContent = formatTime(duration * 60); // Set initial timer display

    let timeLeft = duration * 60; // Convert minutes to seconds

    timerInterval = setInterval(() => {
        timeLeft--;
        document.getElementById(`${exerciseId}-timer`).textContent = formatTime(timeLeft);

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            showWellDone();
        }
    }, 1000);
}

// Stop an exercise
function stopExercise(exerciseId) {
    clearInterval(timerInterval);
    document.getElementById(`${exerciseId}-instructions`).textContent = '';
    document.getElementById(`${exerciseId}-timer`).textContent = '00:00';
}

// Format time in MM:SS
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

// Show the Well Done interface
function showWellDone() {
    document.getElementById('main-content').style.display = 'none';
    document.getElementById('well-done').classList.remove('hidden');
}

// Return to the exercise selection
function goBack() {
    document.getElementById('well-done').classList.add('hidden');
    document.getElementById('main-content').style.display = 'block';
}

// Initialize event listeners for all exercise buttons
document.addEventListener('DOMContentLoaded', () => {
    // List of exercises - ensure these match the IDs used in your HTML
    const exercises = ['focused-breathing', 'progressive-muscle-relaxation', 'visualization', 'meditation', 'mindfulness'];

    exercises.forEach(exerciseId => {
        const startButton = document.getElementById(`${exerciseId}-start`);
        const stopButton = document.getElementById(`${exerciseId}-stop`);

        if (startButton) {
            startButton.addEventListener('click', () => startExercise(exerciseId, 5)); // Start with 5-minute duration
        }

        if (stopButton) {
            stopButton.addEventListener('click', () => stopExercise(exerciseId));
        }
    });
});
