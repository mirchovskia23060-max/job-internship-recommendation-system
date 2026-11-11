const API_BASE = "http://localhost:8000";

const candidateSelect = document.getElementById("candidateSelect");
const categoryFilter = document.getElementById("categoryFilter");
const typeFilter = document.getElementById("typeFilter");
const remoteFilter = document.getElementById("remoteFilter");
const applyFiltersBtn = document.getElementById("applyFiltersBtn");
const cardsContainer = document.getElementById("cardsContainer");
const statusMessage = document.getElementById("statusMessage");

// Иницијализација на URL параметри
const urlParams = new URLSearchParams(window.location.search);
const initialCandidateId = urlParams.get("candidate_id") || "1";

async function init() {
  try {
    const res = await fetch(`${API_BASE}/candidates`);
    if (!res.ok) throw new Error("Грешка при вчитување кандидати");
    const candidates = await res.json();

    candidateSelect.innerHTML = candidates.map(c =>
      `<option value="${c.id}" ${c.id == initialCandidateId ? 'selected' : ''}>${c.name} (${c.study_area})</option>`
    ).join("");

    loadRecommendations();
  } catch (err) {
    showStatus("Грешка при комуникација со серверот.", true);
  }
}

async function loadRecommendations() {
  const candidateId = candidateSelect.value;
  showStatus("Се вчитуваат препораки...");
  cardsContainer.innerHTML = "";

  try {
    const res = await fetch(`${API_BASE}/recommendations/${candidateId}`);
    if (!res.ok) throw new Error("Неуспешно преземање на препораки");

    const data = await res.json();
    let recs = data.recommendations;

    // Примена на филтри на фронтенд страната
    const selectedCategory = categoryFilter.value;
    const selectedType = typeFilter.value;
    const remoteOnly = remoteFilter.checked;

    if (selectedCategory) {
      recs = recs.filter(r => r.category === selectedCategory);
    }
    if (selectedType) {
      recs = recs.filter(r => r.employment_type === selectedType);
    }
    if (remoteOnly) {
      recs = recs.filter(r => r.work_mode.toLowerCase() === "remote");
    }

    if (recs.length === 0) {
      showStatus("Нема пронајдено соодветни огласи за избраните критериуми.");
      return;
    }

    clearStatus();
    renderCards(recs);
  } catch (err) {
    showStatus("Настана грешка при прикажување на препораките.", true);
  }
}

function renderCards(recommendations) {
  cardsContainer.innerHTML = recommendations.map(job => `
    <div class="card">
      <div>
        <div class="card-header">
          <div class="card-title">${job.title}</div>
          <div class="score-badge">${job.score} поени</div>
        </div>
        <div class="card-meta">
          <strong>${job.employer}</strong> • ${job.category}
        </div>
        <div class="card-details">
          <p>📍 <strong>Локација:</strong> ${job.location_name} (${job.work_mode}) ${job.distance_km !== null ? `• ${job.distance_km} km` : ''}</p>
          <p>💼 <strong>Тип:</strong> ${job.employment_type}</p>
          <p>💰 <strong>Плата:</strong> ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()} МКД</p>
          <p>👥 <strong>Слободни места:</strong> ${job.available_positions}</p>
          <p>📅 <strong>Краен рок:</strong> ${job.application_deadline}</p>
        </div>
      </div>
      <div class="card-reason">
        💡 ${job.reason}
      </div>
    </div>
  `).join("");
}

function showStatus(text, isError = false) {
  statusMessage.textContent = text;
  statusMessage.style.color = isError ? "#ef4444" : "#64748b";
  statusMessage.style.display = "block";
}

function clearStatus() {
  statusMessage.textContent = "";
  statusMessage.style.display = "none";
}

candidateSelect.addEventListener("change", () => {
  const newUrl = `${window.location.pathname}?candidate_id=${candidateSelect.value}`;
  window.history.replaceState(null, '', newUrl);
  loadRecommendations();
});

applyFiltersBtn.addEventListener("click", loadRecommendations);

window.onload = init;
