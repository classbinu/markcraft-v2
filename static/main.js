// 강의실 이동
function go(url) {
  window.location.href = url;
}

// 회원가입 시 비밀번호 일치 확인
function checkPasswordMatch() {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm_password").value;
  const passwordInfo = document.getElementById("password_info");
  const submitButton = document.getElementById("submit_button");

  if (password === confirmPassword) {
    passwordInfo.innerHTML = "비밀번호가 일치합니다.";
    passwordInfo.classList.add("text-success");
    passwordInfo.classList.remove("text-error");
    submitButton.disabled = false;
    return true;
  } else {
    passwordInfo.innerHTML = "비밀번호가 일치하지 않습니다.";
    passwordInfo.classList.add("text-error");
    passwordInfo.classList.remove("text-success");
    submitButton.disabled = true;
    return false;
  }
}

// 밀리세컨드를 00:00 형식으로 변환
function millisecondsToMinutesSeconds(milliseconds) {
  let seconds = Math.floor(milliseconds / 1000);
  let minutes = Math.floor(seconds / 60);
  const formattedTime =
    (minutes < 10 ? "0" : "") +
    minutes +
    ":" +
    (seconds < 10 ? "0" : "") +
    seconds;

  return formattedTime;
}

function logout(cookieName) {
  document.cookie =
    cookieName + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  window.location.href = "/";
}

// 연습장 마크다운 동적 실시간 렌더링
function initializeRealTimeRendering() {
  const practiceInput = document.getElementById("practiceInput");
  const previewOutput = document.getElementById("previewOutput");

  practiceInput.addEventListener("input", function () {
    previewOutput.innerHTML = marked(practiceInput.value);
    console.log(marked(practiceInput.value), previewOutput.innerHTML);

    document.querySelectorAll("pre code").forEach((block) => {
      hljs.highlightBlock(block);
    });
  });
}

function resetAllContext() {
  const textarea = document.getElementById("practiceInput");
  textarea.value = "";
  const preview = document.getElementById("previewOutput");
  preview.textContent = "";
}

// 강의실 마크다운 정적 렌더링
function markdownStaticRendering() {
  const question = document.getElementById("question").value;
  const previewOutput = document.getElementById("previewOutput");
  previewOutput.innerHTML = marked(question);
  console.log(previewOutput.innerHTML);
}

// 여러 줄 들어가는 예시 데이터
function staticRendering() {
  const previewOutput = document.getElementById("previewOutput");
  const html = document.getElementById("html");
  previewOutput.innerHTML = html.value;
}

function checkAnswer() {
  let question;
  let answer = document.getElementById("answer");
  console.log(answer.value);
  // const chapter_id = parseInt(document.getElementById("chapter_id").innerText);
  if (/\n/.test(answer.value)) {
    question = document.getElementById("previewOutput");
    question = question.innerHTML;
    let value = marked(answer.value);
    // 개행문자 제거
    value = value.replace(/\n/g, "");
    answer = value;
  } else {
    answer = answer.value;
    question = document.getElementById("question").value;
  }
  // question = question.trim();
  // answer = answer.trim();
  console.log(`"${question}"`);
  console.log(`"${answer}"`);

  console.log(question);
  console.log(answer);

  console.log(question === answer);
  if (question === answer) {
    Swal.fire({
      position: "center",
      icon: "success",
      title: "정답입니다!",
      showConfirmButton: false,
      timer: 1500,
    });
    setTimeout(() => {
      location.reload();
    }, 1500);
  }
}

// 강의실 내 최종 진도 업데이트
// 내 기록 업데이트하기
async function postUpdateMyProgress(progress) {
  const url = "/progress";

  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ progress }),
  };

  try {
    const response = await fetch(url, options);

    if (!response.ok) {
      throw new Error("네트워크 오류 발생");
    }

    const data = await response.json();
    console.log("서버 응답:", data);
  } catch (error) {
    console.error("오류 발생:", error);
  }
}

// 강의실 정답보기
function showAnswerModal() {
  const question = document.getElementById("html").value;
  const answerEl = document.getElementById("answer");
  const convert = convertHtmlToMarkdown(question);
  console.log(convert);

  Swal.fire({
    html: `${convert}`,
    focusConfirm: false,
  }).then(() => {
    setTimeout(() => answerEl.focus(), 300);
  });
}
