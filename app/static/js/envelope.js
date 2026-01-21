document.addEventListener("DOMContentLoaded", () => {
    const envelope = document.getElementById('envelope');
    const envelopeSection = document.getElementById('envelope-section');
    const otherSections = document.querySelectorAll('main > section:not(.envelope-section)');

    envelope.addEventListener('click', () => {
        envelope.classList.add('open');

        setTimeout(() => {
            envelopeSection.style.display = 'none';
            otherSections.forEach((sec,i) => {
                setTimeout(()=>{ sec.classList.add('fade-in'); }, i*300);
            });
        },600);
    });
});
