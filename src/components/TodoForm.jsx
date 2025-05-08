import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { addTodo } from '../store/todoSlice'; // nouveau chemin

function TodoForm() {
  const [input, setInput] = useState('');
  const dispatch = useDispatch();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() === '') return;
    dispatch(addTodo(input));
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Nouvelle tâche"
      />
      <button type="submit">Ajouter</button>
    </form>
  );
}

export default TodoForm;
