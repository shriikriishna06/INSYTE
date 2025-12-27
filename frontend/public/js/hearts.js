//hearts pop up 
const btn = document.getElementById('mobile-menu-btn');
const menu = document.getElementById('mobile-menu');
btn.addEventListener('click', () => {
    menu.classList.toggle('hidden');
});

function popHearts(event) {
    const container = event.currentTarget.parentNode;
    // Loop to create 7 hearts
    for (let i = 0; i < 7; i++) {
        const heart = document.createElement('span');
        heart.innerHTML = '❤️';
        heart.classList.add('heart-animation');

        const randomX = -(Math.random() * 1000);
        const randomY = (Math.random() * 250);

        heart.style.setProperty('--tx', `${(Math.random() - 0.5) * 50}px`);
        heart.style.left = `${event.offsetX + randomX + event.target.offsetLeft}px`;
        heart.style.top = `${event.offsetY + randomY}px`;

        container.appendChild(heart);

        setTimeout(() => {
            heart.remove();
        }, 1000);
    }
}

