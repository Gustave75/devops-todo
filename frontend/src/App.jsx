import { useState, useEffect } from "react"
import axios from "axios"
import "./App.css"

const API = import.meta.env.VITE_API_URL || "http://localhost:8000"

function App() {
  const [tasks, setTasks] = useState([])
  const [title, setTitle] = useState("")

  useEffect(() => { fetchTasks() }, [])

  const fetchTasks = async () => {
    const res = await axios.get(`${API}/tasks`)
    setTasks(res.data)
  }

  const addTask = async () => {
    if (!title.trim()) return
    await axios.post(`${API}/tasks`, { title })
    setTitle("")
    fetchTasks()
  }

  const toggleDone = async (task) => {
    await axios.patch(`${API}/tasks/${task.id}`, { done: !task.done })
    fetchTasks()
  }

  const deleteTask = async (id) => {
    await axios.delete(`${API}/tasks/${id}`)
    fetchTasks()
  }

  const done = tasks.filter(t => t.done).length

  return (
    <div className="app">
      <div className="header">
        <h1>Task manager</h1>
        <p>DevOps TP — Todo application</p>
      </div>

      <div className="input-row">
        <input
          type="text"
          placeholder="Add a new task..."
          value={title}
          onChange={e => setTitle(e.target.value)}
          onKeyDown={e => e.key === "Enter" && addTask()}
        />
        <button className="btn-add" onClick={addTask}>+ Add</button>
      </div>

      <div className="stats">
        <div className="stat"><div className="val">{tasks.length}</div><div className="lbl">Total</div></div>
        <div className="stat"><div className="val">{done}</div><div className="lbl">Done</div></div>
        <div className="stat"><div className="val">{tasks.length - done}</div><div className="lbl">Remaining</div></div>
      </div>

      <div className="section-label">Tasks</div>

      <div className="task-list">
        {tasks.length === 0 && (
          <div className="empty">No tasks yet. Add one above.</div>
        )}
        {tasks.map(task => (
          <div key={task.id} className={`task ${task.done ? "done" : ""}`} onClick={() => toggleDone(task)}>
            <div className="checkbox">{task.done && <span>✓</span>}</div>
            <span className="task-title">{task.title}</span>
            <button className="btn-del" onClick={e => { e.stopPropagation(); deleteTask(task.id) }}>🗑</button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App