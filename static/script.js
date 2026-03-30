// script.js — DevPath client-side logic
// Handles: skill chip manager, form validation, API calls,
//          result card rendering, and the code viewer panel.

// ============================================================
// Determine which page we are on by checking for key elements
// ============================================================
var isIndexPage   = !!document.getElementById("recommend-form");
var isDetailPage  = typeof PROJECT_ID !== "undefined";


// ============================================================
// INDEX PAGE LOGIC
// ============================================================
if (isIndexPage) {

  // --- DOM references ---
  var form             = document.getElementById("recommend-form");
  var submitBtn        = document.getElementById("submit-btn");
  var btnLabel         = document.getElementById("btn-label");
  var btnLoading       = document.getElementById("btn-loading");
  var resultsSection   = document.getElementById("results-section");
  var resultsGrid      = document.getElementById("results-grid");
  var resultsLoading   = document.getElementById("results-loading");
  var resultsEmpty     = document.getElementById("results-empty");
  var emptyMessage     = document.getElementById("empty-message");
  var skillsHidden     = document.getElementById("skills");
  var skillsInput      = document.getElementById("skills-input");
  var chipsSelected    = document.getElementById("skill-chips-selected");
  var availableChips   = document.querySelectorAll(".skill-chip");

  // Holds the list of skills the user has added
  var selectedSkills = [];


  // ----------------------------------------------------------
  // Skill chip manager
  // ----------------------------------------------------------

  // Add a skill when user presses Enter in the text box
  skillsInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      var value = skillsInput.value.trim();
      if (value) {
        addSkill(value);
        skillsInput.value = "";
      }
    }
  });

  // Add a skill when user clicks one of the quick-pick chips
  availableChips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var skill = chip.getAttribute("data-skill");
      if (skill) {
        addSkill(skill);
        chip.classList.add("active"); // Mark the chip as selected
      }
    });
  });

  // Focus the text input when the user clicks anywhere inside the wrap
  var skillWrap = document.querySelector(".skill-input-wrap");
  if (skillWrap) {
    skillWrap.addEventListener("click", function () {
      skillsInput.focus();
    });
  }

  function addSkill(skill) {
    // Prevent duplicate entries (case-insensitive check)
    var lower = skill.toLowerCase();
    var exists = selectedSkills.some(function (s) {
      return s.toLowerCase() === lower;
    });
    if (exists) return;

    selectedSkills.push(skill);
    renderSelectedChips();
    syncHiddenField();
    clearFieldError("skills-error");
  }

  function removeSkill(skill) {
    // Remove skill from the array and re-render
    selectedSkills = selectedSkills.filter(function (s) {
      return s !== skill;
    });
    renderSelectedChips();
    syncHiddenField();

    // Un-highlight the quick-pick chip if it matches
    availableChips.forEach(function (chip) {
      if (chip.getAttribute("data-skill") === skill) {
        chip.classList.remove("active");
      }
    });
  }

  function renderSelectedChips() {
    // Clear and rebuild the chips inside the input wrap
    chipsSelected.innerHTML = "";
    selectedSkills.forEach(function (skill) {
      var chip = document.createElement("span");
      chip.className = "skill-chip-selected";
      chip.textContent = skill;

      // Remove button on each chip
      var removeBtn = document.createElement("button");
      removeBtn.type = "button";
      removeBtn.className = "skill-chip-remove";
      removeBtn.innerHTML = "&times;";
      removeBtn.setAttribute("aria-label", "Remove " + skill);
      removeBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        removeSkill(skill);
      });

      chip.appendChild(removeBtn);
      chipsSelected.appendChild(chip);
    });
  }

  function syncHiddenField() {
    // Keep the hidden input in sync so the form can read the value
    skillsHidden.value = selectedSkills.join(", ");
  }


  // ----------------------------------------------------------
  // Form validation helpers
  // ----------------------------------------------------------

  function showFieldError(fieldId, message) {
    var el = document.getElementById(fieldId);
    if (el) el.textContent = message;
  }

  function clearFieldError(fieldId) {
    var el = document.getElementById(fieldId);
    if (el) el.textContent = "";
  }

  function clearAllErrors() {
    ["skills-error", "level-error", "interest-error", "time-error"].forEach(clearFieldError);
    document.getElementById("form-error-general").textContent = "";
  }

  function validateForm() {
    // Returns true if valid, false and shows errors if not
    var valid = true;

    if (selectedSkills.length === 0 && !skillsHidden.value.trim()) {
      showFieldError("skills-error", "Please add at least one skill.");
      valid = false;
    }

    if (!document.getElementById("level").value) {
      showFieldError("level-error", "Please select your experience level.");
      valid = false;
    }

    if (!document.getElementById("interest").value) {
      showFieldError("interest-error", "Please select an area of interest.");
      valid = false;
    }

    if (!document.getElementById("time").value) {
      showFieldError("time-error", "Please select your time availability.");
      valid = false;
    }

    return valid;
  }


  // ----------------------------------------------------------
  // Form submission and API call
  // ----------------------------------------------------------

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    clearAllErrors();

    if (!validateForm()) return;

    // Show loading state
    setLoadingState(true);

    // Build the request payload
    var payload = {
      skills:   skillsHidden.value.trim() || skillsInput.value.trim(),
      level:    document.getElementById("level").value,
      interest: document.getElementById("interest").value,
      time:     document.getElementById("time").value
    };

    fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        setLoadingState(false);

        if (data.error) {
          document.getElementById("form-error-general").textContent = data.error;
          return;
        }

        renderResults(data.projects || [], data.message);
      })
      .catch(function (err) {
        setLoadingState(false);
        document.getElementById("form-error-general").textContent =
          "Something went wrong. Please try again.";
        console.error("API error:", err);
      });
  });

  function setLoadingState(isLoading) {
    submitBtn.disabled = isLoading;
    btnLabel.style.display   = isLoading ? "none"   : "inline";
    btnLoading.style.display = isLoading ? "inline" : "none";

    // Show results section with loading indicator
    if (isLoading) {
      resultsSection.style.display = "block";
      resultsLoading.style.display = "block";
      resultsGrid.style.display    = "none";
      resultsEmpty.style.display   = "none";
      resultsSection.scrollIntoView({ behavior: "smooth" });
    } else {
      resultsLoading.style.display = "none";
      resultsGrid.style.display    = "grid";
    }
  }


  // ----------------------------------------------------------
  // Render project result cards
  // ----------------------------------------------------------

  function renderResults(projects, message) {
    resultsSection.style.display = "block";
    resultsLoading.style.display = "none";
    resultsGrid.innerHTML        = "";

    if (!projects || projects.length === 0) {
      // Show empty state
      resultsGrid.style.display   = "none";
      resultsEmpty.style.display  = "block";
      if (message) emptyMessage.textContent = message;
      resultsSection.scrollIntoView({ behavior: "smooth" });
      return;
    }

    resultsEmpty.style.display = "none";
    resultsGrid.style.display  = "grid";

    projects.forEach(function (project) {
      var card = buildProjectCard(project);
      resultsGrid.appendChild(card);
    });

    resultsSection.scrollIntoView({ behavior: "smooth" });
  }

  function buildProjectCard(project) {
    var card = document.createElement("div");
    card.className = "project-card";

    // Title
    var title = document.createElement("h3");
    title.className   = "project-card-title";
    title.textContent = project.title;

    // Description (truncated to keep cards uniform)
    var desc = document.createElement("p");
    desc.className   = "project-card-desc";
    desc.textContent = truncate(project.description, 120);

    // Tags row
    var tags = document.createElement("div");
    tags.className = "project-card-tags";

    // Skill tags (first two only to avoid overflow)
    var skills = project.skills || [];
    skills.slice(0, 2).forEach(function (skill) {
      tags.appendChild(makeTag(skill, "skill"));
    });

    // Level tag with colour-coded class
    var levelClass = "level " + (project.level || "").toLowerCase();
    tags.appendChild(makeTag(project.level, levelClass));

    // Time tag
    tags.appendChild(makeTag("Time: " + project.time, "time"));

    // Footer row with action button
    var footer = document.createElement("div");
    footer.className = "project-card-footer";

    var btn = document.createElement("a");
    btn.className = "btn-details";
    btn.textContent = "View Full Project";
    btn.href = "/project/" + project.id;

    footer.appendChild(btn);

    // Assemble card
    card.appendChild(title);
    card.appendChild(desc);
    card.appendChild(tags);
    card.appendChild(footer);

    return card;
  }

  function makeTag(text, type) {
    var span = document.createElement("span");
    span.className   = "project-tag project-tag--" + type;
    span.textContent = text;
    return span;
  }

  function truncate(text, maxLength) {
    if (!text) return "";
    return text.length > maxLength ? text.slice(0, maxLength) + "..." : text;
  }

} // end isIndexPage


