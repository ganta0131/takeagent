import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected && selected.type === "application/pdf") {
      setFile(selected);
      setMessage("");
    } else {
      setMessage("PDFファイルを選択してください");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("ファイルが選択されていません");
      return;
    }
    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const res = await fetch("/api/upload-pdf", {
        method: "POST",
        body: formData,
      });
      if (res.ok) {
        setMessage("アップロード成功！");
      } else {
        setMessage("アップロード失敗しました");
      }
    } catch (error) {
      setMessage("通信エラーです");
    }
  };

  return (
    <div style={{ maxWidth: 320, margin: "auto", padding: 20 }}>
      <h2>給食・下校時刻PDFアップロード</h2>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ marginTop: 10 }}>
        アップロード
      </button>
      <p>{message}</p>
    </div>
  );
}
