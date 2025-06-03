
var input = document.getElementById("task-title");
input.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        addTask();
    }
})

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
  
      // 🔽 Context Menu Button
      const ctxBtn = document.createElement("button");
      ctxBtn.textContent = "⋮";
      ctxBtn.style.marginLeft = "0.5rem";
      ctxBtn.onclick = (e) => toggleContextMenu(task.id, li);
      li.appendChild(ctxBtn);
  
      container.appendChild(li);
      renderTaskTree(container, byParent, task.id, depth + 1);
    }
  }
  
  function toggleContextMenu(taskId, parentEl) {
    // Remove existing menus
    const oldMenu = document.getElementById("ctx-menu");
    if (oldMenu) oldMenu.remove();
  
    // Create menu
    const menu = document.createElement("div");
    menu.id = "ctx-menu";
    menu.style.position = "absolute";
    menu.style.background = "#fff";
    menu.style.border = "1px solid #ccc";
    menu.style.padding = "0.5rem";
    menu.style.boxShadow = "0 0 5px rgba(0,0,0,0.2)";
    menu.style.zIndex = 1000;
  
    // Position menu near parent element
    const rect = parentEl.getBoundingClientRect();
    menu.style.top = `${rect.bottom + window.scrollY}px`;
    menu.style.left = `${rect.left + window.scrollX + 150}px`;
  
    // Add options
    const editBtn = document.createElement("button");
    editBtn.textContent = "✏️ Edit";
    editBtn.onclick = () => {
      const newTitle = prompt("New title:");
      if (newTitle) editTask(taskId, newTitle).then(loadTasks);
      menu.remove();
    };
    menu.appendChild(editBtn);
  
    const delBtn = document.createElement("button");
    delBtn.textContent = "❌ Delete";
    delBtn.onclick = () => {
      deleteTask(taskId).then(loadTasks);
      menu.remove();
    };
    menu.appendChild(delBtn);
  
    const moveBtn = document.createElement("button");
    moveBtn.textContent = "📁 Move";
    moveBtn.onclick = async () => {
      const res = await fetch("/tasks");
      const tasks = await res.json();
      const options = tasks
        .filter(t => t.id !== taskId)
        .map(t => `${t.id}: ${t.title}`)
        .join("\n");
  
      const input = prompt("Enter new parent task ID:\n" + options);
      if (input) {
        await fetch(`/tasks/${taskId}/move`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ parent_id: input })
        });
        loadTasks();
      }
      menu.remove();
    };
    menu.appendChild(moveBtn);
  
    document.body.appendChild(menu);
  
    // Remove menu on outside click
    setTimeout(() => {
      const handler = (e) => {
        if (!menu.contains(e.target)) {
          menu.remove();
          document.removeEventListener("click", handler);
        }
      };
      document.addEventListener("click", handler);
    }, 0);
  }

loadTasks();