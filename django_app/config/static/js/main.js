document.getElementById("myForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const answerDiv = document.getElementById("answer");
  answerDiv.innerText = "답변 생성 중...";

  try {
    const question = document.getElementById("question").value;

    const response = await fetch("/chat/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    if (!response.ok) {
      throw new Error("서버 응답 오류");
    }

    const data = await response.json();
    answerDiv.innerText = data.answer;

  } catch (err) {
    answerDiv.innerText = "오류가 발생했습니다.";
  }
});
