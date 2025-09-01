const getResults = async (mood) => {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/analyze-mood", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ mood }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching recommendations:", error);
    return null;
  }
};

export default getResults;
