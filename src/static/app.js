document.addEventListener("DOMContentLoaded", () => {
  const curso = document.querySelector('[name="curso_id"]');
  const disciplina = document.querySelector('[name="disciplina_id"]');
  const professor = document.querySelector('[name="professor_id"]');
  const nota = document.querySelector('[name="nota"]');
  const btn = document.querySelector('button[type="submit"], input[type="submit"]');

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

  // Estado inicial: tudo bloqueado
  disableField(disciplina, "Selecione o curso primeiro");
  disableField(professor, "Selecione o curso primeiro");
  disableField(nota, "Selecione o curso primeiro");
  if (btn) btn.disabled = true;

  curso.addEventListener("change", () => {
    const cursoId = curso.value;

    if (!cursoId) {
      disableField(disciplina, "Selecione o curso primeiro");
      disableField(professor, "Selecione o curso primeiro");
      disableField(nota, "Selecione o curso primeiro");
      if (btn) btn.disabled = true;
      return;
    }

    // Libera os campos dependentes do curso
    enableField(disciplina, "Selecione a disciplina…");
    enableField(professor, "Selecione o professor…");
    enableField(nota, "Selecione a nota…");
    if (btn) btn.disabled = false;

    filterByCurso(cursoId);
  });

  console.log("app.js ativo: curso -> disciplina, professor e nota.");
});
