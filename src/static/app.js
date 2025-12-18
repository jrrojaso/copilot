document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Intenta obtener actividades del endpoint, si falla usa datos de ejemplo
  async function loadActivities() {
    try {
      const res = await fetch('/api/activities');
      if (!res.ok) throw new Error('fetch failed');
      return await res.json();
    } catch {
      // Ejemplo fallback
      return [
        { id: 'chess', name: 'Chess Club', description: 'Tactics & matches', participants: ['alice@mergington.edu', 'ben@mergington.edu'] },
        { id: 'robotics', name: 'Robotics Team', description: 'Build and program robots', participants: [] },
        { id: 'drama', name: 'Drama Club', description: 'Plays and improv', participants: ['cara@mergington.edu'] }
      ];
    }
  }

  function renderParticipantsList(ul, participants) {
    ul.innerHTML = '';
    if (!participants || participants.length === 0) {
      const li = document.createElement('li');
      li.textContent = 'No participants yet';
      li.className = 'empty';
      ul.appendChild(li);
      return;
    }
    participants.forEach(p => {
      const li = document.createElement('li');
      li.textContent = p;
      ul.appendChild(li);
    });
  }

  function renderActivities(activities) {
    activitiesList.innerHTML = '';
    activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';
    activities.forEach(act => {
      // fill select
      const opt = document.createElement('option');
      opt.value = act.id;
      opt.textContent = act.name;
      activitySelect.appendChild(opt);

      // fill card
      const activityCard = document.createElement("div");
      activityCard.className = "activity-card";

      activityCard.innerHTML = `
        <h4 class="activity-title">${act.name}</h4>
        <p class="activity-meta">ID: ${act.id}</p>
        <p class="activity-desc">${act.description || ''}</p>
        <ul class="participants-list"></ul>
      `;

      const ul = activityCard.querySelector('.participants-list');
      renderParticipantsList(ul, act.participants);
      activitiesList.appendChild(activityCard);
    });
  }

  (async function () {
    let activities = await loadActivities();

    // ensure each activity has participants array
    activities = activities.map(a => ({ ...a, participants: Array.isArray(a.participants) ? a.participants.slice() : [] }));
    renderActivities(activities);

    // Handle form submission
    signupForm.addEventListener("submit", async (event) => {
      event.preventDefault();

      const email = document.getElementById("email").value;
      const activityId = activitySelect.value;
      if (!email || !activityId) {
        messageDiv.textContent = 'Please provide an email and select an activity.';
        messageDiv.className = '';
        return;
      }

      // Local update (optimistic). If you have an API, POST here and refresh from server.
      const act = activities.find(a => a.id === activityId);
      if (!act) {
        messageDiv.textContent = 'Selected activity not found.';
        messageDiv.className = '';
        return;
      }
      if (!act.participants.includes(email)) {
        act.participants.push(email);
      }

      renderActivities(activities);
      signupForm.reset();
      messageDiv.textContent = 'Signed up successfully!';
      messageDiv.className = '';
      setTimeout(() => { messageDiv.className = 'hidden'; }, 3000);
    });
  })();
});
