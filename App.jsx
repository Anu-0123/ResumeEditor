import React, { useState } from "react";
import html2pdf from "html2pdf.js";

function App() {
  const [resume, setResume] = useState({
    name: "Anusree Anu",
    skills: "HTML, CSS, JavaScript",
    education: "BCA, Final Year",
    experience: "Fresher",
  });

  const handleChange = (e) => {
    setResume({ ...resume, [e.target.name]: e.target.value });
  };

  const saveResume = () => {
    const id = `resume_${Date.now()}`;
    localStorage.setItem(id, JSON.stringify(resume));
    alert(`Resume saved with ID: ${id}`);
  };

  const loadResume = (id) => {
    const data = localStorage.getItem(id);
    if (data) {
      setResume(JSON.parse(data));
    } else {
      alert("Resume ID not found.");
    }
  };

  const downloadResume = () => {
    const element = document.getElementById("resume-preview");

    // Wait a moment to let the content render before generating PDF
    setTimeout(() => {
      html2pdf().from(element).set({
        margin: 10,
        filename: "My_Resume.pdf",
        html2canvas: { scale: 2 },
        jsPDF: { format: "a4", orientation: "portrait" },
      }).save();
    }, 100);
  };

  return (
    <div className="App" style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>Resume Editor</h2>

      <div style={{ display: "flex", flexDirection: "column", gap: "10px", maxWidth: "500px" }}>
        <label>Name:</label>
        <input name="name" value={resume.name} onChange={handleChange} />

        <label>Skills:</label>
        <input name="skills" value={resume.skills} onChange={handleChange} />

        <label>Education:</label>
        <input name="education" value={resume.education} onChange={handleChange} />

        <label>Experience:</label>
        <input name="experience" value={resume.experience} onChange={handleChange} />
      </div>

      <div style={{ marginTop: "20px" }}>
        <button onClick={saveResume}>Save Resume</button>
        <button onClick={() => loadResume(prompt("Enter Resume ID"))}>Load Resume</button>
        <button onClick={downloadResume}>Download Resume</button>
      </div>

      <h3 style={{ marginTop: "40px" }}>Resume Preview</h3>
      <div
        id="resume-preview"
        style={{
          padding: "20px",
          backgroundColor: "#ffffff",
          color: "#000000",
          width: "600px",
          margin: "0 auto",
          border: "1px solid #ccc",
        }}
      >
        <h2>{resume.name}</h2>
        <p><strong>Skills:</strong> {resume.skills}</p>
        <p><strong>Education:</strong> {resume.education}</p>
        <p><strong>Experience:</strong> {resume.experience}</p>
      </div>
    </div>
  );
}

export default App;


