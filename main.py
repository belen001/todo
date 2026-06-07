from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Base de datos en memoria para tareas
todos = [
    {"id": 1, "titulo": "Hacer tarea de la universidad", "completada": False},
    {"id": 2, "titulo": "Hacer aseo", "completada": False},
    {"id": 3, "titulo": "Leer capitulo 5 de libro de clase", "completada": True}
]

# --- VISTA HTML (Frontend Minimalista) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de Tareas</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-primary: #0f172a;
            --text-secondary: #64748b;
            --accent: #6366f1;
            --accent-hover: #4f46e5;
            --accent-light: #e0e7ff;
            --border: #e2e8f0;
            --danger: #ef4444;
            --danger-bg: #fee2e2;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 1.5rem;
        }

        .card {
            background: var(--card-bg);
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05), 0 0 0 1px rgba(0, 0, 0, 0.02);
            width: 100%;
            max-width: 480px;
            padding: 2rem;
            transition: all 0.3s ease;
        }

        h1 {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: -0.025em;
        }

        p.subtitle {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
        }

        .input-group {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
        }

        input[type="text"] {
            flex: 1;
            padding: 0.75rem 1rem;
            border: 1px solid var(--border);
            border-radius: 10px;
            font-family: inherit;
            font-size: 0.95rem;
            outline: none;
            transition: all 0.2s ease;
        }

        input[type="text"]:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-light);
        }

        button.btn-add {
            background: var(--accent);
            color: white;
            border: none;
            padding: 0.75rem 1.25rem;
            border-radius: 10px;
            font-family: inherit;
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        button.btn-add:hover {
            background: var(--accent-hover);
        }

        button.btn-add:active {
            transform: scale(0.98);
        }

        .todo-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            max-height: 320px;
            overflow-y: auto;
            padding-right: 2px;
        }

        /* Scrollbar custom style */
        .todo-list::-webkit-scrollbar {
            width: 6px;
        }
        .todo-list::-webkit-scrollbar-thumb {
            background-color: var(--border);
            border-radius: 3px;
        }

        .todo-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.85rem 1rem;
            background: #fff;
            border: 1px solid var(--border);
            border-radius: 10px;
            transition: all 0.2s ease;
        }

        .todo-item:hover {
            border-color: #cbd5e1;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }

        .todo-item.completed {
            background: #f8fafc;
            border-color: var(--border);
            opacity: 0.65;
        }

        .todo-item.completed span {
            text-decoration: line-through;
            color: var(--text-secondary);
        }

        .todo-content {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            flex: 1;
            cursor: pointer;
            user-select: none;
        }

        .todo-item input[type="checkbox"] {
            appearance: none;
            width: 1.25rem;
            height: 1.25rem;
            border: 2px solid #cbd5e1;
            border-radius: 6px;
            outline: none;
            cursor: pointer;
            display: grid;
            place-content: center;
            transition: all 0.2s ease;
        }

        .todo-item input[type="checkbox"]:checked {
            background-color: var(--accent);
            border-color: var(--accent);
        }

        .todo-item input[type="checkbox"]:checked::before {
            content: "";
            width: 0.55rem;
            height: 0.3rem;
            border-left: 2px solid white;
            border-bottom: 2px solid white;
            transform: rotate(-45deg) translate(1px, -1px);
        }

        .todo-title {
            font-size: 0.95rem;
            font-weight: 500;
        }

        .delete-btn {
            background: none;
            border: none;
            color: #94a3b8;
            cursor: pointer;
            padding: 0.35rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 6px;
            transition: all 0.2s ease;
        }

        .delete-btn:hover {
            color: var(--danger);
            background: var(--danger-bg);
        }

        .empty-state {
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.9rem;
            padding: 2rem 0;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Tareas Pendientes</h1>
        <p class="subtitle">Una aplicación minimalista en Python y Flask.</p>
        
        <div class="input-group">
            <input type="text" id="newTodoInput" placeholder="¿Qué tienes planeado hacer hoy?" onkeydown="if(event.key === 'Enter') addTodo()">
            <button class="btn-add" onclick="addTodo()">Añadir</button>
        </div>

        <ul id="todoList" class="todo-list">
            <!-- Tareas insertadas dinámicamente -->
        </ul>
    </div>

    <script>
        const API_URL = '/todos';

        // Cargar las tareas al iniciar
        document.addEventListener('DOMContentLoaded', fetchTodos);

        async function fetchTodos() {
            try {
                const response = await fetch(API_URL);
                const todos = await response.json();
                renderTodos(todos);
            } catch (error) {
                console.error('Error al obtener tareas:', error);
            }
        }

        function renderTodos(todos) {
            const list = document.getElementById('todoList');
            list.innerHTML = '';

            if (todos.length === 0) {
                list.innerHTML = '<li class="empty-state">🎉 ¡Todo listo! No tienes tareas pendientes.</li>';
                return;
            }

            todos.forEach(todo => {
                const li = document.createElement('li');
                li.className = `todo-item ${todo.completada ? 'completed' : ''}`;

                li.innerHTML = `
                    <div class="todo-content" onclick="toggleTodo(${todo.id}, ${!todo.completada})">
                        <input type="checkbox" ${todo.completada ? 'checked' : ''} onclick="event.stopPropagation(); toggleTodo(${todo.id}, !${todo.completada})">
                        <span class="todo-title">${escapeHTML(todo.titulo)}</span>
                    </div>
                    <button class="delete-btn" onclick="deleteTodo(${todo.id})" title="Eliminar tarea">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
                    </button>
                `;
                list.appendChild(li);
            });
        }

        async function addTodo() {
            const input = document.getElementById('newTodoInput');
            const titulo = input.value.trim();
            if (!titulo) return;

            try {
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ titulo })
                });

                if (response.ok) {
                    input.value = '';
                    fetchTodos();
                }
            } catch (error) {
                console.error('Error al crear tarea:', error);
            }
        }

        async function toggleTodo(id, completada) {
            try {
                const response = await fetch(`${API_URL}/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ completada })
                });

                if (response.ok) {
                    fetchTodos();
                }
            } catch (error) {
                console.error('Error al actualizar tarea:', error);
            }
        }

        async function deleteTodo(id) {
            try {
                const response = await fetch(`${API_URL}/${id}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    fetchTodos();
                }
            } catch (error) {
                console.error('Error al eliminar tarea:', error);
            }
        }

        function escapeHTML(str) {
            return str.replace(/[&<>'"]/g, 
                tag => ({
                    '&': '&amp;',
                    '<': '&lt;',
                    '>': '&gt;',
                    "'": '&#39;',
                    '"': '&quot;'
                }[tag] || tag)
            );
        }
    </script>
</body>
</html>
"""

# --- RUTAS DE LA API ---

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/todos", methods=["GET"])
def obtener_todos():
    return jsonify(todos), 200

@app.route("/todos", methods=["POST"])
def agregar_todo():
    data = request.get_json()
    if not data or "titulo" not in data:
        return jsonify({"error": "Falta el campo 'titulo'"}), 400
    
    nuevo_id = max([t["id"] for t in todos], default=0) + 1
    nueva_tarea = {
        "id": nuevo_id,
        "titulo": data["titulo"],
        "completada": data.get("completada", False)
    }
    todos.append(nueva_tarea)
    return jsonify(nueva_tarea), 201

@app.route("/todos/<int:id>", methods=["PUT"])
def actualizar_todo(id):
    data = request.get_json()
    for t in todos:
        if t["id"] == id:
            t["titulo"] = data.get("titulo", t["titulo"])
            t["completada"] = data.get("completada", t["completada"])
            return jsonify(t), 200
    return jsonify({"error": "Tarea no encontrada"}), 404

@app.route("/todos/<int:id>", methods=["DELETE"])
def eliminar_todo(id):
    for i, t in enumerate(todos):
        if t["id"] == id:
            eliminado = todos.pop(i)
            return jsonify(eliminado), 200
    return jsonify({"error": "Tarea no encontrada"}), 404

if __name__ == "__main__":
    # Escucha en todas las interfaces de red (0.0.0.0) y puerto 5000 por defecto
    # Esto es ideal para probar localmente y prepararse para el despliegue.
    app.run(host="0.0.0.0", port=5000, debug=True)