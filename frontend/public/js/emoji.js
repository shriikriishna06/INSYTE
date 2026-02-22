//emoji pop up 
const btn = document.getElementById('mobile-menu-btn');
const menu = document.getElementById('mobile-menu');
btn.addEventListener('click', () => {
    menu.classList.toggle('hidden');
});

function pop(event) {
    const container = event.currentTarget.parentNode;
    // Loop to create 7 emojis
    for (let i = 0; i < 7; i++) {
        const x = document.createElement('span');
        x.innerHTML = '⚡';
        x.classList.add('heart-animation');

        const randomX = -(Math.random() * 1000);
        const randomY = (Math.random() * 250);

        x.style.setProperty('--tx', `${(Math.random() - 0.5) * 50}px`);
        x.style.left = `${event.offsetX + randomX + event.target.offsetLeft}px`;
        x.style.top = `${event.offsetY + randomY}px`;

        container.appendChild(x);

        setTimeout(() => {
            x.remove();
        }, 1000);
    }
}

