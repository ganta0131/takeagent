import formidable from "formidable";
import fs from "fs";

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method Not Allowed" });
  }

  const form = new formidable.IncomingForm();

  form.parse(req, async (err, fields, files) => {
    if (err) {
      console.error("form parse error:", err);
      return res.status(500).json({ error: "ファイル解析エラー" });
    }

    const pdfFile = files.pdf;
    if (!pdfFile) {
      return res.status(400).json({ error: "PDFファイルがありません" });
    }

    // ファイルを一時保存（Vercel環境なら/tmpに保存可能）
    const data = fs.readFileSync(pdfFile.filepath);

    // ここでGoogle Cloud Vision APIに渡す処理を後で実装予定

    res.status(200).json({ message: "ファイル受け取り成功" });
  });
}
