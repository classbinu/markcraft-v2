// 강의실 이동
function go(url) {
  window.location.href = url;
}

// 강의실, 타임어택
// 예제 JSON 데이터
const jsonData = {
  questions: [
    {
      id: 1,
      userPrompt: "This is inline code.",
      correctAnswer: "This is `inline code`.",
    },
    // {
    //   "id": 2,
    //   "userPrompt": "",
    //   "correctAnswer": "가나다"
    // },
    // {
    //   "id": 3,
    //   "userPrompt": "이것은 제목",
    //   "correctAnswer": "## 이것은 제목"
    // },
    // {
    //   "id": 4,
    //   "userPrompt": "여기에 본문을 입력하세요.\n\n이것은 강조된 텍스트입니다.",
    //   "correctAnswer": "여기에 본문을 입력하세요.\n\n이것은 **강조된** 텍스트입니다."
    // }
    // 추가적인 문제들...
  ],
};

// 현재 문제 인덱스
let currentQuestionIndex = 0;
const userInput = document.getElementById("userInput");
const userOutput = document.getElementById("userOutput");
const correctOutput = document.getElementById("correctOutput");
const comparisonResult = document.getElementById("comparisonResult");
const questionsContainer = document.getElementById("questionsContainer");

// 현재 최고 기록
let bestTime = document.getElementById("bestTime");
bestTime.textContent = localStorage.getItem("bestTime")
  ? parseInt(localStorage.getItem("bestTime"))
  : Infinity;

// 1. 타이머를 위한 변수 설정
let timerInterval;
let startTime;
let timeDisplay = document.getElementById("currentTime");

function convertTimeFormat(milliseconds) {
  let minutes = Math.floor(milliseconds / (60 * 1000));
  let seconds = Math.floor((milliseconds % (60 * 1000)) / 1000);
  let ms = milliseconds % 1000;

  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(
    2,
    "0"
  )}:${String(ms).padStart(3, "0")}`;
}

// 2. 시작 버튼 클릭 이벤트 리스너 추가
document.querySelector(".btn-success").addEventListener("click", function () {
  this.style.display = "none"; // 시작 버튼 숨기기
  startTimer();
  // 처음 문제 로드
  loadQuestion(currentQuestionIndex);
});

// 3. 타이머 시작/정지 함수
function startTimer() {
  startTime = Date.now();
  timerInterval = setInterval(function () {
    let elapsedTime = Date.now() - startTime;
    timeDisplay.textContent = convertTimeFormat(elapsedTime);
  }, 10);
}

function stopTimer() {
  clearInterval(timerInterval);
  timerInterval = null;
}

// 문제가 모두 완료되었을 때 타이머를 멈추고 모달을 띄움
function completeChallenges() {
  stopTimer();
  showModal();
}

// 모달을 보여주는 함수
function showModal() {
  let completionModal = document.getElementById("completionModal");
  let completionTime = document.getElementById("completionTime");

  let currentScore = timeDisplay.textContent;
  if (currentScore < bestTime) {
    // 폭죽 애니메이션 추가
    let fireworks = document.createElement("div");
    fireworks.className = "fireworks";
    document.body.appendChild(fireworks);
    setTimeout(() => {
      document.body.removeChild(fireworks);
    }, 1000);
    bestTime = currentScore;
    localStorage.setItem("bestTime", bestTime);
    // 추가: 최고 기록 UI 업데이트
    completionTime.textContent = `축하합니다! 최고 기록을 경신하셨습니다!!\n\n걸린 시간: ${currentScore}`;
  } else {
    completionTime.textContent = `완료까지 걸린 시간: ${currentScore}`;
  }

  completionModal.style.display = "block";
}

// 모달을 닫는 함수
function closeModal() {
  let completionModal = document.getElementById("completionModal");
  completionModal.style.display = "none";
  location.reload();
}

function loadQuestion(index) {
  console.log(index);
  // 문제 불러오기
  userInput.value = jsonData.questions[index].userPrompt;
  correctOutput.innerHTML = marked(jsonData.questions[index].correctAnswer);
  correctOutput.style.display = "block"; // 정답 미리보기 보이기
  userInput.focus();
}

userInput.addEventListener("input", function () {
  // userOutput.innerHTML = marked(userInput.value); // 사용자 입력을 미리보기에 표시ㄴ
  document.querySelectorAll("pre code").forEach((block) => {
    hljs.highlightBlock(block); // 코드 하이라이팅
  });

  if (marked(userInput.value).trim() === correctOutput.innerHTML.trim()) {
    // comparisonResult.textContent = "정답입니다!";
    // comparisonResult.style.color = "green";
    // userInput.style.borderColor = "#ccc";
    // 문제를 모두 풀면 모달을 보여주는 코드
    if (currentQuestionIndex === jsonData.questions.length - 1) {
      completeChallenges();
    } else {
      // setTimeout(loadNextQuestion, 2000);
      loadNextQuestion();
    }
  } else {
    // comparisonResult.textContent = "틀렸습니다. 다시 시도해보세요.";
    // comparisonResult.style.color = "red";
    // userInput.style.borderColor = "red";
  }
});

// 다음 문제 로드 함수
function loadNextQuestion() {
  currentQuestionIndex++;
  if (currentQuestionIndex < jsonData.questions.length) {
    loadQuestion(currentQuestionIndex);
    console.log(currentQuestionIndex);
  }
}

// 노트 실시간 렌더링
// const userInput = document.getElementById("userInput");
// const preview = document.getElementById("preview");

// console.log(userInput);
// console.log(preview);
// userInput.addEventListener("input", function () {
//   preview.innerHTML = marked(userInput.value);
//   document.querySelectorAll("pre code").forEach((block) => {
//     hljs.highlightBlock(block);
//   });
// });