// ============================================================
// DETAIL PAGE LOGIC
// ============================================================
if (isDetailPage) {

  var codePanel          = document.getElementById("code-panel");
  var codePanelOverlay   = document.getElementById("code-panel-overlay");
  var codeContent        = document.getElementById("code-content");
  var codePanelFilename  = document.getElementById("code-panel-filename");

  // Both "View Code" buttons (hero and sidebar) trigger the same panel
  var btnViewCode   = document.getElementById("btn-view-code");
  var btnViewCodeSm = document.getElementById("btn-view-code-sm");
  var btnClosePanel = document.getElementById("code-panel-close");

  // Track whether code has already been fetched to avoid repeat requests
  var codeFetched = false;

  function openCodePanel() {
    codePanel.classList.add("active");
    codePanelOverlay.classList.add("active");
    document.body.style.overflow = "hidden"; // Prevent background scroll

    // Fetch code content only on first open
    if (!codeFetched) {
      fetchCode();
    }
  }

  function closeCodePanel() {
    codePanel.classList.remove("active");
    codePanelOverlay.classList.remove("active");
    document.body.style.overflow = "";
  }

  function fetchCode() {
    codeContent.textContent = "Loading starter code...";

    fetch("/project/" + PROJECT_ID + "/code")
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (data.error) {
          codeContent.textContent = "Error: " + data.error;
          return;
        }
        // Display the filename and raw code
        codePanelFilename.textContent = data.filename;
        codeContent.textContent = data.code;
        codeFetched = true;
      })
      .catch(function () {
        codeContent.textContent = "Failed to load starter code. Try downloading it instead.";
      });
  }

  // Wire up open/close buttons if they exist on the page
  if (btnViewCode)   btnViewCode.addEventListener("click", openCodePanel);
  if (btnViewCodeSm) btnViewCodeSm.addEventListener("click", openCodePanel);
  if (btnClosePanel) btnClosePanel.addEventListener("click", closeCodePanel);

  // Close panel when clicking the dark overlay
  if (codePanelOverlay) {
    codePanelOverlay.addEventListener("click", closeCodePanel);
  }

  // Close panel with the Escape key
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeCodePanel();
  });

} // end isDetailPage
