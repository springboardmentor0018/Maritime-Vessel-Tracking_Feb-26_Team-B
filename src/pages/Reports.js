import React, { useEffect, useState } from "react";
import "../styles/reports.css";

function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  // ✅ Fetch reports (mock now, backend later)
  useEffect(() => {
    // 🔹 Replace this with real API later
    const mockData = [
      {
        id: 1,
        title: "Monthly Vessel Activity Report",
        description: "Overview of vessel movements and activities",
        date: "March 2026",
        type: "PDF",
        size: "2.4 MB",
        fileUrl: "/files/report1.pdf",
      },
      {
        id: 2,
        title: "Risk Assessment Summary",
        description: "Analysis of maritime risks",
        date: "March 2026",
        type: "PDF",
        size: "1.8 MB",
        fileUrl: "/files/report2.pdf",
      },
      {
        id: 3,
        title: "Port Performance Metrics",
        description: "Port efficiency analytics",
        date: "February 2026",
        type: "Excel",
        size: "3.1 MB",
        fileUrl: "/files/report3.xlsx",
      },
      {
        id: 4,
        title: "Insurance Claims Analysis",
        description: "Claims and policy performance",
        date: "Q1 2026",
        type: "PDF",
        size: "2.7 MB",
        fileUrl: "/files/report4.pdf",
      },
    ];

    setTimeout(() => {
      setReports(mockData);
      setLoading(false);
    }, 500);
  }, []);

  // ✅ Download handler (backend-ready)
  const handleDownload = (report) => {
    // 🔥 FUTURE BACKEND VERSION:
    // window.open(`http://localhost:5000/api/reports/${report.id}/download`);

    // ✅ CURRENT (mock download)
    const link = document.createElement("a");
    link.href = report.fileUrl;
    link.download = report.title;
    link.click();
  };

  // ✅ Generate report button
  const handleGenerateReport = () => {
    alert("Report generation started (connect backend later)");
  };

  return (
    <div className="reports-container">
      
      {/* HEADER */}
      <div className="reports-header">
        <div>
          <h2>Reports</h2>
          <p>Generate and download analytical reports</p>
        </div>

        <button className="generate-btn" onClick={handleGenerateReport}>
          Generate New Report
        </button>
      </div>

      {/* LOADING */}
      {loading ? (
        <p>Loading reports...</p>
      ) : (
        <div className="reports-grid">
          
          {reports.map((report) => (
            <div key={report.id} className="report-card">

              <div className="report-icon">📊</div>

              <h3>{report.title}</h3>
              <p className="desc">{report.description}</p>

              <div className="report-meta">
                <span>📅 {report.date}</span>
                <span>{report.type} • {report.size}</span>
              </div>

              <button
                className="download-btn"
                onClick={() => handleDownload(report)}
              >
                ⬇ Download
              </button>

            </div>
          ))}

        </div>
      )}
    </div>
  );
}

export default Reports;