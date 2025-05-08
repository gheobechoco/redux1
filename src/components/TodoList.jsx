import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { removeTodo } from '../store/todoSlice'; // nouveau chemin

function TodoList() {
  const todos = useSelector((state) => state.todos);
  const dispatch = useDispatch();

  return (
    <ul>
      {todos.map((todo, index) => (
        <li key={index}>
          {todo}
          <button onClick={() => dispatch(removeTodo(index))}>Supprimer</button>
        </li>
      ))}
    </ul>
  );
}

export default TodoList;
