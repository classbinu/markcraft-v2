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

// 강의실, 타임어택
// 예제 example 데이터

function classRoom() {}

function timeAttack() {
  // function updateProgressBar(index) {
  //   const progressBar = document.getElementById("progress-bar");
  //   progressBar.max = example.questions.length;
  //   progressBar.value = index + 1;
  // }
  // function updateProgressText(index) {
  //   const progressText = document.getElementById("progress-text");
  //   progressText.textContent = `${index + 1}/${example.questions.length}`;
  // }
  // updateProgressBar(currentQuestionIndex);
  // updateProgressText(currentQuestionIndex);
  // const userInput = document.getElementById("userInput");
  // const correctOutput = document.getElementById("correctOutput");
  // function convertTimeFormat(milliseconds) {
  //   let minutes = Math.floor(milliseconds / (60 * 1000));
  //   let seconds = Math.floor((milliseconds % (60 * 1000)) / 1000);
  //   return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(
  //     2,
  //     "0"
  //   )}`;
}

// 1. 타이머를 위한 변수 설정
// let timerInterval;
// let startTime;
// let myTime;
// let timeDisplay = document.getElementById("currentTime");

// 2. 시작 버튼 클릭 이벤트 리스너 추가
// document.querySelector(".btn-success").addEventListener("click", function () {
//   this.style.display = "none"; // 시작 버튼 숨기기
//   startTimer();
//   // 처음 문제 로드
//   loadQuestion(currentQuestionIndex);
// });

// 3. 타이머 시작/정지 함수
//   function startTimer() {
//     startTime = Date.now();
//     timerInterval = setInterval(function () {
//       myTime = Date.now() - startTime;
//       timeDisplay.textContent = convertTimeFormat(myTime);
//     }, 10);
//   }

//   function stopTimer() {
//     clearInterval(timerInterval);
//     timerInterval = null;
//   }

//   // 문제가 모두 완료되었을 때 타이머를 멈추고 모달을 띄움
//   function completeChallenges() {
//     // postMyTime(myTime);
//     const question = document.getElementById("question").textContent;
//     const answer = document.getElementById("answer").textContent;
//     if (question === answer) {
//       Swal.fire({
//         position: "center",
//         icon: "success",
//         title: "정답입니다!",
//         showConfirmButton: false,
//         timer: 1500,
//       });
//       setTimeout(() => {
//         location.reload();
//       }, 1500);
//     }
//   }
//   function loadQuestion(index) {
//     console.log(index);
//     updateProgressBar(index);
//     updateProgressText(index);
//     // 문제 불러오기
//     userInput.value = example.questions[index].userPrompt;
//     correctOutput.innerHTML = marked(example.questions[index].correctAnswer);
//     correctOutput.style.display = "block"; // 정답 미리보기 보이기
//     userInput.focus();
//   }

//   userInput.addEventListener("input", function () {
//     // userOutput.innerHTML = marked(userInput.value); // 사용자 입력을 미리보기에 표시ㄴ
//     document.querySelectorAll("pre code").forEach((block) => {
//       hljs.highlightBlock(block); // 코드 하이라이팅
//     });

//     if (marked(userInput.value).trim() === correctOutput.innerHTML.trim()) {
//       // 문제를 모두 풀면 모달을 보여주는 코드
//       if (currentQuestionIndex === example.questions.length - 1) {
//         stopTimer();
//         completeChallenges();
//       } else {
//         loadNextQuestion();
//       }
//     }
//   });
//   // 다음 문제 로드 함수
//   function loadNextQuestion() {
//     currentQuestionIndex++;
//     if (currentQuestionIndex < example.questions.length) {
//       loadQuestion(currentQuestionIndex);
//       console.log(currentQuestionIndex);
//     }
//   }
// }

// 연습장 마크다운 동적 실시간 렌더링
function initializeRealTimeRendering() {
  const practiceInput = document.getElementById("practiceInput");
  const previewOutput = document.getElementById("previewOutput");

  practiceInput.addEventListener("input", function () {
    previewOutput.innerHTML = marked(practiceInput.value);
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
}

function checkAnswer() {
  const question = document.getElementById("question").value;
  const answer = document.getElementById("answer").value;
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
  const question = document.getElementById("question").value;
  const answerEl = document.getElementById("answer");
  Swal.fire({
    text: question,
    focusConfirm: false,
  }).then(() => {
    setTimeout(() => answerEl.focus(), 300);
  });
}
