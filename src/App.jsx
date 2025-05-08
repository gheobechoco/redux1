
import './App.css';
import React from 'react'; // Import React
import TodoForm from './components/TodoForm.jsx';
import TodoList from './components/TodoList.jsx';

function App() {
  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Todo List avec redux</h1>
      <TodoForm />
      <TodoList />
    </div>
  );
}

export default App;