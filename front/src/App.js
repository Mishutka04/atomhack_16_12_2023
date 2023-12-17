import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [inputText, setInputText] = useState('');
  const [generatedText, setGeneratedText] = useState('');
  const [error, setError] = useState(null);

  const generateAnswer = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/generate-answer/', { input_text: inputText });
      setGeneratedText(response.data.generated_text);
      setError(null);
    } catch (error) {
      console.error('Error:', error);
      setError('Error generating text');
    }
  };

  return (
    <div
      style={{
        backgroundColor: '#ffffff',
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <header style={{ padding: '20px', textAlign: 'center', backgroundColor: '#f0f0f0', color: '#333333' }}>
        <h1>Rosatom's Digital Solutions</h1>
        <p>Empowering Innovation, Ensuring Sovereignty</p>
      </header>
      <main style={{ flex: 1, padding: '20px', display: 'flex', flexDirection: 'column', alignItems: 'center', backgroundImage: 'none' }}>
        <img src="https://rosatom.ru/upload/medialibrary/c60/c607008c0fdf7aa368dc54c96c11b739.jpg" alt="Your Image" style={{ width: '100%', height: 'auto' }} />
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          style={{
            backgroundColor: '#add8e6',
            color: '#000000',
            padding: '10px',
            marginBottom: '10px',
            height: '200px',
            width: '80%',
          }}
        />
        <br />
        <button
          onClick={generateAnswer}
          style={{
            backgroundColor: '#3e4095',
            color: '#ffffff',
            padding: '10px',
            border: 'none',
            cursor: 'pointer',
          }}
        >
          Generate Answer
        </button>
        <div style={{ marginTop: '20px', color: '#000000', fontSize: '20px', width: '80%' }}>
          {generatedText && <strong>Generated Text:</strong>} {generatedText}
        </div>
        {error && (
          <div style={{ marginTop: '20px', color: '#d2222a' }}>
            <strong>Error:</strong> {error}
          </div>
        )}
      </main>
      <footer style={{ padding: '20px', textAlign: 'center', backgroundColor: '#f0f0f0', color: '#333333' }}>
        <p>&copy; 2023 Rosatom Digital Solutions. All rights reserved.</p>
        <p>Developed with Innovation and Safety in Mind</p>
      </footer>

    </div>
  );
}

export default App;
