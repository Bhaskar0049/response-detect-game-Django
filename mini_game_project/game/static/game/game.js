(function() {
    // Utility to get CSRF token from cookie (in case we need it)
    function getCsrfToken() {
        const cookieValue = document.cookie.match(/csrftoken=([^;]+)/);
        return cookieValue ? cookieValue[1] : document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    document.addEventListener('DOMContentLoaded', function() {
        const gameArea = document.getElementById('game-area');
        const scoreDisplay = document.getElementById('score');
        const comboDisplay = document.getElementById('combo');
        const timeDisplay = document.getElementById('time');
        const sessionId = document.getElementById('session-id').value;

        let hits = 0;
        let combos = 0;
        let lastHitTime = null;
        const gameDuration = 30.0; // seconds
        const spawnInterval = 500; // milliseconds between spawns
        let startTime = performance.now();

        // Spawn a target at a random position within the game area
        function spawnTarget() {
            const target = document.createElement('div');
            target.classList.add('target');
            const size = 50;
            const areaRect = gameArea.getBoundingClientRect();
            const x = Math.random() * (areaRect.width - size);
            const y = Math.random() * (areaRect.height - size);
            target.style.width = `${size}px`;
            target.style.height = `${size}px`;
            target.style.left = `${x}px`;
            target.style.top = `${y}px`;
            target.addEventListener('click', handleHit);
            gameArea.appendChild(target);
            // Remove after 1 second
            setTimeout(() => {
                if (target.parentNode) {
                    target.remove();
                }
            }, 1000);
        }

        function handleHit(event) {
            hits += 1;
            const now = performance.now();
            if (lastHitTime && now - lastHitTime <= 800) {
                combos += 1;
            }
            lastHitTime = now;
            scoreDisplay.textContent = hits.toString();
            comboDisplay.textContent = combos.toString();
            event.target.remove();
        }

        // Game loop updates time and spawns targets
        function gameLoop() {
            const elapsed = (performance.now() - startTime) / 1000.0;
            const remaining = Math.max(0, gameDuration - elapsed);
            timeDisplay.textContent = remaining.toFixed(1);
            if (remaining <= 0) {
                finishGame();
            } else {
                requestAnimationFrame(gameLoop);
            }
        }

        // Spawn targets on a timer separate from the game loop
        let spawnTimer = setInterval(() => {
            // Only spawn if there is time remaining
            const elapsed = (performance.now() - startTime) / 1000.0;
            if (elapsed < gameDuration) {
                spawnTarget();
            } else {
                clearInterval(spawnTimer);
            }
        }, spawnInterval);

        function finishGame() {
            // Send results to server
            const payload = {
                hits: hits,
                combos: combos,
                duration: (performance.now() - startTime) / 1000.0,
            };
            fetch(`/finish/${sessionId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify(payload),
            })
                .then((response) => response.json())
                .then((data) => {
                    // Redirect to results page
                    window.location.href = data.redirect_url;
                })
                .catch(() => {
                    // Fallback: reload page on failure
                    window.location.reload();
                });
        }

        // Kick off the game
        gameLoop();
    });
})();