document.addEventListener('DOMContentLoaded', () => {
    const guessBtn = document.getElementById('guess-button');
    const resetBtn = document.getElementById('reset-button');
    const input = document.getElementById('letter-input');
    const message = document.getElementById('message');

    async function handleGuess() {
        const letter = input.value;
        input.value = "";
        if (!letter) return;

        const response = await fetch('/guess', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ letter: letter })
        });
        const data = await response.json();

        document.getElementById('word-display').innerText = data.display;
        document.getElementById('attempts-count').innerText = data.attempts;
        document.getElementById('used-letters').innerText = data.used;

        if (data.win) {
            message.innerText = "YOU WON! 🎉";
            message.style.color = "green";
            endGame();
        } else if (data.game_over) {
            message.innerText = "GAME OVER! Word: " + data.correct_word;
            message.style.color = "red";
            endGame();
        }
    }

    async function handleReset() {
        const response = await fetch('/reset', { method: 'POST' });
        const data = await response.json();
        location.reload(); // Simplest way to restart everything
    }

    function endGame() {
        guessBtn.disabled = true;
        input.disabled = true;
        document.getElementById('play-again').classList.remove('hidden');
    }

    guessBtn.addEventListener('click', handleGuess);
    resetBtn.addEventListener('click', handleReset);
});