const analyzePolicy = async () => {
  if (!file && !text.trim()) {
    alert("Upload a PDF or paste policy text");
    return;
  }

  setLoading(true);

  try {
    const formData = new FormData();

    if (file !== null) {
      formData.append("file", file);
    }

    if (file === null) {
      formData.append("text", text);
    }

    const response = await axios.post(
      "http://127.0.0.1:8000/analyze",
      formData
    );

    setResult(response.data);
  } catch (err) {
    console.error("AXIOS ERROR:", err);
    alert("Backend did not accept input");
  } finally {
    setLoading(false);
  }
};
