document.addEventListener('DOMContentLoaded', function() {
  const questionInput = document.getElementById('questionInput');
  const sendButton = document.getElementById('sendButton');
  const chatMessages = document.getElementById('chatMessages');

  // 메시지 추가 함수
  function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const icon = document.createElement('div');
    icon.className = 'message-icon';
    icon.textContent = isUser ? '👤' : '🤖';
    
    const text = document.createElement('div');
    text.className = 'message-text';
    text.textContent = content;
    
    messageDiv.appendChild(icon);
    messageDiv.appendChild(text);
    chatMessages.appendChild(messageDiv);
    
    // 스크롤 최하단으로
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // 로딩 메시지 추가/제거
  function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot-message loading';
    loadingDiv.id = 'loadingMessage';
    loadingDiv.innerHTML = '<div class="message-icon">🤖</div><div class="message-text">답변 생성 중...</div>';
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function hideLoading() {
    const loading = document.getElementById('loadingMessage');
    if (loading) loading.remove();
  }

  // 메시지 전송
  async function sendMessage() {
    const question = questionInput.value.trim();
    if (!question) return;

    // 사용자 메시지 표시
    addMessage(question, true);
    questionInput.value = '';
    sendButton.disabled = true;

    // 로딩 표시
    showLoading();

    try {
      const formData = new FormData();
      formData.append('question', question);

      const response = await fetch('/chat/ask/', {
        method: 'POST',
        body: formData
      });

      hideLoading();

      if (!response.ok) {
        throw new Error('서버 응답 오류');
      }

      const data = await response.json();
      addMessage(data.answer, false);

    } catch (error) {
      hideLoading();
      addMessage('오류가 발생했습니다: ' + error.message, false);
      console.error('Error:', error);
    } finally {
      sendButton.disabled = false;
      questionInput.focus();
    }
  }

  // 이벤트 리스너
  sendButton.addEventListener('click', sendMessage);
  
  questionInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      sendMessage();
    }
  });

  // 초기 포커스
  questionInput.focus();
});
