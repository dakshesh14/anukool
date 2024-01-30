const myForm = document.getElementById("myForm");
const myButton = document.getElementById("myButton");
const contentArea = document.getElementById("contentArea");

myForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const formData = new FormData(myForm);

  const aboutJob = formData.get("aboutJob");
  const aboutCompany = formData.get("aboutCompany");

  const payload = {
    job_description: aboutJob,
    company_description: aboutCompany,
  };

  myButton.setAttribute("disabled", "disabled");
  myButton.innerText = "Generating...";

  axios({
    url: "/chat",
    method: "POST",
    data: payload,
  })
    .then((res) => {
      // removing all child elements
      while (contentArea.firstChild) {
        contentArea.removeChild(contentArea.firstChild);
      }

      const pElement = document.createElement("p");
      pElement.classList.add("text-muted");
      pElement.innerText = res.data.answer;

      const h2Element = document.createElement("h2");
      h2Element.innerText = "Generated cover letter:";

      contentArea.appendChild(h2Element);
      contentArea.appendChild(pElement);
    })
    .catch((err) => {
      console.error(err);
    })
    .finally(() => {
      myButton.removeAttribute("disabled");
      myButton.innerText = "Generate";
    });
});
