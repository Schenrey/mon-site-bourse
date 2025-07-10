document.addEventListener("DOMContentLoaded", () => {
    const burger = document.getElementById("burger");
    const menu = document.getElementById("menu");
    const alertsSection = document.getElementById("alerts");
    const alertsList = document.getElementById("alerts-list");
  
    burger.addEventListener("click", () => {
      menu.classList.toggle("hidden");
    });
  
    const socket = io();
  
    socket.on("new_alert", (data) => {
      alertsSection.style.display = "block";
  
      const li = document.createElement("li");
      li.textContent = data.message;
      alertsList.prepend(li);
  
      // Optionnel: jouer un son ou notification desktop
      if (Notification.permission === "granted") {
        new Notification("Alerte Bourse", { body: data.message });
      }
    });
  
    if (Notification.permission !== "granted") {
      Notification.requestPermission();
    }
  });
  