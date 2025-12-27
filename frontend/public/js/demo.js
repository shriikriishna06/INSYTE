//Video playback
const modal = document.getElementById('video-modal');
const backdrop = document.getElementById('modal-backdrop');
const content = document.getElementById('modal-content');
const videoElement = document.getElementById('demo-video');

function openModal() {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    setTimeout(() => {
        backdrop.classList.remove('opacity-0');
        content.classList.remove('scale-95', 'opacity-0');
        content.classList.add('scale-100', 'opacity-100');
        videoElement.play();
    }, 10);
}

function closeModal() {
    backdrop.classList.add('opacity-0');
    content.classList.remove('scale-100', 'opacity-100');
    content.classList.add('scale-95', 'opacity-0');
    videoElement.pause();
    videoElement.currentTime=0;
    setTimeout(() => {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }, 300);
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
        closeModal();
    }
});