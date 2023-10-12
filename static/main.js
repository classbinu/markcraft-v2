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
  seconds = seconds % 60;
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

// 모달을 보여주는 함수
function showModal() {
  let completionModal = document.getElementById("completionModal");
  let completionTime = document.getElementById("completionTime");
  completionModal.style.display = "block";
}

// 모달을 닫는 함수
function closeModal() {
  let completionModal = document.getElementById("completionModal");
  completionModal.style.display = "none";
  location.reload();
}

function timeAttack() {
  // 현재 문제 인덱스
  let currentQuestionIndex = 0;
  // 예제문제
  const example = {
    questions: [
      {
        id: 1,
        userPrompt: "This is inline code.",
        correctAnswer: "This is `inline code`.",
      },
      // {
      //   id: 2,
      //   userPrompt: "",
      //   correctAnswer: "가나다",
      // },
      // {
      //   id: 3,
      //   userPrompt: "이것은 제목",
      //   correctAnswer: "## 이것은 제목",
      // },
      // {
      //   id: 4,
      //   userPrompt: "여기에 본문을 입력하세요.\n\n이것은 강조된 텍스트입니다.",
      //   correctAnswer:
      //     "여기에 본문을 입력하세요.\n\n이것은 **강조된** 텍스트입니다.",
      // },
    ],
  };
  async function getBestTime() {
    const response = await fetch("/besttime", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    console.log(data.value);
  }

  function updateProgressBar(index) {
    const progressBar = document.getElementById("progress-bar");
    progressBar.max = example.questions.length;
    progressBar.value = index + 1;
  }

  function updateProgressText(index) {
    const progressText = document.getElementById("progress-text");
    progressText.textContent = `${index + 1}/${example.questions.length}`;
  }
  getBestTime();
  updateProgressBar(currentQuestionIndex);
  updateProgressText(currentQuestionIndex);
  const userInput = document.getElementById("userInput");
  const userOutput = document.getElementById("userOutput");
  const correctOutput = document.getElementById("correctOutput");
  const comparisonResult = document.getElementById("comparisonResult");
  const questionsContainer = document.getElementById("questionsContainer");

  function convertTimeFormat(milliseconds) {
    let minutes = Math.floor(milliseconds / (60 * 1000));
    let seconds = Math.floor((milliseconds % (60 * 1000)) / 1000);
    let ms = milliseconds % 1000;

    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(
      2,
      "0"
    )}:${String(ms).padStart(3, "0")}`;
  }

  // 1. 타이머를 위한 변수 설정
  let timerInterval;
  let startTime;
  let totalTime;
  let timeDisplay = document.getElementById("currentTime");

  // 현재 최고 기록
  // let max_best = 51 * 60000;
  // let bestTime = document.getElementById("bestTime");
  // console.log(convertTimeFormat(max_best));
  // if (!localStorage.getItem("bestTime")) {
  //   localStorage.setItem("bestTime", max_best);
  // }
  // bestTime.textContent = convertTimeFormat(localStorage.getItem("bestTime"));

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
      totalTime = Date.now() - startTime;
      timeDisplay.textContent = convertTimeFormat(totalTime);
    }, 10);
  }

  function stopTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
  }

  function storedBestTime(time) {
    return fetch("/timeattack", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ bestTime: time }),
    }).then((response) => response.json());
  }
  // 문제가 모두 완료되었을 때 타이머를 멈추고 모달을 띄움
  function completeChallenges() {
    if (totalTime < localStorage.getItem("bestTime")) {
      storedBestTime(totalTime);
      // // 최고 기록 UI 업데이트
      // document.getElementById("bestTime").textContent = bestTime;

      // 폭죽 이펙트 실행
      document.getElementById("particles-js").style.display = "block";
      setTimeout(function () {
        document.getElementById("particles-js").style.display = "none";
      }, 2000); // 2초 후 폭죽 이펙트 숨김

      // 모달 메시지 변경
      document.getElementById(
        "completionTime"
      ).textContent = `축하합니다! 최고 기록을 경신하셨습니다!!\n\n걸린 시간: ${timeDisplay.textContent}`;
    } else {
      document.getElementById(
        "completionTime"
      ).textContent = `완료까지 걸린 시간: ${timeDisplay.textContent}`;
    }
    showModal();
  }
  particlesJS("particles-js", {
    particles: {
      number: {
        value: 100,
      },
      size: {
        value: 3,
      },
      line_linked: {
        enable: false,
      },
      move: {
        direction: "top",
        speed: 2,
      },
    },
    interactivity: {
      events: {
        onclick: {
          enable: true,
          mode: "repulse",
        },
      },
      modes: {
        repulse: {
          distance: 200,
          duration: 0.4,
        },
      },
    },
  });

  function loadQuestion(index) {
    console.log(index);
    updateProgressBar(index);
    updateProgressText(index);
    // 문제 불러오기
    userInput.value = example.questions[index].userPrompt;
    correctOutput.innerHTML = marked(example.questions[index].correctAnswer);
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
      if (currentQuestionIndex === example.questions.length - 1) {
        stopTimer();
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
    if (currentQuestionIndex < example.questions.length) {
      loadQuestion(currentQuestionIndex);
      console.log(currentQuestionIndex);
    }
  }
}

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

// 강의실 마크다운 정적 렌더링
function markdownStaticRendering() {
  const question = document.getElementById("question").value;
  const markdown = document.getElementById("markdown");
  markdown.innerHTML = marked(question);
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
