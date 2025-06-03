async function loadTasks() {
    const res = await fetch("/tasks");
    const tasks = await res.json();
    const byParent = {};
    tasks.forEach(t => {
      const pid = t.parent_id || "root";
      (byParent[pid] ||= []).push(t);
    });
  
    // populate parent selector
    const select = document.getElementById("task-parent");
    select.innerHTML = '<option value="">(No Parent)</option>';
    tasks.forEach(t => {
      select.innerHTML += `<option value="${t.id}">${t.title}</option>`;
    });
  
    const ul = document.getElementById("task-list");
    ul.innerHTML = "";
    renderTaskTree(ul, byParent, "root", 0);
  }
  
  function renderTaskTree(container, byParent, parentId, depth) {
    const tasks = byParent[parentId] || [];
    for (const task of tasks) {
      const li = document.createElement("li");
      li.className = task.done ? "done" : "";
      li.style.marginLeft = `${depth * 1.5}rem`;
  
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked = task.done;
      checkbox.onchange = () => toggleTask(task.id);
      li.appendChild(checkbox);
  
      const span = document.createElement("span");
      span.textContent = " " + task.title;
      span.contentEditable = true;
      span.className = "edit-input";
      span.onblur = () => editTask(task.id, span.textContent.trim());
      li.appendChild(span);
  
      const delBtn = document.createElement("button");
      delBtn.textContent = "❌";
      delBtn.onclick = () => deleteTask(task.id);
      li.appendChild(delBtn);
  
      container.appendChild(li);
      renderTaskTree(container, byParent, task.id, depth + 1);
    }
  }
  
  async function addTask() {
    const title = document.getElementById("task-title").value;
    const parent = document.getElementById("task-parent").value;
    if (!title) return;
    await fetch("/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, parent_id: parent || null })
    });
    document.getElementById("task-title").value = "";
    loadTasks();
  }
  
  async function toggleTask(id) {
    await fetch(`/tasks/${id}/toggle`, { method: "POST" });
    loadTasks();
  }
  
  async function deleteTask(id) {
    await fetch(`/tasks/${id}/delete`, { method: "POST" });
    loadTasks();
  }
  
  async function editTask(id, title) {
    if (!title) return;
    await fetch(`/tasks/${id}/edit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title })
    });
  }
  
  loadTasks();