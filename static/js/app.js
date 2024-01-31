const myForm = document.getElementById("myForm");
const generateButton = document.getElementById("generateButton");
const copyButton = document.getElementById("copyButton");
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

  generateButton.setAttribute("disabled", "disabled");
  generateButton.innerText = "Generating...";

  axios({
    url: "/chat",
    method: "POST",
    data: payload,
  })
    .then((res) => {
      const modalContentArea = document.getElementById("modalOutputArea");
      modalContentArea.innerText = res.data.answer;

      const myModal = new bootstrap.Modal(
        document.getElementById("coverLetterOutput")
      );

      myModal.show();
    })
    .catch((err) => {
      console.error(err);
    })
    .finally(() => {
      generateButton.removeAttribute("disabled");
      generateButton.innerText = "Generate";
    });
});

copyButton.addEventListener("click", (e) => {
  const modalContentArea = document.getElementById("modalOutputArea");
  const textToCopy = modalContentArea.innerText;

  navigator.clipboard.writeText(textToCopy);

  copyButton.innerText = "Copied!";

  const timeout = setTimeout(() => {
    copyButton.innerText = "Copy";
    clearTimeout(timeout);
  }, 2000);
});
