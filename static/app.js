(function () {
  "use strict";

  const textarea = document.getElementById("newsInput");
  const charCount = document.getElementById("charCount");
  const analyzeBtn = document.getElementById("analyzeBtn");
  const clearBtn = document.getElementById("clearBtn");
  const exampleBtn = document.getElementById("exampleBtn");
  const apiStatus = document.getElementById("apiStatus");

  const resultArea = document.getElementById("resultArea");
  const resultCard = document.getElementById("resultCard");
  const resultBadge = document.getElementById("resultBadge");
  const resultConfidence = document.getElementById("resultConfidence");
  const resultExplain = document.getElementById("resultExplain");
  const resultTime = document.getElementById("resultTime");
  const copyBtn = document.getElementById("copyBtn");

  const errorArea = document.getElementById("errorArea");

  const historySection = document.getElementById("historySection");
  const historyList = document.getElementById("historyList");

  const EXAMPLES = [
    "Scientists reveal that drinking hot water cures cancer overnight. Share this before it gets deleted!",
    "The Reserve Bank of India announced a 0.25 percent increase in the benchmark interest rate on Wednesday. The announcement was made during a press briefing.",
    "An anonymous whistleblower claims a secret government cure for aging is being hidden from the public. Mainstream media refuses to report this.",
  ];

  let lastResult = null;
  let history = [];

  function updateCharCount() {
    charCount.textContent = String(textarea.value.length);
  }

  function setLoading(isLoading) {
    analyzeBtn.disabled = isLoading;
    analyzeBtn.textContent = isLoading ? "Analyzing…" : "Analyze";
  }

  function showError(message) {
    errorArea.textContent = message;
    errorArea.hidden = false;
    resultArea.hidden = true;
  }

  function hideError() {
    errorArea.hidden = true;
  }

  function checkHealth() {
    fetch("/health")
      .then((res) => res.json().then((body) => ({ ok: res.ok, body })))
      .then(({ ok, body }) => {
        if (ok) {
          apiStatus.textContent = "Model ready";
          apiStatus.className = "api-status is-online";
        } else {
          apiStatus.textContent = body.message || "Model unavailable";
          apiStatus.className = "api-status is-offline";
        }
      })
      .catch(() => {
        apiStatus.textContent = "Backend unreachable";
        apiStatus.className = "api-status is-offline";
      });
  }

  function renderResult(data, text) {
    const isReal = data.prediction === "REAL";

    resultCard.classList.toggle("is-real", isReal);
    resultCard.classList.toggle("is-fake", !isReal);

    resultBadge.textContent = isReal ? "REAL NEWS" : "FAKE NEWS";
    resultConfidence.textContent = data.confidence.toFixed(1) + "% confidence";

    resultExplain.textContent = isReal
      ? "This text's wording patterns are closer to the reported-news examples the model was trained on."
      : "This text's wording patterns are closer to the fabricated-news examples the model was trained on.";

    const now = new Date();
    const timeLabel = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    resultTime.textContent = "Analyzed at " + timeLabel;

    resultArea.hidden = false;
    hideError();

    lastResult = { prediction: data.prediction, confidence: data.confidence, text, time: timeLabel };
    addToHistory(lastResult);
  }

  function addToHistory(entry) {
    history.unshift(entry);
    history = history.slice(0, 8);

    historyList.innerHTML = "";
    history.forEach((item) => {
      const li = document.createElement("li");

      const tag = document.createElement("span");
      tag.className = "tag " + (item.prediction === "REAL" ? "real" : "fake");
      tag.textContent = item.prediction;

      const snippet = document.createElement("span");
      snippet.className = "snippet";
      snippet.textContent = item.text;

      const when = document.createElement("span");
      when.className = "when";
      when.textContent = item.time;

      li.appendChild(tag);
      li.appendChild(snippet);
      li.appendChild(when);
      historyList.appendChild(li);
    });

    historySection.hidden = history.length === 0;
  }

  function analyze() {
    const text = textarea.value.trim();

    if (text.length < 10) {
      showError("Please enter at least 10 characters of news text before analyzing.");
      return;
    }

    hideError();
    setLoading(true);

    fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    })
      .then((res) => res.json().then((body) => ({ ok: res.ok, body })))
      .then(({ ok, body }) => {
        if (!ok) {
          throw new Error(body.error || "Something went wrong while analyzing.");
        }
        renderResult(body, text);
      })
      .catch((err) => {
        showError(err.message || "Could not reach the analysis service.");
      })
      .finally(() => setLoading(false));
  }

  function clearAll() {
    textarea.value = "";
    updateCharCount();
    resultArea.hidden = true;
    hideError();
    textarea.focus();
  }

  function insertExample() {
    const example = EXAMPLES[Math.floor(Math.random() * EXAMPLES.length)];
    textarea.value = example;
    updateCharCount();
    hideError();
    textarea.focus();
  }

  function copyResult() {
    if (!lastResult) return;
    const summary = `${lastResult.prediction} (${lastResult.confidence.toFixed(1)}% confidence) — "${lastResult.text}"`;
    navigator.clipboard.writeText(summary).then(() => {
      const original = copyBtn.textContent;
      copyBtn.textContent = "Copied";
      setTimeout(() => { copyBtn.textContent = original; }, 1500);
    });
  }

  textarea.addEventListener("input", updateCharCount);
  analyzeBtn.addEventListener("click", analyze);
  clearBtn.addEventListener("click", clearAll);
  exampleBtn.addEventListener("click", insertExample);
  copyBtn.addEventListener("click", copyResult);

  textarea.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      analyze();
    }
  });

  updateCharCount();
  checkHealth();
})();
