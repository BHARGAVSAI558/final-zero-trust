import { useState, useEffect } from "react";
import axios from "axios";

const API = axios.create({ baseURL: "http://localhost:8000" });

export default function FileManager() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [content, setContent] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [recycleBin, setRecycleBin] = useState([]);
  const [showRecycle, setShowRecycle] = useState(false);
  const username = localStorage.getItem("username") || "user";

  useEffect(() => {
    loadFiles();
    const interval = setInterval(loadFiles, 3000);
    return () => clearInterval(interval);
  }, []);

  const loadFiles = async () => {
    try {
      const [filesRes, recycleRes] = await Promise.all([
        API.get("/files/list").catch(() => ({ data: { files: [] } })),
        API.get("/files/recycle-bin").catch(() => ({ data: { files: [] } }))
      ]);
      setFiles(filesRes.data.files || []);
      setRecycleBin(recycleRes.data.files || []);
    } catch (err) {
      console.error("Load error:", err);
    }
  };

  const handleOpen = async (filename) => {
    try {
      console.log('Opening file:', filename);
      const res = await API.get(`/files/read/${filename}?user=${username}`);
      console.log('File opened successfully');
      setSelectedFile(filename);
      setContent(res.data.content);
      setIsEditing(false);
    } catch (err) {
      console.error('Open error details:', err.response?.data || err.message);
      alert("Error opening file: " + (err.response?.data?.detail || err.message));
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = async () => {
    try {
      console.log('Saving file:', { filename: selectedFile, content, user: username });
      const response = await API.post("/files/edit", { 
        filename: selectedFile, 
        content, 
        user: username 
      });
      console.log('Save response:', response.data);
      alert("File saved successfully");
      setIsEditing(false);
      loadFiles();
    } catch (err) {
      console.error('Save error details:', err.response?.data || err.message);
      alert("Error saving: " + (err.response?.data?.detail || err.message));
    }
  };

  const handleDelete = async (filename) => {
    if (!window.confirm(`Delete ${filename}?`)) return;
    try {
      await API.post("/files/delete", { filename, user: username });
      alert("File moved to recycle bin");
      setSelectedFile(null);
      loadFiles();
    } catch (err) {
      alert("Error deleting: " + err.message);
    }
  };

  const handleRestore = async (filename) => {
    try {
      await API.post("/files/restore", { filename, user: username });
      alert("File restored");
      loadFiles();
    } catch (err) {
      alert("Error restoring: " + err.message);
    }
  };

  const getSensitivityColor = (level) => {
    const colors = {
      critical: "bg-red-500/20 text-red-300 border-red-500/50",
      sensitive: "bg-orange-500/20 text-orange-300 border-orange-500/50",
      internal: "bg-yellow-500/20 text-yellow-300 border-yellow-500/50",
      public: "bg-green-500/20 text-green-300 border-green-500/50"
    };
    return colors[level] || colors.internal;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="bg-gray-800/80 backdrop-blur rounded-2xl border border-blue-500/30 shadow-2xl overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6 flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-semibold text-white">File Manager</h1>
              <p className="text-blue-100 text-sm mt-1">Document Management System</p>
            </div>
            <div className="flex gap-3">
              <button onClick={() => window.location.href = '/soc'} className="px-4 py-2 bg-white/20 hover:bg-white/30 text-white text-sm font-medium rounded-lg transition-colors">
                SOC Dashboard
              </button>
              <button onClick={() => window.location.href = '/admin'} className="px-4 py-2 bg-white/20 hover:bg-white/30 text-white text-sm font-medium rounded-lg transition-colors">
                Admin
              </button>
              <button onClick={() => window.location.href = '/files'} className="px-4 py-2 bg-white/20 hover:bg-white/30 text-white text-sm font-medium rounded-lg transition-colors">
                Portal
              </button>
            </div>
          </div>

          <div className="flex gap-4 p-4 bg-gray-900/50">
            <button onClick={() => setShowRecycle(false)} className={`px-6 py-2 rounded-lg font-semibold transition ${!showRecycle ? "bg-blue-600 text-white" : "bg-gray-700 text-gray-300 hover:bg-gray-600"}`}>
              Files ({files.length})
            </button>
            <button onClick={() => setShowRecycle(true)} className={`px-6 py-2 rounded-lg font-semibold transition ${showRecycle ? "bg-blue-600 text-white" : "bg-gray-700 text-gray-300 hover:bg-gray-600"}`}>
              Recycle Bin ({recycleBin.length})
            </button>
          </div>

          <div className="grid grid-cols-3 gap-6 p-6">
            <div className="col-span-1 space-y-2 max-h-[600px] overflow-y-auto">
              {!showRecycle ? (
                files.length === 0 ? (
                  <div className="text-center text-gray-500 py-8">No files</div>
                ) : (
                  files.map((file, i) => (
                    <div key={i} onClick={() => handleOpen(file.name)} className={`p-4 rounded-lg border cursor-pointer transition hover:scale-105 ${selectedFile === file.name ? "bg-blue-600/30 border-blue-500" : "bg-gray-800/50 border-gray-700 hover:border-blue-500/50"}`}>
                      <div className="flex justify-between items-start mb-2">
                        <span className="text-white font-semibold text-sm truncate">{file.name}</span>
                        <span className={`px-2 py-0.5 rounded text-xs font-bold border ${getSensitivityColor(file.sensitivity)}`}>
                          {file.sensitivity.toUpperCase()}
                        </span>
                      </div>
                      <div className="text-xs text-gray-400">{(file.size / 1024).toFixed(1)} KB</div>
                      <div className="text-xs text-gray-500">{new Date(file.modified).toLocaleString()}</div>
                    </div>
                  ))
                )
              ) : (
                recycleBin.length === 0 ? (
                  <div className="text-center text-gray-500 py-8">Recycle bin empty</div>
                ) : (
                  recycleBin.map((file, i) => (
                    <div key={i} className="p-4 rounded-lg border bg-gray-800/50 border-gray-700">
                      <div className="text-white font-semibold text-sm mb-2">{file.original_name}</div>
                      <div className="text-xs text-gray-400 mb-3">{new Date(file.deleted).toLocaleString()}</div>
                      <button onClick={() => handleRestore(file.name)} className="w-full px-3 py-1.5 bg-green-600 hover:bg-green-500 text-white rounded text-xs font-semibold transition">
                        RESTORE
                      </button>
                    </div>
                  ))
                )
              )}
            </div>

            <div className="col-span-2">
              {selectedFile ? (
                <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6 h-full flex flex-col">
                  <div className="flex justify-between items-center mb-4">
                    <h2 className="text-xl font-bold text-white">{selectedFile}</h2>
                    <div className="flex gap-2">
                      {!isEditing ? (
                        <>
                          <button onClick={handleEdit} className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-semibold transition">
                            ✏️ EDIT
                          </button>
                          <button onClick={() => handleDelete(selectedFile)} className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg text-sm font-semibold transition">
                            🗑️ DELETE
                          </button>
                        </>
                      ) : (
                        <>
                          <button onClick={handleSave} className="px-4 py-2 bg-green-600 hover:bg-green-500 text-white rounded-lg text-sm font-semibold transition">
                            💾 SAVE
                          </button>
                          <button onClick={() => setIsEditing(false)} className="px-4 py-2 bg-gray-600 hover:bg-gray-500 text-white rounded-lg text-sm font-semibold transition">
                            ✖️ CANCEL
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                  <textarea value={content} onChange={(e) => setContent(e.target.value)} readOnly={!isEditing} className={`flex-1 w-full p-4 rounded-lg font-mono text-sm ${isEditing ? "bg-gray-900 text-white border-2 border-blue-500" : "bg-gray-900/50 text-gray-300 border border-gray-700"} focus:outline-none resize-none`} />
                </div>
              ) : (
                <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6 h-full flex items-center justify-center">
                  <div className="text-center text-gray-500">
                    <div className="text-6xl mb-4">📄</div>
                    <div className="text-lg">Select a file to view</div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
