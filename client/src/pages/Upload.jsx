import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

function Upload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post("/resume/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage(`Uploaded successfully: ${response.data.file_name}`);
    } catch (err) {
      if (err.response?.status === 401) {
        navigate("/login");
      } else {
        setMessage(
          "Upload failed: " + (err.response?.data?.detail || err.message),
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "400px",
        margin: "60px auto",
        fontFamily: "sans-serif",
      }}
    >
      <h2>Upload Your Resume</h2>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
          style={{ marginBottom: "12px" }}
        />
        <br />
        <button
          type="submit"
          disabled={loading}
          style={{ padding: "10px 20px" }}
        >
          {loading ? "Uploading..." : "Upload"}
        </button>
      </form>
      {message && <p style={{ marginTop: "12px" }}>{message}</p>}
    </div>
  );
}

export default Upload;
