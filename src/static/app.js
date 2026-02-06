document.addEventListener("DOMContentLoaded", () => {
  const curso = document.querySelector('[name="curso_id"]');
  const disciplina = document.querySelector('[name="disciplina_id"]');
  const professor = document.querySelector('[name="professor_id"]');
  const btn = document.querySelector('button[type="submit"], input[type="submit"]');
  const form = document.getElementById("avaliar-form");

  if (!curso || !disciplina) {
    console.error("Não achei curso_id ou disciplina_id no HTML.");
    return;
  }

  function setFirstOptionText(selectEl, text) {
    if (!selectEl) return;
    if (selectEl.tagName.toLowerCase() !== "select") return;
    if (selectEl.options.length > 0) selectEl.options[0].textContent = text;
  }

  function disableField(field, msg) {
    if (!field) return;
    field.disabled = true;
    field.value = "";
    setFirstOptionText(field, msg);
  }

  function enableField(field, msg) {
    if (!field) return;
    field.disabled = false;
    setFirstOptionText(field, msg);
  }

  function filterByCurso(cursoId) {
    const opts = Array.from(disciplina.querySelectorAll("option"));
    opts.forEach((opt, idx) => {
      if (idx === 0) return; // placeholder
      const cid = opt.getAttribute("data-curso");
      const show = cid === String(cursoId);
      opt.hidden = !show;
      opt.disabled = !show;
    });
    disciplina.value = "";
  }

  // Estado inicial: apenas disciplina e professor bloqueados
  disableField(disciplina, "Selecione o curso primeiro");
  disableField(professor, "Selecione o curso primeiro");
  if (btn) btn.disabled = true;

  curso.addEventListener("change", () => {
    const cursoId = curso.value;

    if (!cursoId) {
      disableField(disciplina, "Selecione o curso primeiro");
      disableField(professor, "Selecione o curso primeiro");
      if (btn) btn.disabled = true;
      return;
    }

    // Libera os campos dependentes do curso
    enableField(disciplina, "Selecione a disciplina…");
    enableField(professor, "Selecione o professor…");
    if (btn) btn.disabled = false;

    filterByCurso(cursoId);
  });

  // Validação antes de enviar
  if (form) {
    form.addEventListener("submit", (e) => {
      const cursoId = curso.value;
      const disciplinaId = disciplina.value;
      const professorId = professor.value;
      const notaSelecionada = document.querySelector('[name="nota"]:checked');

      if (!cursoId || !disciplinaId || !professorId || !notaSelecionada) {
        e.preventDefault();
        alert("Por favor, preencha todos os campos obrigatórios: Curso, Disciplina, Professor e Nota.");
        return false;
      }
    });
  }

  // Contador de caracteres para o comentário
  const comentarioField = document.getElementById("comentario");
  const charCount = document.getElementById("char-count");
  
  if (comentarioField && charCount) {
    comentarioField.addEventListener("input", () => {
      const count = comentarioField.value.length;
      charCount.textContent = count;
      
      // Muda a cor quando está próximo do limite
      if (count > 450) {
        charCount.style.color = "var(--error)";
      } else if (count > 400) {
        charCount.style.color = "var(--accent)";
      } else {
        charCount.style.color = "var(--text-muted)";
      }
    });
  }

  console.log("app.js ativo: curso -> disciplina, professor e nota.");
});

