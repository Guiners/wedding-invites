document.addEventListener("DOMContentLoaded", () => {
  const app = document.getElementById("app");
  const countdown = document.getElementById("countdown");

    function counter() {
      let timeLeftInMilliSec = new Date(app.dataset.weddingDateTime) - new Date();

      if (timeLeftInMilliSec <= 0) {
          countdown.textContent = "To już dziś ❤️"
          return;
      }

      const daysLeft = Math.floor(timeLeftInMilliSec/86400000)
      timeLeftInMilliSec = timeLeftInMilliSec%86400000

      const hoursLeft = Math.floor(timeLeftInMilliSec/3600000)
      timeLeftInMilliSec = timeLeftInMilliSec%3600000

      const minutesLeft = Math.floor(timeLeftInMilliSec/60000)
      timeLeftInMilliSec = timeLeftInMilliSec%60000

      const secondsLeft = Math.floor(timeLeftInMilliSec/1000)
      countdown.textContent = `${daysLeft} dni ${hoursLeft} godzin ${minutesLeft} minut ${secondsLeft} sekund`
  }

  const timer = setInterval(counter, 1000);

});
