import {useEffect, useState} from "react"
import './App.css';

function App() {

  const [livros,setLivros]= useState([])
  useEffect(() =>{async function get_livro(){
    const resposta=await fetch('http://127.0.0.1:5000/api/books')
    const livro=await resposta.json()
    setLivros(livro)
}

get_livro()},[]) 

  return (
    <div  class="row">
      {livros.map((livro)=>(<div class="card blue">
        <div id="titulo">
          <h2>{livro.name}</h2></div>
        <div id="autor">
          <p>{livro.author}</p></div>
        <div id="description">
            {livro.description}
        </div>
      </div>))}
    </div>
  );
}

export default App;