// ===== BUSCA COM SUGESTÕES NO RANKING =====
document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("ranking-search");
  const rankingTable = document.getElementById("ranking-table");
  const noResults = document.getElementById("no-results");
  
  if (!searchInput || !rankingTable) return;
  
  // Criar dropdown de sugestões
  const suggestionsDropdown = document.createElement("div");
  suggestionsDropdown.className = "suggestions-dropdown";
  searchInput.parentElement.appendChild(suggestionsDropdown);
  
  let currentSuggestions = [];
  let selectedIndex = -1;
  let searchTimeout;
  let allRows = [];
  
  // Guardar todas as linhas originais
  const tbody = rankingTable.querySelector("tbody");
  allRows = Array.from(tbody.querySelectorAll("tr"));
  
  // Buscar sugestões
  searchInput.addEventListener("input", (e) => {
    clearTimeout(searchTimeout);
    const query = e.target.value.trim();
    selectedIndex = -1;
    
    if (query.length < 2) {
      hideSuggestions();
      showAllRows();
      return;
    }
    
    searchTimeout = setTimeout(() => {
      fetchSuggestions(query);
    }, 300);
  });
  
  // Navegação com teclado
  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      selectedIndex = Math.min(selectedIndex + 1, currentSuggestions.length - 1);
      updateSuggestionHighlight();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      selectedIndex = Math.max(selectedIndex - 1, -1);
      updateSuggestionHighlight();
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (selectedIndex >= 0 && currentSuggestions[selectedIndex]) {
        selectSuggestion(currentSuggestions[selectedIndex].text);
      } else {
        filterTable(searchInput.value.trim());
      }
      hideSuggestions();
    } else if (e.key === "Escape") {
      hideSuggestions();
    }
  });
  
  // Fechar sugestões ao clicar fora
  document.addEventListener("click", (e) => {
    if (!searchInput.contains(e.target) && !suggestionsDropdown.contains(e.target)) {
      hideSuggestions();
    }
  });
  
  async function fetchSuggestions(query) {
    try {
      const response = await fetch(`/api/ranking/suggestions?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      currentSuggestions = data.suggestions || [];
      displaySuggestions();
    } catch (error) {
      console.error("Erro ao buscar sugestões:", error);
    }
  }
  
  function displaySuggestions() {
    if (currentSuggestions.length === 0) {
      hideSuggestions();
      return;
    }
    
    suggestionsDropdown.innerHTML = currentSuggestions.map((suggestion, index) => {
      const typeClass = suggestion.type === "disciplina" ? "type-disciplina" : "type-professor";
      const label = suggestion.type === "disciplina" ? "Disciplina" : "Professor";
      return `
        <div class="suggestion-item" data-index="${index}">
          <span class="suggestion-badge ${typeClass}">${label}</span>
          <div class="suggestion-content">
            <div class="suggestion-text">${highlightMatch(suggestion.text, searchInput.value)}</div>
          </div>
        </div>
      `;
    }).join("");
    
    suggestionsDropdown.style.display = "block";
    
    // Adicionar listeners de clique
    suggestionsDropdown.querySelectorAll(".suggestion-item").forEach(item => {
      item.addEventListener("click", () => {
        const index = parseInt(item.dataset.index);
        selectSuggestion(currentSuggestions[index].text);
        hideSuggestions();
      });
    });
  }
  
  function highlightMatch(text, query) {
    const regex = new RegExp(`(${query})`, "gi");
    return text.replace(regex, "<strong>$1</strong>");
  }
  
  function updateSuggestionHighlight() {
    const items = suggestionsDropdown.querySelectorAll(".suggestion-item");
    items.forEach((item, index) => {
      if (index === selectedIndex) {
        item.classList.add("selected");
        item.scrollIntoView({ block: "nearest" });
      } else {
        item.classList.remove("selected");
      }
    });
  }
  
  function selectSuggestion(text) {
    searchInput.value = text;
    filterTable(text);
  }
  
  function filterTable(searchTerm) {
    if (!searchTerm) {
      showAllRows();
      return;
    }
    
    const term = searchTerm.toLowerCase();
    let visibleCount = 0;
    
    allRows.forEach(row => {
      const disciplina = row.cells[1]?.textContent.toLowerCase() || "";
      const curso = row.cells[2]?.textContent.toLowerCase() || "";
      const professor = row.cells[3]?.textContent.toLowerCase() || "";
      
      if (disciplina.includes(term) || curso.includes(term) || professor.includes(term)) {
        row.style.display = "";
        visibleCount++;
        // Atualizar posição
        const positionSpan = row.querySelector(".ranking-position");
        if (positionSpan) {
          positionSpan.textContent = visibleCount;
        }
      } else {
        row.style.display = "none";
      }
    });
    
    if (visibleCount === 0) {
      rankingTable.style.display = "none";
      noResults.style.display = "block";
    } else {
      rankingTable.style.display = "table";
      noResults.style.display = "none";
    }
  }
  
  function showAllRows() {
    allRows.forEach((row, index) => {
      row.style.display = "";
      const positionSpan = row.querySelector(".ranking-position");
      if (positionSpan) {
        positionSpan.textContent = index + 1;
      }
    });
    rankingTable.style.display = "table";
    noResults.style.display = "none";
  }
  
  function hideSuggestions() {
    suggestionsDropdown.style.display = "none";
    selectedIndex = -1;
  }
});

// ===== AUTO-APLICAR FILTROS =====
document.addEventListener("DOMContentLoaded", () => {
  const filterForm = document.getElementById("filter-form");
  if (!filterForm) return;
  
  const selects = filterForm.querySelectorAll("select");
  selects.forEach(select => {
    select.addEventListener("change", () => {
      filterForm.submit();
    });
  });
});
