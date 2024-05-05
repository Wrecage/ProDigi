

//This part is for handlinng API (LanguageToolAPI)
document.addEventListener("DOMContentLoaded", function() {
  var checkTextButton = document.getElementById("checkTextButton");
  checkTextButton.addEventListener("click", handleCheckText);
});

function handleCheckText(event) {
  event.preventDefault(); 
  var formData = new FormData(document.getElementById("entryForm"));
  var text = formData.get("content"); 
  fetchTextSuggestions(text);
}

function fetchTextSuggestions(text) {
  fetch("https://api.languagetool.org/v2/check", {
      method: "POST",
      body: "text=" + encodeURIComponent(text) + "&language=en-US",
      headers: {
          "Content-Type": "application/x-www-form-urlencoded"
      }
  })
  .then(response => response.json())
  .then(displaySuggestions)
  .catch(handleError);
}

function displaySuggestions(data) {
  var suggestionsList = document.getElementById("suggestionsList");
  suggestionsList.innerHTML = "";
  data.matches.forEach(match => {
      var listItem = document.createElement("div");
      if (match.context) {
          var correctedText = match.context.text.slice(0, match.context.offset) +
                              `<span class="error-location ">${match.context.text.slice(match.context.offset, match.context.offset + match.context.length)}</span>` +
                              match.context.text.slice(match.context.offset + match.context.length);
          listItem.innerHTML = `
              <p class="error">✗ ${correctedText}</p>
              <p class="correction">✓ ${match.message}</p>
          `;
      } else {
          listItem.textContent = match.message;
      }
      suggestionsList.appendChild(listItem);
  });
}

function handleError(error) {
  console.error("Error:", error);
}