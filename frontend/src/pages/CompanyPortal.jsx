import { useState, useEffect } from "react";
import axios from "axios";

const API = axios.create({ baseURL: "http://localhost:8000" });

// SVG Icons as components
const UploadIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>;
const SearchIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>;
const EyeIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>;
const DownloadIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>;
const EditIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>;
const DeleteIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>;
const LogoutIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>;
const DocumentIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>;
const ChartIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>;
const UsersIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>;
const FolderIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" /></svg>;
const RocketIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>;

export default function CompanyPortal() {
  const user = localStorage.getItem("username") || "user";
  const [activeTab, setActiveTab] = useState("dashboard");
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [notification, setNotification] = useState("");

  const [selectedReport, setSelectedReport] = useState(null);
  const [reportData, setReportData] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    if (activeTab === "documents") {
      loadFiles();
    }
  }, [activeTab]);

  const handleViewReport = (reportName) => {
    const mockData = {
      "Q1 Revenue": {
        title: "Q1 2024 Revenue Report",
        summary: "Total revenue increased by 12% compared to Q4 2023",
        data: [
          { month: "January", amount: "₹68 L", growth: "+8%" },
          { month: "February", amount: "₹72 L", growth: "+15%" },
          { month: "March", amount: "₹70 L", growth: "+10%" }
        ],
        total: "₹2.1 Cr",
        insights: ["Strong performance in enterprise sales", "New client acquisitions up 25%", "Recurring revenue stable"]
      },
      "Q2 Expenses": {
        title: "Q2 2024 Expense Analysis",
        summary: "Operating expenses reduced by 5% through cost optimization",
        data: [
          { category: "Personnel", amount: "₹95 L", percentage: "53%" },
          { category: "Technology", amount: "₹42 L", percentage: "23%" },
          { category: "Operations", amount: "₹43 L", percentage: "24%" }
        ],
        total: "₹1.8 Cr",
        insights: ["Reduced cloud infrastructure costs", "Optimized staffing levels", "Negotiated better vendor contracts"]
      },
      "Annual Budget": {
        title: "2024 Annual Budget Overview",
        summary: "Budget allocation across departments with 8% increase from 2023",
        data: [
          { department: "Engineering", budget: "₹3.4 Cr", allocation: "40%" },
          { department: "Sales & Marketing", budget: "₹2.55 Cr", allocation: "30%" },
          { department: "Operations", budget: "₹1.7 Cr", allocation: "20%" },
          { department: "Administration", budget: "₹85 L", allocation: "10%" }
        ],
        total: "₹8.5 Cr",
        insights: ["Increased R&D investment", "Expanded sales team", "New market expansion budget"]
      },
      "Tax Documents": {
        title: "2024 Tax Documentation Status",
        summary: "All required tax documents prepared and filed",
        data: [
          { document: "Corporate Tax Return", status: "Filed", date: "March 15, 2024" },
          { document: "Quarterly Estimates", status: "Paid", date: "January 15, 2024" },
          { document: "Employee Tax Forms", status: "Distributed", date: "January 31, 2024" },
          { document: "Sales Tax Returns", status: "Current", date: "Monthly" }
        ],
        total: "100% Compliance",
        insights: ["No outstanding tax obligations", "All deadlines met", "Audit-ready documentation"]
      }
    };
    setReportData(mockData[reportName]);
    setSelectedReport(reportName);
  };

  const loadFiles = async () => {
    try {
      const res = await API.get("/files/list");
      setFiles(res.data.files || []);
    } catch (err) {
      console.error("Load error:", err);
    }
  };

  const showNotification = (msg) => {
    setNotification(msg);
    setTimeout(() => setNotification(""), 3000);
  };

  const handleOpen = async (filename) => {
    try {
      // Track file access
      await API.post('/files/access', {
        user_id: user,
        file_name: filename,
        action: 'READ'
      });
      
      // Track network activity
      await API.post('/track/network', {
        username: user,
        remote_ip: '127.0.0.1',
        remote_port: 3000,
        protocol: 'HTTPS',
        is_external: false
      });
      
      const res = await API.get(`/files/read/${filename}?user=${user}`);
      const fileExt = filename.split('.').pop().toLowerCase();
      
      if (['pdf', 'xlsx', 'xls', 'docx', 'doc'].includes(fileExt)) {
        showNotification(`${fileExt.toUpperCase()} files can only be downloaded, not viewed in browser`);
        return;
      }
      
      setSelectedFile(filename);
      setFileContent(res.data.content);
      setIsEditing(false);
      showNotification(`Opened: ${filename}`);
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  const handleDownload = async (filename) => {
    try {
      // Track file access
      await API.post('/files/access', {
        user_id: user,
        file_name: filename,
        action: 'DOWNLOAD'
      });
      
      // Track network activity
      await API.post('/track/network', {
        username: user,
        remote_ip: '127.0.0.1',
        remote_port: 3000,
        protocol: 'HTTPS',
        is_external: false
      });
      
      const res = await API.get(`/files/read/${filename}?user=${user}&action=download`);
      const fileExt = filename.split('.').pop().toLowerCase();
      let mimeType = 'text/plain';
      
      if (fileExt === 'pdf') mimeType = 'application/pdf';
      else if (fileExt === 'xlsx' || fileExt === 'xls') mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
      else if (fileExt === 'docx' || fileExt === 'doc') mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
      
      const blob = new Blob([res.data.content], { type: mimeType });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.click();
      window.URL.revokeObjectURL(url);
      showNotification(`Downloaded: ${filename}`);
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  const handleEdit = () => {
    // Track file access
    API.post('/files/access', {
      user_id: user,
      file_name: selectedFile,
      action: 'EDIT'
    });
    
    setIsEditing(true);
    showNotification("Editing mode enabled");
  };

  const handleSave = async () => {
    try {
      await API.post("/files/edit", { filename: selectedFile, content: fileContent, user });
      
      // Track network activity
      await API.post('/track/network', {
        username: user,
        remote_ip: '127.0.0.1',
        remote_port: 3000,
        protocol: 'HTTPS',
        is_external: false
      });
      
      setIsEditing(false);
      showNotification("File saved successfully");
      loadFiles();
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  const handleDelete = async (filename) => {
    if (!window.confirm(`Delete ${filename}?`)) return;
    try {
      // Track file access
      await API.post('/files/access', {
        user_id: user,
        file_name: filename,
        action: 'DELETE'
      });
      
      await API.post("/files/delete", { filename, user });
      showNotification(`Deleted: ${filename}`);
      setSelectedFile(null);
      loadFiles();
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50" style={{fontFamily: 'Inter, system-ui, -apple-system, sans-serif'}}>
      <style>{`
        ::-webkit-scrollbar {
          width: 8px;
          height: 8px;
        }
        ::-webkit-scrollbar-track {
          background: #f1f5f9;
        }
        ::-webkit-scrollbar-thumb {
          background: #94a3b8;
          border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background: #64748b;
        }
      `}</style>
      {notification && (
        <div className="fixed top-4 right-4 z-50 bg-blue-600 text-white px-6 py-3 rounded-lg shadow-lg">
          {notification}
        </div>
      )}

      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-semibold text-sm">
                TC
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">TechCorp Portal</h1>
                <p className="text-xs text-gray-500">Enterprise Platform</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <div className="text-sm font-medium text-gray-900">{user}</div>
                <div className="text-xs text-gray-500">Employee</div>
              </div>
              <button onClick={() => window.location.href = '/login'} className="px-4 py-2 bg-gray-900 hover:bg-gray-800 text-white text-sm font-medium rounded-lg transition-colors flex items-center gap-2">
                <LogoutIcon />
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex gap-1">
            {[
              {key: "dashboard", label: "Dashboard", Icon: ChartIcon},
              {key: "documents", label: "Documents", Icon: FolderIcon},
              {key: "employees", label: "Employees", Icon: UsersIcon},
              {key: "projects", label: "Projects", Icon: RocketIcon},
              {key: "reports", label: "Reports", Icon: DocumentIcon}
            ].map(tab => (
              <button key={tab.key} onClick={() => setActiveTab(tab.key)} className={`px-4 py-3 text-sm font-medium transition-colors flex items-center gap-2 ${
                activeTab === tab.key 
                  ? "text-blue-600 border-b-2 border-blue-600" 
                  : "text-gray-600 hover:text-gray-900"
              }`}>
                <tab.Icon />
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {activeTab === "dashboard" && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-2xl font-semibold text-gray-900">Dashboard Overview</h2>
                <p className="text-sm text-gray-500 mt-1">Business Intelligence & Analytics</p>
              </div>
              <div className="text-sm text-gray-500">Last updated: {new Date().toLocaleString()}</div>
            </div>
            
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[
                { title: "Total Revenue", value: "₹4.2 Cr", change: "+18%", color: "green" },
                { title: "Active Projects", value: "6", change: "+2", color: "blue" },
                { title: "Team Members", value: "156", change: "+12", color: "purple" },
                { title: "Documents", value: "248", change: "+35", color: "orange" }
              ].map((stat, i) => (
                <div key={i} className={`bg-gradient-to-br from-white to-${stat.color}-50 rounded-xl shadow-md border border-${stat.color}-200 p-6 hover:shadow-xl transition-all duration-300`}>
                  <div className="flex justify-between items-start mb-3">
                    <div className="text-sm font-medium text-gray-600">{stat.title}</div>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold shadow-sm bg-${stat.color}-500 text-white`}>
                      {stat.change}
                    </span>
                  </div>
                  <div className="text-3xl font-bold text-gray-900">{stat.value}</div>
                </div>
              ))}
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Recent Activity */}
              <div className="lg:col-span-2 bg-white rounded-xl shadow-md border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
                <div className="space-y-4">
                  {[
                    { user: "Bhargav Sai", action: "approved budget for Q3", time: "2 hours ago", type: "success" },
                    { user: "Jeshwanth", action: "deployed new security patch", time: "4 hours ago", type: "info" },
                    { user: "Sanjay", action: "submitted financial report", time: "6 hours ago", type: "success" },
                    { user: "Yakoob", action: "onboarded 3 new employees", time: "1 day ago", type: "info" },
                    { user: "Bhargav Sai", action: "reviewed project milestones", time: "1 day ago", type: "warning" },
                    { user: "Jeshwanth", action: "updated system architecture", time: "2 days ago", type: "info" }
                  ].map((activity, i) => (
                    <div key={i} className="flex items-start gap-4 p-3 rounded-lg hover:bg-gray-50 transition-colors">
                      <div className={`w-2 h-2 rounded-full mt-2 ${
                        activity.type === 'success' ? 'bg-green-500' :
                        activity.type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
                      }`}></div>
                      <div className="flex-1">
                        <p className="text-sm text-gray-900">
                          <span className="font-semibold">{activity.user}</span> {activity.action}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Stats */}
              <div className="space-y-6">
                {/* Department Performance */}
                <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Department Performance</h3>
                  <div className="space-y-4">
                    {[
                      { dept: "Engineering", score: 92 },
                      { dept: "Sales", score: 88 },
                      { dept: "Finance", score: 95 },
                      { dept: "HR", score: 85 }
                    ].map((dept, i) => (
                      <div key={i}>
                        <div className="flex justify-between text-sm mb-2">
                          <span className="font-medium text-gray-700">{dept.dept}</span>
                          <span className="font-bold text-gray-900">{dept.score}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div className="h-2 rounded-full bg-gray-700" style={{width: `${dept.score}%`}}></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Upcoming Deadlines */}
                <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Upcoming Deadlines</h3>
                  <div className="space-y-3">
                    {[
                      { task: "Security Audit", date: "Feb 15", priority: "high" },
                      { task: "Website Launch", date: "Mar 10", priority: "high" },
                      { task: "Q1 Review", date: "Mar 31", priority: "medium" },
                      { task: "Budget Planning", date: "Apr 05", priority: "low" }
                    ].map((item, i) => (
                      <div key={i} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex-1">
                          <p className="text-sm font-medium text-gray-900">{item.task}</p>
                          <p className="text-xs text-gray-500 mt-1">{item.date}</p>
                        </div>
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                          item.priority === 'high' ? 'bg-red-500 text-white' :
                          item.priority === 'medium' ? 'bg-yellow-500 text-white' :
                          'bg-blue-500 text-white'
                        }`}>{item.priority}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Financial Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl shadow-lg p-6 text-white">
                <div className="text-sm font-medium opacity-90 mb-2">Total Revenue</div>
                <div className="text-3xl font-bold mb-1">₹4.2 Cr</div>
                <div className="text-sm opacity-80">+18% from last quarter</div>
              </div>
              <div className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl shadow-lg p-6 text-white">
                <div className="text-sm font-medium opacity-90 mb-2">Total Expenses</div>
                <div className="text-3xl font-bold mb-1">₹2.8 Cr</div>
                <div className="text-sm opacity-80">-5% cost optimization</div>
              </div>
              <div className="bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl shadow-lg p-6 text-white">
                <div className="text-sm font-medium opacity-90 mb-2">Net Profit</div>
                <div className="text-3xl font-bold mb-1">₹1.4 Cr</div>
                <div className="text-sm opacity-80">+25% growth</div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "documents" && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-2xl font-semibold text-gray-900">Document Library</h2>
                <p className="text-sm text-gray-500 mt-1">Manage and organize your files</p>
              </div>
              <div className="flex gap-3">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Search documents..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <div className="absolute left-3 top-2.5 text-gray-400">
                    <SearchIcon />
                  </div>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
              <table className="w-full">
                <thead className="bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-gray-200">
                  <tr>
                    <th className="text-left px-6 py-3 text-xs font-medium text-blue-700 uppercase tracking-wider">Document</th>
                    <th className="text-left px-6 py-3 text-xs font-medium text-purple-700 uppercase tracking-wider">Type</th>
                    <th className="text-left px-6 py-3 text-xs font-medium text-green-700 uppercase tracking-wider">Size</th>
                    <th className="text-left px-6 py-3 text-xs font-medium text-orange-700 uppercase tracking-wider">Modified</th>
                    <th className="text-right px-6 py-3 text-xs font-medium text-gray-700 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {files.filter(file => 
                    file.name.toLowerCase().includes(searchQuery.toLowerCase())
                  ).map((file, i) => (
                    <tr key={i} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 bg-blue-100 rounded flex items-center justify-center flex-shrink-0">
                            <DocumentIcon />
                          </div>
                          <span className="text-sm font-medium text-gray-900">{file.name}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        {file.sensitivity === "critical" ? (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">
                            Critical
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                            Internal
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500">{(file.size / 1024).toFixed(1)} KB</td>
                      <td className="px-6 py-4 text-sm text-gray-500">{new Date(file.modified).toLocaleDateString()}</td>
                      <td className="px-6 py-4">
                        <div className="flex justify-end gap-2">
                          <button onClick={() => handleOpen(file.name)} className="p-2 text-blue-600 hover:text-blue-700 bg-blue-50 hover:bg-blue-100 rounded transition-colors" title="View">
                            <EyeIcon />
                          </button>
                          <button onClick={() => handleDownload(file.name)} className="p-2 text-green-600 hover:text-green-700 bg-green-50 hover:bg-green-100 rounded transition-colors" title="Download">
                            <DownloadIcon />
                          </button>
                          <button onClick={() => { handleOpen(file.name); setTimeout(handleEdit, 500); }} className="p-2 text-amber-600 hover:text-amber-700 bg-amber-50 hover:bg-amber-100 rounded transition-colors" title="Edit">
                            <EditIcon />
                          </button>
                          <button onClick={() => handleDelete(file.name)} className="p-2 text-red-600 hover:text-red-700 bg-red-50 hover:bg-red-100 rounded transition-colors" title="Delete">
                            <DeleteIcon />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === "employees" && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-2xl font-semibold text-gray-900">Employee Directory</h2>
                <p className="text-sm text-gray-500 mt-1">Corporate Team Management</p>
              </div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
              <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                {[
                  { name: "Bhargav Sai", title: "Chief Executive Officer", email: "bhargav.sai@techcorp.com", phone: "+91 9963545576", dept: "Executive" },
                  { name: "Jeshwanth", title: "Chief Technology Officer", email: "jeshwanth@techcorp.com", phone: "+91 9959085863", dept: "Technology" },
                  { name: "Sanjay", title: "Chief Financial Officer", email: "sanjay@techcorp.com", phone: "+91 9542038156", dept: "Finance" },
                  { name: "Yakoob", title: "Human Resources Director", email: "yakoob@techcorp.com", phone: "+91 9568210478", dept: "HR" }
                ].map((emp, i) => (
                  <div key={i} className="border border-gray-200 rounded-lg p-6 hover:bg-gray-50 transition-colors">
                    <div className="flex items-start gap-4 mb-4">
                      <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-lg flex-shrink-0">
                        {emp.name.split(' ').map(n => n[0]).join('')}
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900">{emp.name}</h3>
                        <p className="text-sm text-gray-600">{emp.title}</p>
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800 mt-2">
                          {emp.dept}
                        </span>
                      </div>
                    </div>
                    <div className="space-y-2 text-sm text-gray-600">
                      <div>{emp.email}</div>
                      <div>{emp.phone}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === "projects" && (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-semibold text-gray-900">Active Projects</h2>
              <p className="text-sm text-gray-500 mt-1">Project Portfolio Management</p>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {[
                { 
                  name: "Website Redesign", 
                  budget: "₹5 L", 
                  progress: 75, 
                  status: "In Progress",
                  lead: "Jeshwanth",
                  team: "8 members",
                  deadline: "Mar 2024",
                  priority: "High"
                },
                { 
                  name: "Mobile Application", 
                  budget: "₹12 L", 
                  progress: 45, 
                  status: "Development",
                  lead: "Sanjay",
                  team: "12 members",
                  deadline: "Jun 2024",
                  priority: "Critical"
                },
                { 
                  name: "Cloud Migration", 
                  budget: "₹20 L", 
                  progress: 20, 
                  status: "Planning",
                  lead: "Bhargav Sai",
                  team: "6 members",
                  deadline: "Sep 2024",
                  priority: "Medium"
                },
                { 
                  name: "AI Analytics Platform", 
                  budget: "₹18 L", 
                  progress: 60, 
                  status: "In Progress",
                  lead: "Jeshwanth",
                  team: "10 members",
                  deadline: "May 2024",
                  priority: "High"
                },
                { 
                  name: "Security Audit System", 
                  budget: "₹8 L", 
                  progress: 85, 
                  status: "Testing",
                  lead: "Yakoob",
                  team: "5 members",
                  deadline: "Feb 2024",
                  priority: "Critical"
                },
                { 
                  name: "Customer Portal v2", 
                  budget: "₹15 L", 
                  progress: 30, 
                  status: "Development",
                  lead: "Sanjay",
                  team: "9 members",
                  deadline: "Aug 2024",
                  priority: "Medium"
                }
              ].map((proj, i) => (
                <div key={i} className="bg-white p-6 rounded-lg shadow-md border border-gray-200 hover:shadow-xl hover:border-blue-300 transition-all duration-300">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">{proj.name}</h3>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold shadow-sm ${
                      proj.status === 'In Progress' ? 'bg-blue-500 text-white' :
                      proj.status === 'Development' ? 'bg-green-500 text-white' :
                      proj.status === 'Testing' ? 'bg-purple-500 text-white' :
                      'bg-yellow-500 text-white'
                    }`}>{proj.status}</span>
                  </div>
                  <div className="space-y-3 mb-4">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Budget:</span>
                      <span className="font-semibold text-gray-900">{proj.budget}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Project Lead:</span>
                      <span className="font-medium text-gray-900">{proj.lead}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Team Size:</span>
                      <span className="font-medium text-gray-900">{proj.team}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Deadline:</span>
                      <span className="font-medium text-gray-900">{proj.deadline}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Priority:</span>
                      <span className={`px-2.5 py-1 rounded-full text-xs font-semibold shadow-sm ${
                        proj.priority === 'Critical' ? 'bg-red-500 text-white' :
                        proj.priority === 'High' ? 'bg-orange-500 text-white' :
                        'bg-blue-500 text-white'
                      }`}>{proj.priority}</span>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-600">Progress:</span>
                      <span className="font-semibold text-gray-900">{proj.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className={`h-2 rounded-full ${
                        proj.progress >= 70 ? 'bg-green-500' :
                        proj.progress >= 40 ? 'bg-blue-500' : 'bg-yellow-500'
                      }`} style={{width: `${proj.progress}%`}}></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === "reports" && (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-semibold text-gray-900">Financial Reports</h2>
              <p className="text-sm text-gray-500 mt-1">Business Intelligence & Analytics</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {[
                { 
                  name: "Q1 Revenue", 
                  value: "₹2.1 Cr", 
                  change: "+12%",
                  period: "Jan - Mar 2024",
                  category: "Revenue",
                  status: "Completed"
                },
                { 
                  name: "Q2 Expenses", 
                  value: "₹1.8 Cr", 
                  change: "-5%",
                  period: "Apr - Jun 2024",
                  category: "Expenses",
                  status: "Completed"
                },
                { 
                  name: "Annual Budget", 
                  value: "₹8.5 Cr", 
                  change: "+8%",
                  period: "FY 2024",
                  category: "Budget",
                  status: "Active"
                },
                { 
                  name: "Tax Documents", 
                  value: "2024", 
                  change: "Complete",
                  period: "FY 2024",
                  category: "Compliance",
                  status: "Filed"
                },
                { 
                  name: "Q3 Forecast", 
                  value: "₹2.4 Cr", 
                  change: "+18%",
                  period: "Jul - Sep 2024",
                  category: "Projection",
                  status: "Draft"
                },
                { 
                  name: "Profit & Loss", 
                  value: "₹45 L", 
                  change: "+22%",
                  period: "H1 2024",
                  category: "Financial",
                  status: "Completed"
                }
              ].map((rep, i) => (
                <div key={i} className="bg-gradient-to-br from-white to-gray-50 p-6 rounded-xl shadow-md border border-gray-200 hover:shadow-xl hover:border-blue-300 transition-all duration-300">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900">{rep.name}</h3>
                      <p className="text-sm text-gray-500 mt-1">{rep.period}</p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold shadow-sm ${
                      rep.status === 'Completed' ? 'bg-green-500 text-white' :
                      rep.status === 'Active' ? 'bg-blue-500 text-white' :
                      rep.status === 'Draft' ? 'bg-yellow-500 text-white' :
                      'bg-purple-500 text-white'
                    }`}>{rep.status}</span>
                  </div>
                  <div className="space-y-3">
                    <div>
                      <p className="text-3xl font-bold text-gray-900">{rep.value}</p>
                      <p className={`text-sm font-medium mt-1 ${
                        rep.change.includes('+') ? 'text-green-600' :
                        rep.change.includes('-') ? 'text-red-600' : 'text-blue-600'
                      }`}>{rep.change}</p>
                    </div>
                    <div className="flex justify-between items-center pt-3 border-t border-gray-200">
                      <span className="text-sm text-gray-600">Category: <span className="font-medium text-gray-900">{rep.category}</span></span>
                      <button onClick={() => handleViewReport(rep.name)} className="px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white text-sm font-semibold rounded-lg shadow-md hover:shadow-lg transition-all duration-200">
                        View Report
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Report Modal */}
      {selectedReport && reportData && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={() => setSelectedReport(null)}>
          <div className="bg-white rounded-xl p-8 max-w-4xl w-full max-h-[90vh] overflow-y-auto shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-3xl font-bold text-gray-900">{reportData.title}</h2>
                <p className="text-gray-600 mt-2">{reportData.summary}</p>
              </div>
              <button onClick={() => setSelectedReport(null)} className="text-gray-500 hover:text-gray-700 text-3xl font-bold">×</button>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-4">Detailed Breakdown</h3>
                <div className="space-y-4">
                  {reportData.data.map((item, i) => (
                    <div key={i} className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex justify-between items-center">
                        <span className="font-semibold text-gray-800">{Object.values(item)[0]}</span>
                        <span className="font-bold text-blue-600">{Object.values(item)[1]}</span>
                      </div>
                      {Object.values(item)[2] && (
                        <div className="text-sm text-gray-600 mt-1">{Object.values(item)[2]}</div>
                      )}
                    </div>
                  ))}
                </div>
                <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                  <div className="flex justify-between items-center">
                    <span className="text-lg font-bold text-gray-900">Total:</span>
                    <span className="text-2xl font-bold text-blue-600">{reportData.total}</span>
                  </div>
                </div>
              </div>
              
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-4">Key Insights</h3>
                <div className="space-y-3">
                  {reportData.insights.map((insight, i) => (
                    <div key={i} className="flex items-start gap-3">
                      <div className="w-2 h-2 bg-blue-600 rounded-full mt-2"></div>
                      <span className="text-gray-700">{insight}</span>
                    </div>
                  ))}
                </div>
                
                <div className="mt-8 flex gap-3">
                  <button onClick={() => {
                    const element = document.createElement('a');
                    const content = `${reportData.title}\n\n${reportData.summary}\n\nDetailed Breakdown:\n${reportData.data.map(item => Object.values(item).join(' - ')).join('\n')}\n\nTotal: ${reportData.total}\n\nKey Insights:\n${reportData.insights.map((ins, i) => `${i+1}. ${ins}`).join('\n')}`;
                    const file = new Blob([content], {type: 'text/plain'});
                    element.href = URL.createObjectURL(file);
                    element.download = `${selectedReport.replace(/ /g, '_')}_Report.txt`;
                    element.click();
                  }} className="px-6 py-3 bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white rounded-lg font-semibold shadow-md hover:shadow-lg transition-all duration-200 flex items-center gap-2">
                    <DownloadIcon />
                    Download Report
                  </button>
                  <button onClick={() => setSelectedReport(null)} className="px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-medium transition-colors duration-200">
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* File Viewer Modal */}
      {selectedFile && (
        <div className="fixed inset-0 bg-gray-900/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={() => setSelectedFile(null)}>
          <div className="bg-white rounded-lg shadow-2xl max-w-5xl w-full max-h-[90vh] overflow-hidden" onClick={(e) => e.stopPropagation()}>
            {/* Modal Header */}
            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4 flex justify-between items-center">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-white/20 rounded flex items-center justify-center">
                  <DocumentIcon />
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-white">{selectedFile}</h2>
                  <p className="text-xs text-blue-100">Document Viewer</p>
                </div>
              </div>
              <button onClick={() => setSelectedFile(null)} className="text-white hover:bg-white/20 rounded-lg p-2 transition-colors">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            {/* Modal Content */}
            <div className="p-6 overflow-y-auto" style={{maxHeight: 'calc(90vh - 180px)'}}>
              {!isEditing ? (
                <div className="bg-black border border-gray-700 rounded-lg p-6">
                  <pre className="text-sm text-gray-100 whitespace-pre-wrap font-mono leading-relaxed">{fileContent}</pre>
                </div>
              ) : (
                <textarea 
                  value={fileContent} 
                  onChange={(e) => setFileContent(e.target.value)} 
                  className="w-full h-96 p-4 bg-black border border-gray-700 text-gray-100 rounded-lg font-mono text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  placeholder="Enter file content..."
                />
              )}
            </div>
            
            {/* Modal Footer */}
            <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-between items-center">
              <div className="text-xs text-gray-500">
                {isEditing ? 'Editing mode' : 'View mode'}
              </div>
              <div className="flex gap-2">
                {!isEditing ? (
                  <>
                    <button onClick={handleEdit} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors flex items-center gap-2">
                      <EditIcon />
                      Edit
                    </button>
                    <button onClick={() => handleDownload(selectedFile)} className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors flex items-center gap-2">
                      <DownloadIcon />
                      Download
                    </button>
                    <button onClick={() => handleDelete(selectedFile)} className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-medium rounded-lg transition-colors flex items-center gap-2">
                      <DeleteIcon />
                      Delete
                    </button>
                  </>
                ) : (
                  <>
                    <button onClick={handleSave} className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors">
                      Save Changes
                    </button>
                    <button onClick={() => setIsEditing(false)} className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white text-sm font-medium rounded-lg transition-colors">
                      Cancel
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}